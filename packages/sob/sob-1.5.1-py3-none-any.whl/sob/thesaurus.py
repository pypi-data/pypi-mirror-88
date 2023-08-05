"""
This module provides functionality for creating a data model from a
set of example structures.
"""
import binascii
import collections
import functools
import os
from base64 import b64decode
from copy import copy, deepcopy
from datetime import date, datetime
from types import ModuleType
from typing import (
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)
from urllib.parse import quote_plus

from iso8601 import ParseError, parse_date  # type: ignore

from . import __name__ as _parent_module_name, abc, meta
from .errors import IsInstanceAssertionError
from .meta import escape_reference_token
from .model import detect_format, from_meta, unmarshal
from .properties import Property, TYPES_PROPERTIES
from .types import MutableTypes
from .utilities import get_source, qualified_name
from .utilities.assertion import (
    assert_is_instance,
    assert_is_subclass,
    assert_not_is_instance,
)
from .utilities.inspect import calling_module_name
from .utilities.io import read
from .utilities.string import MAX_LINE_LENGTH, class_name, property_name
from .utilities.types import NULL, NoneType, Null

__all__: List[str] = ["Synonyms", "Thesaurus"]


def _read(data: abc.Readable) -> str:
    string_data: str
    read_data: Union[str, bytes] = read(data)
    if isinstance(read_data, (bytes, bytearray)):
        string_data = str(read_data, encoding="utf-8")
    else:
        string_data = read_data
    return string_data


def _update_types(
    types: abc.MutableTypes, new_types: abc.Types, memo: Dict[str, type]
) -> None:
    """
    This function updates `types` to incorporate any additional types from
    `new_types`, as well as to merge definitions for shared types.

    Parameters:

    - types (sob.properties.types.Types)
    - new_types (sob.properties.types.Types)
    - memo (dict)
    """
    new_type: Union[type, abc.Property]
    for new_type in new_types:
        if isinstance(new_type, type) and issubclass(new_type, abc.Model):
            if type.__name__ in memo:
                existing_type: type = memo[type.__name__]
                new_type_meta: Optional[abc.Meta] = meta.read(new_type)
                assert isinstance(
                    new_type_meta, (abc.ObjectMeta, abc.ArrayMeta)
                )
                _update_model_class_from_meta(
                    existing_type, new_type_meta, memo=memo
                )
                new_type = existing_type
        if new_type not in types:
            types.append(new_type)


def _update_array_meta(
    metadata: abc.ArrayMeta,
    new_metadata: abc.ArrayMeta,
    memo: Optional[Dict[str, type]] = None,
) -> None:
    """
    This function updates `metadata` by adding/updating `metadata.item_types`
    to include types from `new_metadata.item_types`.

    Parameters:

    - metadata (sob.meta.Array)
    - new_metadata (sob.meta.Array)
    - memo (dict)
    """
    assert memo is not None
    new_item_types: Optional[abc.Types] = new_metadata.item_types
    if new_item_types is not None:
        item_types: abc.MutableTypes = (
            MutableTypes()
            if metadata.item_types is None
            else metadata.item_types
            if isinstance(metadata.item_types, abc.MutableTypes)
            else MutableTypes(metadata.item_types)
        )
        _update_types(item_types, new_item_types, memo)
        metadata.item_types = item_types  # type: ignore


def _update_object_meta(
    metadata: abc.ObjectMeta,
    new_metadata: abc.ObjectMeta,
    memo: Optional[Dict[str, type]] = None,
) -> None:
    """
    This function updates `metadata` by adding any properties from
    `new_metadata` not yet part of `metadata`, and updating the property
    types for all shared properties.

    Parameters:

    - metadata (sob.meta.Array)
    - new_metadata (sob.meta.Array)
    - memo (dict)
    """
    assert memo is not None
    assert metadata.properties is not None
    assert new_metadata.properties is not None
    metadata_keys: Set[str] = set(metadata.properties.keys())
    new_metadata_keys: Set[str] = set(new_metadata.properties.keys())
    # Add properties that don't exist
    key: str
    for key in metadata_keys - new_metadata_keys:
        metadata.properties[key] = new_metadata.properties[key]
    # Update shared properties
    for key in metadata_keys & new_metadata_keys:
        types_: Optional[abc.Types] = metadata.properties[key].types
        new_types: Optional[abc.Types] = new_metadata.properties[key].types
        if new_types is not None:
            mutable_types: abc.MutableTypes = (
                MutableTypes()
                if types_ is None
                else types_
                if isinstance(types_, abc.MutableTypes)
                else MutableTypes(types_)
            )
            _update_types(
                mutable_types, new_types, memo=memo,
            )
            types_ = mutable_types
        metadata.properties[key].types = types_  # type: ignore


def _update_object_class_from_meta(
    object_class: type,
    new_object_metadata: abc.ObjectMeta,
    memo: Dict[str, type],
) -> None:
    """
    This function merges new metadata into an existing object model's metadata.

    Parameters:

    - object_class (type)
    - new_object_metadata (sob.meta.Object)
    - memo (dict)
    """
    assert isinstance(new_object_metadata, abc.ObjectMeta)
    object_metadata: Optional[abc.Meta] = meta.read(object_class)
    assert isinstance(object_metadata, (abc.ObjectMeta, NoneType))
    _update_object_meta(object_metadata, new_object_metadata, memo)
    # Recreate the object class
    updated_object_class: type = from_meta(
        object_class.__name__,
        object_metadata,
        module=object_class.__module__,
        docstring=object_class.__doc__,
    )
    # Apply the rest of the changes to the existing model class
    setattr(
        object_class, "__init__", getattr(updated_object_class, "__init__")
    )
    setattr(object_class, "_source", get_source(updated_object_class))


def _update_array_class_from_meta(
    array_class: type,
    new_array_metadata: abc.ArrayMeta,
    memo: Optional[Dict[str, type]] = None,
) -> None:
    """
    This function merges new metadata into an existing array model's metadata.

    Parameters:

    - array_class (type)
    - new_array_metadata (sob.meta.Array)
    - memo (dict)
    """
    assert memo is not None
    assert isinstance(new_array_metadata, abc.ArrayMeta)
    array_metadata: abc.Meta = meta.writable(array_class)
    assert isinstance(array_metadata, abc.ArrayMeta)
    _update_array_meta(array_metadata, new_array_metadata, memo=memo)
    # Since the two array classes have the same name--the class
    # definition/declaration won't change, so updating the metadata is all that
    # is necessary


def _update_model_class_from_meta(
    model_class: type,
    new_metadata: Union[abc.ArrayMeta, abc.ObjectMeta],
    memo: Optional[Dict[str, type]] = None,
) -> None:
    """
    This function merges new metadata into an existing model's metadata.

    Parameters:

    - model_class (type)
    - new_metadata (sob.meta.Array|sob.meta.Object)
    - memo (dict)
    """
    assert memo is not None
    assert issubclass(model_class, (abc.Array, abc.Object))
    # Update the model metadata in-place
    if issubclass(model_class, abc.Array):
        assert isinstance(new_metadata, abc.ArrayMeta)
        _update_array_class_from_meta(model_class, new_metadata, memo=memo)
    else:
        assert issubclass(model_class, abc.Object)
        assert isinstance(new_metadata, abc.ObjectMeta)
        _update_object_class_from_meta(model_class, new_metadata, memo=memo)


def class_name_from_pointer(pointer: str) -> str:
    """
    This function returns a class name based on the
    [sob.thesaurus.Thesaurus](#Thesaurus) key of the
    [sob.thesaurus.Synonyms](#Synonyms) instance to which an element belongs,
    combined with the *JSON pointer* of the applicable element. This function
    can be substituted for another, when generating a module from a thesaurus,
    by passing a function to the `name` parameter of
    [sob.thesaurus.Thesaurus.get_module_source](#Thesaurus-getmodulesource),
    [sob.thesaurus.Thesaurus.get_module](#Thesaurus-getmodule), or
    [sob.thesaurus.Thesaurus.save_module](#Thesaurus-savemodule).

    Parameters:

    - pointer (str): The synonyms key + JSON pointer of the element for which
      the class is being generated.
    """
    return class_name(
        f"{pointer[:-2]}/item"
        if pointer.endswith("/0")
        else pointer.replace("/0/", "/item/")
    )


def _get_models_from_meta(
    pointer: str,
    metadata: Union[abc.ArrayMeta, abc.ObjectMeta],
    module: str = "__main__",
    memo: Optional[Dict[str, type]] = None,
    name: Callable[[str], str] = class_name_from_pointer,
) -> List[type]:
    """
    This function generates and updates classes from metadata.

    Parameters:

    - pointer (str)
    - metadata (sob.meta.Array|sob.meta.Object)
    - module (str)
    - memo (dict)
    """
    assert memo is not None
    new_models: List[type] = []
    # If a model of the same pointer already exists, we update it to
    # reflect our metadata, otherwise--we create a new model
    if pointer in memo:
        _update_model_class_from_meta(memo[pointer], metadata, memo=memo)
    else:
        new_model: type = from_meta(name(pointer), metadata, module=module)
        memo[pointer] = new_model
        new_models.append(new_model)
    return new_models


def _is_base64(value: str) -> bool:
    """
    Test to see if `value` can be interpreted as base-64 encoded binary data.
    """
    try:
        b64decode(bytes(value, encoding="utf-8"), validate=True)
        return True
    except binascii.Error:
        return False


@functools.lru_cache(maxsize=128)
def _str_date_or_datetime(value: str) -> type:
    """
    Test to see if `value` can be interpreted as an ISO-8601 encoded `date` or
    `datetime`.
    """
    try:
        timestamp: datetime = parse_date(value)
        if (
            timestamp.hour
            or timestamp.minute
            or timestamp.second
            or timestamp.microsecond
        ):
            return date
        else:
            return datetime
    except ParseError:
        return str


def _is_datetime_str(value: str) -> bool:
    """
    Test to see if `value` can be interpreted as an ISO-8601 encoded
    `datetime`.
    """
    return _str_date_or_datetime(value) is datetime


def _is_date_str(value: str) -> bool:
    """
    Test to see if `value` can be interpreted as an ISO-8601 encoded
    `date`.
    """
    return _str_date_or_datetime(value) is date


class Synonyms(set):
    """
    This class contains deserialized data, implied to represent variations of
    one type of entity, and is used to infer a model for that entity.
    """

    def __init__(
        self, items: Iterable[Union[abc.Readable, abc.MarshallableTypes]] = ()
    ) -> None:
        self._data_type: Optional[type] = None
        self._nullable: bool = False
        super().__init__()
        if items:
            self.__ior__(items)

    def add(self, item: Union[abc.Readable, abc.MarshallableTypes]) -> None:
        """
        This method adds a synonymous item to the set. If the item is a
        file-like (input/output) object, that object is first read,
        deserialized, and unmarshalled.

        Parameters:

        - item ({}): A file-like or a JSON-serializable python object.
        """.format(
            "|".join(
                qualified_name(item_type)
                for item_type in ((abc.Readable,) + abc.MARSHALLABLE_TYPES)
            )
        )
        assert isinstance(item, (abc.Readable,) + abc.MARSHALLABLE_TYPES)
        if isinstance(item, abc.Readable):
            # Deserialize and unmarshal file-like objects
            item = unmarshal(detect_format(_read(item))[0])
        elif isinstance(item, Iterable) and not isinstance(
            item, (str, abc.Model, Mapping)
        ):
            if isinstance(item, Iterable) and not isinstance(item, Sequence):
                item = tuple(item)
            # Unmarshal items which appear to not have been part of an
            # unmarshalled container
            item = unmarshal(item)
        if item is NULL:
            self._nullable = True
        elif item is not None:
            if self._data_type is None:
                self._data_type = type(item)
            else:
                # If there is a data type discrepancy between `float` and
                # `int`, use `float`.
                if (
                    issubclass(self._data_type, (int, float))
                    and isinstance(item, (int, float))
                    and (type(item) is not self._data_type)
                ):
                    self._data_type = float
                else:
                    assert isinstance(item, self._data_type)
            super().add(item)

    def union(  # type: ignore
        self, other: Iterable[Union[abc.Readable, abc.MarshallableTypes]]
    ) -> "Synonyms":
        """
        This method returns an instance of `Synonyms` which incorporates
        all (non-redundant) items from both `self` and `other`.
        """
        new_synonyms: Synonyms = copy(self)
        new_synonyms |= other
        return new_synonyms

    def __ior__(
        self, other: Iterable[Union[abc.Readable, abc.MarshallableTypes]]
    ) -> "Synonyms":
        assert_is_instance("other", other, Iterable)
        assert_not_is_instance("other", other, (Mapping, abc.Dictionary))
        item: Union[abc.Readable, abc.MarshallableTypes]
        for item in other:
            self.add(item)
        return self

    def __or__(
        self, other: Iterable[Union[abc.Readable, abc.MarshallableTypes]]
    ) -> "Synonyms":
        return copy(self).__ior__(other)

    def __copy__(self) -> "Synonyms":
        return type(self)(self)

    def __deepcopy__(self, memo: Optional[dict] = None) -> "Synonyms":
        return type(self)(deepcopy(item) for item in self)

    def _get_type(self) -> type:
        assert self._data_type is not None
        data_type: type = self._data_type
        # Determine if this is a string encoded to represent a `date`,
        # `datetime`, or base-64 encoded `bytes`.
        if issubclass(self._data_type, str):
            if all(
                _is_base64(item) for item in self if item not in (None, NULL)
            ):
                data_type = bytes
            elif all(
                _is_datetime_str(item)
                for item in self
                if item not in (None, NULL)
            ):
                data_type = datetime
            elif all(
                _is_date_str(item) for item in self if item not in (None, NULL)
            ):
                data_type = date
        else:
            # This function should only be invoked for simple types, so we
            # first verify the data type is not a container
            assert not issubclass(
                self._data_type, (abc.Model, Mapping, Collection)
            )
        assert data_type is not None
        return data_type

    def _get_property_names_values(
        self,
    ) -> abc.OrderedDict[str, List[abc.MarshallableTypes]]:
        keys_values: abc.OrderedDict[
            str, List[abc.MarshallableTypes]
        ] = collections.OrderedDict()
        item: Union[Mapping, abc.Dictionary]
        for item in self:
            try:
                assert isinstance(item, (Mapping, abc.Dictionary))
            except AssertionError:
                raise IsInstanceAssertionError(
                    "item", item, (Mapping, abc.Dictionary)
                )
            value: abc.MarshallableTypes
            for key, value in item.items():
                if key not in keys_values:
                    keys_values[key] = []
                keys_values[key].append(value)
        return keys_values

    def _get_object_models(
        self,
        pointer: str,
        module: str = "__main__",
        name: Callable[[str], str] = class_name_from_pointer,
        memo: Optional[Dict[str, type]] = None,
    ) -> Iterable[type]:
        metadata: abc.ObjectMeta = meta.Object()
        metadata.properties = meta.Properties()  # type: ignore
        key: str
        property_name_: str
        values: List[abc.MarshallableTypes]
        for key, values in self._get_property_names_values().items():
            property_name_ = property_name(key)
            item_type: Optional[type] = None
            is_model: bool = False
            property_synonyms: Synonyms = type(self)(values)
            for item_type in property_synonyms._get_types(
                pointer=f"{pointer}/{escape_reference_token(property_name_)}",
                module=module,
                memo=memo,
                name=name,
            ):
                if issubclass(item_type, abc.Model):
                    is_model = True
                    yield item_type
                else:
                    is_model = False
            if item_type:
                if is_model:
                    metadata.properties[property_name_] = Property(
                        name=key,
                        types=[item_type]
                        + ([Null] if property_synonyms._nullable else []),
                    )
                elif property_synonyms._nullable:
                    metadata.properties[property_name_] = Property(
                        name=key, types=[TYPES_PROPERTIES[item_type](), Null]
                    )
                else:
                    metadata.properties[property_name_] = TYPES_PROPERTIES[
                        item_type
                    ](name=key)
            else:
                metadata.properties[property_name_] = Property(name=key)
        model_class: type
        for model_class in _get_models_from_meta(
            pointer, metadata, module=module, memo=memo, name=name
        ):
            yield model_class

    def _get_array_models(
        self,
        pointer: str,
        module: str = "__main__",
        name: Callable[[str], str] = class_name_from_pointer,
        memo: Optional[Dict[str, type]] = None,
    ) -> Iterable[type]:
        unified_items: Synonyms = type(self)()
        items: List[abc.MarshallableTypes]
        for items in self:
            unified_items |= items
        item_type: Optional[type] = None
        for item_type in unified_items._get_types(
            pointer=f"{pointer}/0", module=module, memo=memo, name=name
        ):
            yield item_type
        metadata: abc.ArrayMeta = meta.Array(
            item_types=(None if item_type is None else [item_type])
        )
        array_type: type
        for array_type in _get_models_from_meta(
            pointer, metadata, module=module, memo=memo, name=name
        ):
            yield array_type

    def _get_types(
        self,
        pointer: str,
        module: str = "__main__",
        name: Callable[[str], str] = class_name_from_pointer,
        memo: Optional[Dict[str, type]] = None,
    ) -> Iterable[type]:
        # `_memo` holds a dictionary of all classes which have been created,
        # and is passed recursively to facilitate de-duplication
        memo_is_new: bool = False
        if memo is None:
            memo = {}
            memo_is_new = True
        type_iterator: Iterable[type]
        if self._data_type is None:
            type_iterator = []
        elif issubclass(
            self._data_type, (Mapping, abc.Object, abc.Dictionary)
        ):
            type_iterator = self._get_object_models(
                pointer, module=module, memo=memo, name=name
            )
        elif issubclass(
            self._data_type, (Iterable, abc.Array)
        ) and not issubclass(self._data_type, str):
            type_iterator = self._get_array_models(
                pointer, module=module, memo=memo, name=name
            )
        else:
            type_iterator = [self._get_type()]
        # If this was the call which initialized our `_memo`, we want to
        # force the iterator to run, in order to fully update all models before
        # returning them to the user (as some will be updated over the course
        # of traversal when analogous elements are encountered).
        if memo_is_new:
            type_iterator = list(type_iterator)
        type_: type
        for type_ in type_iterator:
            yield type_

    def get_models(
        self,
        pointer: str,
        module: str = "__main__",
        name: Callable[[str], str] = class_name_from_pointer,
    ) -> Iterable[type]:
        """
        Retrieve a sequence of class definitions representing a data model
        capable of describing these synonyms.

        Parameters:

        - pointer (str): A JSON pointer for the top-level model class, used to
          infer class names.
        - module (str): The name of the module in which model classes will be
          defined. This defaults to "__main__".
        - name (str) = sob.thesaurus.class_name_from_pointer:
          A function which accepts one `str` argument—a synonym key
          concatenated with "#" and JSON pointer (for example:
          "key#/body/items/0") and which returns a `str` which will be the
          resulting class name (for example: "KeyBodyItemsItem").
        """
        assert callable(name)
        # This assertion ensures `self` contains data which can be described by
        # a model class.
        assert self._data_type and not issubclass(
            self._data_type, (str, bytes, bytearray)
        )
        assert_is_subclass(
            f"{qualified_name(type(self))}._data_type",
            self._data_type,
            (Mapping, abc.Dictionary, Iterable),
        )
        for model_class in self._get_types(
            pointer="{}#".format(quote_plus(pointer, safe="/+")),
            module=module,
            name=name,
        ):
            assert_is_subclass("model_class", model_class, abc.Model)
            yield model_class


def get_class_meta_attribute_assignment_source(
    class_name_: str, attribute_name: str, metadata: abc.Meta,
) -> str:
    """
    This function generates source code for setting a metadata attribute on
    a class.

    Parameters:

    - class_name (str): The name of the class to which we want to assign a
      metadata attribute.
    - attribute_name (str): The name of the attribute we want to assign.
    - metadata (sob.abc.Meta): The metadata from which to take the assigned
      value.
    """
    writable_function_name: str = "{}.meta.{}_writable".format(
        _parent_module_name,
        (
            "object"
            if isinstance(metadata, abc.ObjectMeta)
            else "array"
            if isinstance(metadata, abc.ArrayMeta)
            else "dictionary"
        ),
    )

    def noqa_line_if_long(line: str) -> str:
        # We want to add "  # noqa" at the end of any line
        # which is within 4 spaces of the maximum line length, since
        # reformatting with `black` will add an additional 4 spaces.
        if len(line) > (MAX_LINE_LENGTH - 4):
            line = f"{line}  # noqa"
        return line

    # We insert "  # type: ignore" at the end of the first line where the value
    # is assigned due to mypy issues with properties having getters and setters
    represent_metadata_attribute: str = "\n".join(
        map(
            noqa_line_if_long,
            repr(getattr(metadata, attribute_name)).split("\n"),
        )
    )
    return (
        f"{writable_function_name}(  # type: ignore\n"
        f"    {class_name_}\n"
        f").{attribute_name} = {represent_metadata_attribute}"
    )


class Thesaurus(collections.OrderedDict):
    """
    TODO
    """

    def __init__(
        self,
        items: Optional[
            Union[
                Dict[
                    str, Iterable[Union[abc.Readable, abc.MarshallableTypes]]
                ],
                Iterable[
                    Tuple[
                        str,
                        Iterable[Union[abc.Readable, abc.MarshallableTypes]],
                    ]
                ],
            ]
        ] = None,
        **kwargs: Iterable[Union[abc.Readable, abc.MarshallableTypes]],
    ) -> None:
        super().__init__(*((items,) if items else ()), **kwargs)

    def __setitem__(
        self,
        key: str,
        value: Iterable[Union[abc.Readable, abc.MarshallableTypes]],
    ) -> None:
        if not isinstance(value, Synonyms):
            value = Synonyms(value)
        return super().__setitem__(key, value)

    def __getitem__(self, key: str) -> Synonyms:
        try:
            return super().__getitem__(key)
        except KeyError:
            self[key] = Synonyms()
            return self[key]

    def __copy__(self) -> "Thesaurus":
        return type(self)(self.items())

    def __deepcopy__(self, memo: Optional[dict] = None) -> "Thesaurus":
        return type(self)(deepcopy(item) for item in self.items())

    def __iadd__(self, other: "Thesaurus") -> "Thesaurus":
        assert isinstance(other, Thesaurus)
        key: str
        value: Synonyms
        for key, value in other.items():
            self[key] |= value
        return self

    def __add__(self, other: "Thesaurus") -> "Thesaurus":
        return copy(self).__iadd__(other)

    def get_models(
        self,
        module: str = "__main__",
        name: Callable[[str], str] = class_name_from_pointer,
    ) -> Iterable[type]:
        key: str
        synonyms: Synonyms
        for key, synonyms in self.items():
            model_class: type
            for model_class in synonyms.get_models(
                key, module=module, name=name
            ):
                yield model_class

    def _get_module_source(
        self,
        module_name: str = "__main__",
        name: Callable[[str], str] = class_name_from_pointer,
    ) -> str:
        class_names_metadata: abc.OrderedDict[
            str, Union[abc.ObjectMeta, abc.ArrayMeta]
        ] = collections.OrderedDict()
        imports: List[str] = []
        classes: List[str] = []
        metadatas: List[str] = []
        model_class: type
        for model_class in self.get_models(module=module_name, name=name):
            imports_str: str
            import_line: str
            source: str = get_source(model_class)
            if "\n\n\n" not in source:
                raise ValueError(source)
            imports_str, source = source.split("\n\n\n")
            for import_line in imports_str.split("\n"):
                if import_line not in imports:
                    imports.append(import_line)
            classes.append(source)
            meta_instance: Optional[abc.Meta] = meta.read(model_class)
            assert isinstance(meta_instance, (abc.ObjectMeta, abc.ArrayMeta))
            class_names_metadata[model_class.__name__] = meta_instance
        for negative_index, class_name_metadata in enumerate(
            class_names_metadata.items(), -(len(class_names_metadata) - 1)
        ):
            separator: str
            class_name_: str
            metadata: Union[abc.ObjectMeta, abc.ArrayMeta]
            class_name_, metadata = class_name_metadata
            assert isinstance(metadata, (abc.ObjectMeta, abc.ArrayMeta))
            if isinstance(metadata, abc.ObjectMeta):
                metadatas.append(
                    get_class_meta_attribute_assignment_source(
                        class_name_, "properties", metadata
                    )
                )
            else:
                metadatas.append(
                    get_class_meta_attribute_assignment_source(
                        class_name_, "item_types", metadata
                    )
                )
        return "\n".join(
            sorted(
                imports,
                key=lambda line: (
                    1 if line == f"import {_parent_module_name}" else 0
                ),
            )
            + ["\n"]
            + classes
            + metadatas
        )

    def get_module_source(
        self, name: Callable[[str], str] = class_name_from_pointer
    ) -> str:
        """
        This method generates and returns the source code for a module
        defining data models applicable to the data contained in this
        thesaurus.

        Parameters:

        - name (str) = sob.thesaurus.class_name_from_pointer:
          A function which accepts one `str` argument—a synonym key
          concatenated with "#" and JSON pointer (for example:
          "key#/body/items/0") and which returns a `str` which will be the
          resulting class name (for example: "KeyBodyItemsItem").
        """
        return self._get_module_source("__main__", name=name)

    def get_module(
        self, name: Callable[[str], str] = class_name_from_pointer
    ) -> ModuleType:
        """
        This method generates and returns a module defining data models
        applicable to the data contained in this thesaurus. This module is not
        suitable for writing out for static use--use `Thesaurus.save_module`
        to generate and write a model suitable for static use.

        Parameters:

        - name (str) = sob.thesaurus.class_name_from_pointer:
          A function which accepts one `str` argument—a synonym key
          concatenated with "#" and JSON pointer (for example:
          "key#/body/items/0") and which returns a `str` which will be the
          resulting class name (for example: "KeyBodyItemsItem").
        """
        # For pickling to work, the `__module__` variable needs to be set to
        # the calling module.
        module_name: str = calling_module_name(2)
        module: ModuleType = ModuleType(module_name)
        exec(self._get_module_source(module_name, name=name), module.__dict__)
        return module

    def save_module(
        self, path: str, name: Callable[[str], str] = class_name_from_pointer,
    ) -> None:
        """
        This method generates and saves the source code for a module
        defining data models applicable to the data contained in this
        thesaurus.

        Parameters:

        - path (str): The file path where the data will be written.
        - name (str) = sob.thesaurus.class_name_from_pointer:
          A function which accepts one `str` argument—a synonym key
          concatenated with "#" and JSON pointer (for example:
          "key#/body/items/0") and which returns a `str` which will be the
          resulting class name (for example: "KeyBodyItemsItem").
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        module_source: str = self.get_module_source(name=name)
        with open(path, "w") as module_io:
            module_io.write(module_source)

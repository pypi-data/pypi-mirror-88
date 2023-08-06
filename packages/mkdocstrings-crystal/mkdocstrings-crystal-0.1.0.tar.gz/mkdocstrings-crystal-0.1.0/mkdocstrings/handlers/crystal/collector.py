import abc
import collections
import copy
import json
import re
import subprocess
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

from mkdocstrings.handlers.base import BaseCollector, CollectionError

T = TypeVar("T")


class DocObject(collections.UserDict, metaclass=abc.ABCMeta):
    JSON_KEY: str
    parent: Optional["DocObject"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None
        for key, sublist in self.items():
            if key in DOC_TYPES:
                for subobj in sublist:
                    subobj.parent = self

    @property
    def name(self):
        return self["name"]

    @property
    def rel_id(self):
        return self["name"]

    @property
    def abs_id(self):
        return self["id"]

    def __repr__(self, skip_keys={"doc", "summary", "url", "locations", "html_id", "path"}):
        return type(self).__name__ + repr(
            {k: v for k, v in self.items() if v and k not in skip_keys}
        )

    def __bool__(self):
        return True

    def lookup(self, identifier: str) -> "DocObject":
        ret_obj = obj = self
        path = re.split(r"(::|#|\.|:|^)", identifier)
        for sep, name in zip(path[1::2], path[2::2]):
            try:
                order = _LOOKUP_ORDER[sep]
            except KeyError:
                raise CollectionError(f"{identifier!r} - unknown separator {sep!r}") from None
            mapp = collections.ChainMap(*(obj[t.JSON_KEY] for t in order if t.JSON_KEY in obj))
            obj = mapp.get(name.replace(" ", "")) or mapp.get(name.split("(", 1)[0])
            if obj is None:
                if self.parent:
                    return self.parent.lookup(identifier)
                raise CollectionError(f"{identifier!r} - can't find {name!r}")
            ret_obj = obj
            if isinstance(obj, DocType) and obj.get("aliased"):
                try:
                    obj = self.lookup(obj["aliased"])
                except CollectionError:
                    pass
        return ret_obj


class DocType(DocObject):
    JSON_KEY = "types"

    @property
    def abs_id(self):
        return self["full_name"].split("(", 1)[0]

    def walk_types(self) -> Iterator["DocType"]:
        for typ in self["types"]:
            yield typ
            yield from typ.walk_types()


class DocConstant(DocObject):
    JSON_KEY = "constants"

    @property
    def abs_id(self):
        return (self.parent.abs_id + "::" if self.parent else "") + self.rel_id


class DocMethod(DocObject, metaclass=abc.ABCMeta):
    METHOD_SEP: str = ""
    METHOD_ID_SEP: str

    @property
    def rel_id(self):
        d = self["def"]

        args = [arg["external_name"] for arg in d["args"]]
        if d.get("splat_index") is not None:
            args[d["splat_index"]] = "*" + args[d["splat_index"]]
        if d.get("double_splat"):
            args.append("**" + d["double_splat"]["external_name"])
        if d.get("block_arg"):
            args.append("&")

        return self.name + "(" + ",".join(args) + ")"

    @property
    def abs_id(self):
        return (self.parent.abs_id if self.parent else "") + self.METHOD_ID_SEP + self.rel_id

    @property
    def short_name(self):
        return self.METHOD_SEP + self.name


class DocInstanceMethod(DocMethod):
    JSON_KEY = "instance_methods"
    METHOD_SEP = METHOD_ID_SEP = "#"


class DocClassMethod(DocMethod):
    JSON_KEY = "class_methods"
    METHOD_SEP = METHOD_ID_SEP = "."


class DocMacro(DocMethod):
    JSON_KEY = "macros"
    METHOD_ID_SEP = ":"


class DocConstructor(DocClassMethod):
    JSON_KEY = "constructors"


DOC_TYPES = {
    t.JSON_KEY: t
    for t in [DocType, DocInstanceMethod, DocClassMethod, DocMacro, DocConstructor, DocConstant]
}

_LOOKUP_ORDER = {
    "": [DocType, DocConstant, DocInstanceMethod, DocClassMethod, DocConstructor, DocMacro],
    "::": [DocType, DocConstant],
    "#": [DocInstanceMethod, DocClassMethod, DocConstructor, DocMacro],
    ".": [DocClassMethod, DocConstructor, DocInstanceMethod, DocMacro],
    ":": [DocMacro],
}

D = TypeVar("D", bound=DocObject)


class DocMapping(Generic[D]):
    def __init__(self, items: Sequence[D]):
        self.items = items
        self.search = search = {}
        for item in self.items:
            search.setdefault(item.rel_id, item)
            search.setdefault(item.name, item)

    def __iter__(self) -> Iterator[D]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, key: str) -> bool:
        return key in self.search

    def __getitem__(self, key: str) -> D:
        return self.search[key]

    def __repr__(self):
        return "DocMapping" + repr(list(self.search))


def _object_hook(obj: MutableMapping[str, T]) -> MutableMapping[str, Union[DocObject, T]]:
    for key, sublist in obj.items():
        if key in DOC_TYPES:
            obj[key] = DocMapping(list(map(DOC_TYPES[key], obj[key])))
    return obj


class CrystalCollector(BaseCollector):
    default_config: dict = {
        "nested_types": False,
        "file_filters": True,
    }

    def __init__(self, crystal_docs_flags: Sequence[str] = ()):
        with subprocess.Popen(
            [
                "crystal",
                "docs",
                "--format=json",
                "--project-name=",
                "--project-version=",
                "--source-refname=master",
                *crystal_docs_flags,
            ],
            stdout=subprocess.PIPE,
        ) as proc:
            self.root = DocType(json.load(proc.stdout, object_hook=_object_hook)["program"])

    def collect(
        self, identifier: str, config: Mapping[str, Any], *, context: Optional[DocObject] = None
    ) -> DocObject:
        config = collections.ChainMap(config, self.default_config)

        if identifier.startswith("::") or not context:
            context = self.root

        obj = copy.copy(context.lookup(identifier))

        if isinstance(obj, DocType) and not config["nested_types"]:
            obj[DocType.JSON_KEY] = {}
        for key in DOC_TYPES:
            if not obj.get(key):
                continue
            obj[key] = self._filter(config["file_filters"], obj[key], self._get_locations)
        return obj

    @classmethod
    def _get_locations(cls, obj: DocObject) -> Sequence[str]:
        if isinstance(obj, DocConstant):
            obj = obj.parent
            if not obj:
                return ()
        if isinstance(obj, DocType):
            return [loc["url"].rsplit("#", 1)[0] for loc in obj["locations"]]
        else:
            return (obj["source_link"].rsplit("#", 1)[0],)

    @classmethod
    def _filter(
        cls,
        filters: Union[bool, Sequence[str]],
        mapp: DocMapping[D],
        getter: Callable[[D], Sequence[str]],
    ) -> DocMapping[D]:
        if filters is False:
            return DocMapping(())
        if filters is True:
            return mapp
        try:
            re.compile(filters[0])
        except (TypeError, IndexError):
            raise CollectionError(
                f"Expected a non-empty list of strings as filters, not {filters!r}"
            )

        return DocMapping([item for item in mapp if _apply_filter(filters, getter(item))])


def _apply_filter(
    filters: Iterable[str],
    tags: Sequence[str],
) -> bool:
    match = False
    for filt in filters:
        filter_kind = True
        if filt.startswith("!"):
            filter_kind = False
            filt = filt[1:]
        if any(re.search(filt, s) for s in tags):
            match = filter_kind
    return match

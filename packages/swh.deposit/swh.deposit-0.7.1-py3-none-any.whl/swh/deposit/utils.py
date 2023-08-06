# Copyright (C) 2018-2020 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from types import GeneratorType
from typing import Any, Dict, Tuple, Union

import iso8601
import xmltodict

from swh.model.identifiers import SWHID, normalize_timestamp, parse_swhid
from swh.model.model import MetadataTargetType


def parse_xml(stream, encoding="utf-8"):
    namespaces = {
        "http://www.w3.org/2005/Atom": "atom",
        "http://www.w3.org/2007/app": "app",
        "http://purl.org/dc/terms/": "dc",
        "https://doi.org/10.5063/SCHEMA/CODEMETA-2.0": "codemeta",
        "http://purl.org/net/sword/terms/": "sword",
        "https://www.softwareheritage.org/schema/2018/deposit": "swh",
    }

    data = xmltodict.parse(
        stream,
        encoding=encoding,
        namespaces=namespaces,
        process_namespaces=True,
        dict_constructor=dict,
    )
    if "atom:entry" in data:
        data = data["atom:entry"]
    return data


def merge(*dicts):
    """Given an iterator of dicts, merge them losing no information.

    Args:
        *dicts: arguments are all supposed to be dict to merge into one

    Returns:
        dict merged without losing information

    """

    def _extend(existing_val, value):
        """Given an existing value and a value (as potential lists), merge
           them together without repetition.

        """
        if isinstance(value, (list, map, GeneratorType)):
            vals = value
        else:
            vals = [value]
        for v in vals:
            if v in existing_val:
                continue
            existing_val.append(v)
        return existing_val

    d = {}
    for data in dicts:
        if not isinstance(data, dict):
            raise ValueError("dicts is supposed to be a variable arguments of dict")

        for key, value in data.items():
            existing_val = d.get(key)
            if not existing_val:
                d[key] = value
                continue
            if isinstance(existing_val, (list, map, GeneratorType)):
                new_val = _extend(existing_val, value)
            elif isinstance(existing_val, dict):
                if isinstance(value, dict):
                    new_val = merge(existing_val, value)
                else:
                    new_val = _extend([existing_val], value)
            else:
                new_val = _extend([existing_val], value)
            d[key] = new_val
    return d


def normalize_date(date):
    """Normalize date fields as expected by swh workers.

    If date is a list, elect arbitrarily the first element of that
    list

    If date is (then) a string, parse it through
    dateutil.parser.parse to extract a datetime.

    Then normalize it through
    swh.model.identifiers.normalize_timestamp.

    Returns
        The swh date object

    """
    if isinstance(date, list):
        date = date[0]
    if isinstance(date, str):
        date = iso8601.parse_date(date)

    return normalize_timestamp(date)


def compute_metadata_context(
    swhid_reference: Union[SWHID, str]
) -> Tuple[MetadataTargetType, Dict[str, Any]]:
    """Given a SWHID object, determine the context as a dict.

    The parse_swhid calls within are not expected to raise (because they should have
    been caught early on).

    """
    metadata_context: Dict[str, Any] = {"origin": None}
    if isinstance(swhid_reference, SWHID):
        object_type = MetadataTargetType(swhid_reference.object_type)
        assert object_type != MetadataTargetType.ORIGIN

        if swhid_reference.metadata:
            path = swhid_reference.metadata.get("path")
            metadata_context = {
                "origin": swhid_reference.metadata.get("origin"),
                "path": path.encode() if path else None,
            }
            snapshot = swhid_reference.metadata.get("visit")
            if snapshot:
                metadata_context["snapshot"] = parse_swhid(snapshot)

            anchor = swhid_reference.metadata.get("anchor")
            if anchor:
                anchor_swhid = parse_swhid(anchor)
                metadata_context[anchor_swhid.object_type] = anchor_swhid
    else:
        object_type = MetadataTargetType.ORIGIN

    return object_type, metadata_context

import logging
from typing import Any
from typing import Dict
from typing import IO
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from astropy.io import fits
from astropy.io.fits.hdu.hdulist import HDUList
from dkist_fits_specifications.spec214 import load_full_spec214
from dkist_fits_specifications.utils import expand_naxis


logger = logging.getLogger(__name__)

__all__ = ["convert_spec122_to_spec214"]

type_map = {"int": int, "float": float, "str": str, "bool": bool}


def convert_spec122_to_spec214(
    spec122_input: Union[HDUList, dict, fits.header.Header, str, IO, List]
) -> Union[dict, HDUList]:
    """
    Convert spec 122 headers to spec 214 headers
    :param spec122_input: Spec 122 headers or headers + data to convert
    """
    # extract headers and data
    input_headers, input_data = _parse_spec122(spec122_input)
    # convert headers
    output_headers = _add_214_headers(input_headers)
    if input_data:  # return hdu list if the input had data
        return _format_output_hdu(output_headers, input_data)
    return output_headers  # return headers if only headers were given


def _parse_spec122(
    spec122_input: Union[HDUList, dict, fits.header.Header, str, IO, List]
) -> Tuple[dict, Optional[bytes]]:
    """
    Parse out a header and optional data from the various types of input
    """
    if isinstance(spec122_input, dict):
        return spec122_input, None
    if isinstance(spec122_input, fits.header.Header):
        return dict(spec122_input), None
    if isinstance(spec122_input, HDUList):
        try:
            return dict(spec122_input[1].header), spec122_input[1].data
        except IndexError:  # non-compressed
            return dict(spec122_input[0].header), spec122_input[0].data

    # If headers are of any other type, see if it is a file and try to open that
    try:  # compressed
        with fits.open(spec122_input, disable_image_compression=True) as hdus:
            return dict(hdus[1].header), hdus[1].data
    except IndexError:  # non-compressed
        with fits.open(spec122_input, disable_image_compression=True) as hdus:
            return dict(hdus[0].header), hdus[0].data


def _format_output_hdu(hdr, data) -> HDUList:
    new_hdu = fits.PrimaryHDU(data)
    hdu_list = fits.HDUList([new_hdu])
    for key, value in hdr.items():
        hdu_list[0].header[key] = value
    return hdu_list


generic_spec214_schema = load_full_spec214().values()  # global for performance


def _create_spec214_schema_for_header(hdr: dict) -> Dict[str, Dict[str, Any]]:
    s = {
        key: schema for definition in generic_spec214_schema for (key, schema) in definition.items()
    }
    return expand_naxis(hdr["NAXIS"], s)  # only need to account for spec 122 input


def _add_214_headers(hdr: dict):
    """
    Adds new 214 headers into dictionary
    """
    result = {}  # output headers
    spec214_schema = _create_spec214_schema_for_header(hdr)

    # translate 122 -> 214 headers
    for key, key_schema in spec214_schema.items():
        result.update(_translate_key(key, key_schema, hdr))

    # add remaining header values to result
    hdr_keys_not_translated = {k: v for k, v in hdr.items() if k not in result}
    result.update(hdr_keys_not_translated)
    return result


def _translate_key(key, key_schema, hdr) -> dict:
    default_values = {"str": "default", "int": -999, "float": -999.9}
    key_is_copied = key_schema.get("copy")
    copy_schema_only = key_schema.get("copy") == "schema"
    key_is_renamed = key_schema.get("rename")
    renamed_key_is_in_header = key_schema.get("rename") in hdr
    key_is_required = key_schema.get("required")
    key_is_in_header = key in hdr

    if copy_schema_only and key_is_in_header:
        return {key: default_values[key_schema["type"]]}
    if key_is_copied and key_is_in_header:
        return {key: hdr[key]}
    if key_is_copied and not key_is_in_header and renamed_key_is_in_header:
        return {key: hdr[key_schema.get("rename")]}
    if (
        key_is_copied
        and not key_is_in_header
        and key_is_renamed
        and not renamed_key_is_in_header
        and key_is_required
    ):
        raise KeyError(f" Required keyword {key!r} not found.")
    if key_is_copied and not key_is_in_header and not key_is_renamed and key_is_required:
        raise KeyError(f" Required keyword {key!r} not found.")
    if not key_is_copied and key_is_required and key_is_in_header:
        return {key: hdr[key]}
    if not key_is_copied and key_is_required and not key_is_in_header:
        return {key: default_values[key_schema["type"]]}
    # nothing to translate
    return {}

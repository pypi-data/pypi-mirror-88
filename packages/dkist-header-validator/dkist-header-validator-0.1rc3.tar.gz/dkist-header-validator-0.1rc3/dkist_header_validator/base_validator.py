"""
Definition of the base objects for the creation of a spec validator
"""
import logging
import os
from pathlib import Path
from pathlib import PurePath
from typing import IO
from typing import List
from typing import Type
from typing import Union

import numpy as np
import voluptuous as vol
from astropy import time as t
from astropy import units as u
from astropy.io import fits
from astropy.io.fits.hdu.hdulist import HDUList
from dkist_fits_specifications import spec214
from dkist_fits_specifications.utils import expand_naxis
from numpy import ndarray

from dkist_header_validator.exceptions import SpecSchemaDefinitionException
from dkist_header_validator.exceptions import SpecValidationException
from dkist_header_validator.exceptions import ValidationException
from dkist_header_validator.translator import convert_spec122_to_spec214


logger = logging.getLogger(__name__)

__all__ = ["SpecValidator", "SpecSchema"]


class SpecSchema:
    """
    Define a schema that is used to validate FITS headers for a spec based upon structured definitions
    in YAML or dicts
    """

    # Schemas defined for a spec have the following structure per key
    definition_schema_definition = {
        vol.Required("required"): vol.Any(True, False),
        vol.Required("type"): vol.Any("int", "float", "str", "bool"),
        "values": list,
        "expected": vol.Any(True, False),
        "expand": vol.Any(True, False),
        "format": vol.Any("unit", "isot"),
    }
    # Voluptuous schema instance used to validate the definitions
    definition_schema = vol.Schema(definition_schema_definition, extra=vol.ALLOW_EXTRA)

    def __init__(self, spec_schema_definitions: Union[Path, dict, List[dict]]):
        """
        Constructor for the SpecSchema which builds a voluptuous schema from
        specification definition files in YAML or dicts
        :param spec_schema_definitions: Definition of the spec's schema in one of the following forms
            - Dict definition of the spec schema
            - List of Dict definitions of the spec schema
            - Path to a YAML file defining the spec schema
            - Path to a directory containing YAML files defining spec schema
        """
        # convert spec schema definitions to a list of dicts
        self.spec_schema_definitions = self._parse_spec_schema_definitions(spec_schema_definitions)
        # validate the dict definition of the spec schema
        self._validate_spec_schema_definitions()

    @classmethod
    def _parse_spec_schema_definitions(cls, spec_schema: List[dict]) -> dict:
        """
        Convert from a list of dicts multiple formats to a dict
        :param spec_schema: Definition(s) of the spec's schema
        :return: Dictionary capturing the spec schema definition
        """

        # Test for proper types and non-emptiness
        if spec_schema:
            if all([isinstance(item, dict) and item for item in spec_schema]):
                schema = {key: schema for item in spec_schema for (key, schema) in item.items()}
                return schema
        # empty or not a known type
        raise SpecSchemaDefinitionException(
            "Schema definition is empty or is not a supported type",
            errors={
                "received": type(spec_schema),
                "expected": List[dict],
            },
        )

    def _validate_spec_schema_definitions(self) -> None:
        """
        Validate the spec schema definitions against the class schema for
        spec schema definitions and raise a SpecSchemaDefinitionException
        on failure
        :return: None
        """

        for key, spec_schema in self.spec_schema_definitions.items():
            schema_errors = {}
            try:
                self.definition_schema(spec_schema)
            except vol.MultipleInvalid as e:
                schema_errors = {error.path[0]: error.msg for error in e.errors}
            if schema_errors:
                logger.error(
                    f"Errors during schema definition validation. key={key} errors={schema_errors}"
                )
                raise SpecSchemaDefinitionException(
                    f"Errors during schema definition validation. key={key}",
                    errors=schema_errors,
                )

    def expand_schema(self, headers) -> dict:
        """
        Expand schema indices using information from fits headers
        :param headers: Fits file headers whose values are to be used to know how to expand spec keys
        :return: schema dictionary
        """
        # 214 Expansion
        if {"DAAXES", "DEAXES", "DNAXIS"}.issubset(headers.keys()):
            # This function includes the expansion for NAXIS
            return spec214.expand_214_schema(self.spec_schema_definitions, **headers)

        # 122 Only expands "n" with NAXIS
        return expand_naxis(headers["NAXIS"], self.spec_schema_definitions)

    @staticmethod
    def generate_schema_for_key(key_schema):
        """
        Generate voluptuous schema for a key
        :param key_schema: Spec schema (from yml) used to generate voluptuous schema
        :return: Voluptuous schema for a key
        """
        type_map = {"int": int, "float": float, "str": str, "bool": bool}
        if key_schema.get("values"):
            return vol.All(type_map[key_schema.get("type")], vol.Any(*key_schema.get("values")))
        return vol.All(type_map[key_schema.get("type")])

    @staticmethod
    def _validate_units(schema: dict, headers: dict):
        """
        Validates units of headers against the spec raising
        ValueErrors upon failure.
        :param schema: Definition of the spec's schema
        :param headers: Fits file headers
        """
        for key, value in schema.items():
            if key in headers:
                if value.get("format", None) == "unit":
                    return u.Unit(headers[key], format="fits")
                if value.get("format", None) == "isot":
                    return t.Time(headers[key], format="fits")

    def _add_keys_to_schema(self, schema: dict) -> dict:
        schema_keys = {}  # keys to be added to voluptuous schema
        required_keys = {
            vol.Required(k): self.generate_schema_for_key(v)
            for k, v in schema.items()
            if v.get("required")
        }
        schema_keys.update(required_keys)
        remaining_keys = {
            k: self.generate_schema_for_key(v) for k, v in schema.items() if not v.get("required")
        }
        schema_keys.update(remaining_keys)
        return schema_keys

    def _check_for_expansion(self, headers):
        for value in self.spec_schema_definitions.values():
            # check the whole schema to see if there is an expand = True keyword
            if value["expand"]:
                # if there is an 'expand' keyword set to true in the schema, expand the whole spec schema
                expanded_schema = self.expand_schema(headers)
                return expanded_schema
        return self.spec_schema_definitions

    def _create_spec_schema(self, headers, extra) -> vol.Schema:
        """
        A voluptuous.spec_validator object to validate headers against.
        Constructed from Spec keywords.
        :param headers: Fits file headers
        :return: Voluptuous schema
        """

        spec_schema = {}

        schema = self._check_for_expansion(headers)
        self._validate_units(schema, headers)
        spec_schema.update(self._add_keys_to_schema(schema))
        if extra:
            return vol.Schema(spec_schema, extra=vol.ALLOW_EXTRA)
        return vol.Schema(spec_schema)

    def __call__(self, headers: dict, extra) -> vol.Schema:
        """
        Validate headers against the instance spec schema
        raising voluptuous errors on failure
        :param headers: header dict to validate
        :return: vol.Schema
        """
        spec_schema = self._create_spec_schema(headers, extra)
        return spec_schema(headers)


class SpecValidator:
    """
    Validates FITS Headers against a schema
    """

    def __init__(
        self,
        spec_schema: Union[Path, PurePath, dict, List[dict], SpecSchema],
        SchemaValidationException: Type[SpecValidationException] = SpecValidationException,
    ):
        """
        Constructor for the SpecValidator
        :param spec_schema: Definition of the spec's schema in one of the following forms
            - SpecSchema instance
            - Dict definition of the spec schema
            - List of Dict definitions of the spec schema
            - Path to a YAML file defining the spec schema
            - Path to a directory containing YAML files defining spec schema
        :param SchemaValidationException: SpecValidationException or subclass of SpecValidationException
            to raise if spec_validator validation fails
        """
        # Callable for validating a dict against the defined spec_validator
        if isinstance(spec_schema, SpecSchema):
            self.spec_schema = spec_schema
        else:
            self.spec_schema = SpecSchema(spec_schema)

        # Exception raised when spec validation fails
        self.SchemaValidationException = SchemaValidationException

    @staticmethod
    def _headers_to_dict(headers: Union[HDUList, dict, fits.header.Header, str, IO]) -> dict:
        """
        Convert headers from multiple types to a dict
        :param headers: Headers to convert to a dict
        :return: Dict of the headers
        """
        if isinstance(headers, dict):
            return headers
        if isinstance(headers, fits.header.Header):
            return dict(headers)
        if isinstance(headers, HDUList):
            if len(headers) > 1:
                return dict(headers[1].header)
            return dict(headers[0].header)

    def verify_headers(self, headers, extra) -> dict:
        """
        Validates file headers against the instance spec_validator
        :param headers: file headers
        :param extra: switch for validation to allow extra keys in schema
        :return: dict of headers
        :raises: SchemaValidationException
        """

        validation_errors = {}
        try:
            self.spec_schema(headers, extra)
        except vol.MultipleInvalid as e:
            validation_errors = {
                error.path[0]: f"{error.msg}. Actual value: "
                f"{headers.get(error.path[0], 'Required keyword not present')}"
                for error in e.errors
            }
        # Raise exception if we have errors
        if validation_errors:
            logger.error(f"Errors during validation: errors={validation_errors}")
            raise self.SchemaValidationException(errors=validation_errors)
        logger.debug("Schema validation succeeded")

        return headers

    def _validate_headers(
        self, input_headers: Union[HDUList, dict, fits.header.Header], extra
    ) -> dict:
        """
        Validates open input headers against the instance spec_schema
        :param input_headers: The input headers to validate in the following formats:
            - HDUList object
            - fits.header.Header object
            - Dictionary of header keys and values
        :param extra: switch for validation to allow extra keys in schema
        :return: dictionary of verified headers to be used later
        """
        headers = self._headers_to_dict(input_headers)
        verified_headers = self.verify_headers(headers, extra)
        return verified_headers

    def _validate_file(self, input_headers: Union[str, IO], extra) -> dict:
        """
        Validates files against the astropy and then instance spec_schema
        :param input_headers: The input headers to validate in the following formats:
            - string file path
            - File like object
        :param extra: switch for validation to allow extra keys in schema
        :return: dictionary of verified headers to be used later
        """
        try:
            with fits.open(input_headers, disable_image_compression=True) as hdul:
                # verify fits headers with astropy verify library
                hdul.verify("exception")
                # normalize headers into a dict
                hdus = self._headers_to_dict(hdul[0].header)
                verified_headers = self.verify_headers(hdus, extra)
                return verified_headers
        except (ValueError, FileNotFoundError, OSError, IndexError) as exc:
            logger.error(f"Cannot parse headers: detail = {exc}")
            raise ValidationException(f"Cannot parse headers", errors={type(exc): str(exc)})

    @staticmethod
    def _return_hdulist(validated_headers) -> HDUList:
        """
        Returns validated headers as an HDUList
        :param validated_headers: Already validated/translated headers to be written out into an HDUList
        :return: HDUList
        """
        if isinstance(validated_headers, HDUList):
            return validated_headers
        temp_array: ndarray = np.ones((1, 1, 1), dtype=np.int16)
        new_hdu = fits.PrimaryHDU(temp_array)
        for (key, value) in validated_headers.items():
            new_hdu.header[key] = value
        new_hdu_list = fits.HDUList([new_hdu])
        return new_hdu_list

    @staticmethod
    def _return_dictionary(validated_headers) -> dict:
        """
        Returns validated headers as a dictionary
        :param validated_headers: Already validated/translated headers to be written out into a dictionary
        :return: dictionary
        """
        return validated_headers

    @staticmethod
    def _return_file(validated_headers, input_headers) -> (str, IO):
        """
        Returns validated headers as a FITS file
        :param validated_headers: Already validated/translated headers to be written out into a FITS file
        :param input_headers: original filepath
        :return: FITS file
        """
        hdul = fits.open(input_headers, disable_image_compression=True)
        new_hdu = fits.PrimaryHDU(hdul[0].data)
        for (key, value) in validated_headers.items():
            new_hdu.header[key] = value
        new_hdu_list = fits.HDUList([new_hdu])
        new_hdu_list.writeto(
            str(os.path.basename(input_headers)),
            overwrite=True,
            output_verify="exception",
            checksum=True,
        )

    def _format_output(self, return_dict, validated_headers, input_headers=None):
        if return_dict:
            return self._return_dictionary(validated_headers)
        if isinstance(validated_headers, (dict, fits.header.Header, HDUList)):
            return self._return_hdulist(validated_headers)
        else:
            return self._return_file(validated_headers, input_headers)

    def validate(self, input_headers, return_dict=False, extra=True):
        """
        Validates against the instance spec_schema
        :param input_headers: The headers to validate in the following formats:
            - string file path
            - File like object
            - HDUList object
            - fits.header.Header object
            - Dictionary of header keys and values
        :param return_dict: switch to determine return type. If true, will return a dictionary. Default is false.
        :param extra: switch for validation to allow extra keys in schema. Default is true, which will
        allow extra keys. Ingest validation should allow extra keys.
        :return: formatted headers
        :raises: SpecValidationException or subclass
        """
        if isinstance(input_headers, (dict, fits.header.Header, HDUList)):
            validated_headers = self._validate_headers(input_headers, extra)
            return self._format_output(return_dict, validated_headers)
        else:
            validated_headers = self._validate_file(input_headers, extra)
            return self._format_output(return_dict, validated_headers, input_headers)

    def validate_and_translate(self, input_headers, return_dict=False, extra=True):
        """
        Validates against the instance spec_schema and then translates
        :param input_headers: The headers to validate in the following formats:
            - string file path
            - File like object
            - HDUList object
            - fits.header.Header object
            - Dictionary of header keys and values
        :param return_dict: switch to determine return type. If true, will return a dictionary. Default is false,
                            which will return an HDUList.
        :param extra: switch for validation to allow extra keys in schema. Default is true, which will
        allow extra keys. Ingest validation should allow extra keys.
        :return: formatted headers
        :raises: SpecValidationException or subclass
        """
        if isinstance(input_headers, (dict, fits.header.Header, HDUList)):
            validated_headers = self._validate_headers(input_headers, extra)
            translated_headers = convert_spec122_to_spec214(validated_headers)
            return self._format_output(return_dict, translated_headers)
        else:
            validated_headers = self._validate_file(input_headers, extra)
            translated_headers = convert_spec122_to_spec214(validated_headers)
            return self._format_output(return_dict, translated_headers, input_headers)

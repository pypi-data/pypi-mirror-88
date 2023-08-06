DKIST Data Validator
===========================

An interface containing a validator, and a spec translator for DKIST specs:

- SPEC-0122 Rev C: Data received from the summit

- SPEC-0214 Rev ?: Data published by the Data Center (incomplete)

Features
--------

-  Uses `voluptuous <https://pypi.org/project/voluptuous/>`__ schemas to
   validate a given input header against dkist specifications

-  3 keyword validations: type validation, required-ness validation, and value validation

-  Failure exceptions include a dictionary of validation failure causes

-  SPEC-0122 to SPEC-0214 translation


Installation
------------

.. code:: bash

   pip install dkist-header-validator


Usage
--------
Currently, this package can be used to validate SPEC122 data or SPEC214 data. Please import the
corresponding methods (spec122_validator and Spec122ValidationException, or spec214_validator, Spec214ValidationException).

This package can be used for validating data, or for validating and translating data (SPEC122 input only).

Input data can be one of:
    - string file path
    - File like object
    - HDUList object
    - fits.header.Header object
    - Dictionary of header keys and values

To validate data:

.. code:: python

    >>> from dkist_header_validator import spec122_validator, Spec122ValidationException

    >>> spec122_validator.validate('dkist_rosa0181200000_observation.fits')

To validate and translate data:

.. code:: python

    >>> from dkist_header_validator import spec122_validator, Spec122ValidationException

    >>> spec122_validator.validate_and_translate('dkist_rosa0181200000_observation.fits')

Within the validate and validate_and_translate methods, a series of flags can be set, otherwise they will take their default values:
    - extra: Default value is true (allow extra keys). This flag determines if extra keywords are allowed in the schema to be validated. Ingest validation should allow extra keys.
    - return_dict: Default value is false. If set to true, validation will return a dictionary of validated headers.


Examples
--------
1. Validate a file:

.. code:: python

    >>> from dkist_header_validator import spec122_validator, Spec122ValidationException
    >>> spec122_validator.validate('dkist_rosa0181200000_observation.fits', return_dict=True)

    2. Validate and translate a file:
    >>> spec122_validator.validate('dkist_rosa0181200000_observation.fits', return_dict=True)

2. Validate and translate a file:

.. code:: python

    >>> from dkist_header_validator import spec122_validator, Spec122ValidationException
    >>> spec122_validator.validate_and_translate('dkist_rosa0181200000_observation.fits')

    3. Validate headers:
    >>> spec122_validator.validate_and_translate('dkist_rosa0181200000_observation.fits')

3. Validate headers:

.. code:: python

    >>> from dkist_header_validator import spec122_validator, Spec122ValidationException
    >>> from astropy.io import fits
    >>> hdus = fits.open('dkist_rosa0181200000_observation.fits')
    >>> spec122_validator.validate(hdus[0].header, return_dict=True)


    This project is Copyright (c) AURA/NSO.
    >>> from astropy.io import fits
    >>> hdus = fits.open('dkist_rosa0181200000_observation.fits')
    >>> spec122_validator.validate(hdus[0].header, return_dict=True)


This project is Copyright (c) AURA/NSO.

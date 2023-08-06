from pathlib import Path

import numpy as np
import pytest
from astropy.io import fits

from dkist_header_validator.translator import convert_spec122_to_spec214


@pytest.fixture(scope="module")
def valid_spec_122_headers(tmpdir_factory):
    """
    Create a dict of valid spec 122 headers to be used in successful
    214 translator tests below.
    """
    valid_spec_122_dict = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "2KJBWEFB4OUUBSFUIB5JKBSDF8JBSK",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
    }

    temp_dir = tmpdir_factory.mktemp("valid spec_122_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu = fits.PrimaryHDU(temp_array)
    # Use the valid_spec_122_dict from above to overwrite the default header
    for (key, value) in valid_spec_122_dict.items():
        valid_hdu.header[key] = value
    valid_hdu_list = fits.HDUList([valid_hdu])
    valid_hdu_list.writeto(str(file_name))

    yield {
        "valid_dkist_hdr.fits": Path(file_name),
        "valid_spec_122_dict": valid_spec_122_dict,
        "valid_HDUList": valid_hdu_list,
        "valid header": valid_hdu.header,
    }


@pytest.fixture(
    scope="function",
    params=[
        "valid_dkist_hdr.fits",
        "valid_spec_122_dict",
        "valid_HDUList",
        "valid header",
    ],
)
def valid_spec_122_header(request, valid_spec_122_headers):
    yield valid_spec_122_headers[request.param]


def test_spec122_valid(valid_spec_122_header):
    """
    Translates a SPEC-0122 object to a SPEC-214 object
    Given: A valid SPEC-0122 object
    When: Translating headers
    Then: For a fits file input, return a HDUList and do not raise an exception
          For a dict, HDUList, or header input, return a dictionary and do not raise an exception
    """
    convert_spec122_to_spec214(valid_spec_122_header)


@pytest.fixture(scope="module")
def spec_122_headers_missing_required_keys(tmpdir_factory):
    """
    Create a dict of invalid spec 122 headers missing required
    keys to be used in failing 214 translator tests below.
    """
    spec_122_dict_missing_required_keys = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
    }

    temp_dir = tmpdir_factory.mktemp("spec_122_headers_missing_required_keys_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    missing_required_keys_hdu = fits.PrimaryHDU(temp_array)
    # Use the spec_122_dict_missing_required_keys from above to overwrite the default header
    for (key, value) in spec_122_dict_missing_required_keys.items():
        missing_required_keys_hdu.header[key] = value
    missing_required_keys_hdu_list = fits.HDUList([missing_required_keys_hdu])
    missing_required_keys_hdu_list.writeto(str(file_name))

    yield {
        "missing_required_keys_hdr.fits": Path(file_name),
        "spec_122_dict_missing_required_keys": spec_122_dict_missing_required_keys,
        "missing_required_keys_HDUList": missing_required_keys_hdu_list,
        "missing_required_keys header": missing_required_keys_hdu.header,
    }


@pytest.fixture(
    scope="function",
    params=[
        "missing_required_keys_hdr.fits",
        "spec_122_dict_missing_required_keys",
        "missing_required_keys_HDUList",
        "missing_required_keys header",
    ],
)
def missing_required_keys_spec_122_header(request, spec_122_headers_missing_required_keys):
    yield spec_122_headers_missing_required_keys[request.param]


def test_spec122_missing_required_keys(missing_required_keys_spec_122_header):
    """
    Translates an invalid SPEC-0122 object missing required
    keys to a SPEC-214 object
    Given: A valid SPEC-0122 object
    When: Translating headers
    Then: Raises a KeyError exception
    """
    with pytest.raises(KeyError):
        convert_spec122_to_spec214(missing_required_keys_spec_122_header)


@pytest.fixture(scope="module")
def max_headers(tmpdir_factory):
    headers = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "2KJBWEFB4OUUBSFUIB5JKBSDF8JBSK",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
        "SIMPLE": True,
        "BZERO": 0.0,
        "BSCALE": 1.0,
        "OBSERVER": "8QN27LDFC7EQHKK4B3WDIN4FY7VG16",
        "CRDATE1": "2035-03-31T09:38:56.668",
        "CRDATE2": "2035-03-31T09:38:56.668",
        "LONPOLE": 180.0,
        "TAZIMUTH": 618993.1279034158,
        "TELEVATN": 819.9173809486648,
        "TELTRACK": "Standard Differential Rotation Tracking",
        "TELSCAN": "Raster",
        "TTBLANGL": 295548.0744481586,
        "TTBLTRCK": "fixed coude table angle",
        "DKIST001": "Manual",
        "DKIST002": "Full",
        "DKIST005": "9CVKTL2JWMH1LHU6G3O2UPE2SO9SUW",
        "DKIST006": "OG4Y0R39WGGB3N0R7VIDQG7VQYD79N",
        "DKIST007": False,
        "DKIST008": 999562,
        "DKIST009": 5750,
        "DKIST010": 295882,
        "ID___001": "73QYTMXIMDLCNZUEBELYY6TZ8QGYKV",
        "ID___003": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "ID___004": "MY50PNI7QUGSKLW5D8XB9N4SDKFDZ4",
        "ID___005": "59ULPBE5GG9S93M9IG63FCWMV63WAD",
        "ID___006": "7VWWG70RLGVD9AC1J9X6Y937EJIQNV",
        "ID___007": "U8M3EWALJLU5F5B96WB4QL3SN0Z1C8",
        "ID___009": "XV64I6WTJEJ93202Z5ZJ15MDBBBPRE",
        "ID___010": "KKWSIWJD2NKL11J03X51ZZR0C6FSHG",
        "ID___011": "OB6PYAI9XC3PTXLLY4I1LV26RTDEGS",
        "ID___014": "UX4QYSNNFC1O99JD3TVPAGUU4XR0JB",
        "CAM__001": "ODJIY4RO6SG7T6YVHT4QVNJPVYGQW7",
        "CAM__002": "JRA5H1LSKENNLLWUZNHW9X93Z9J6G0",
        "CAM__003": 206077,
        "CAM__004": 553109.1055738949,
        "CAM__005": 931934.0145101176,
        "CAM__006": 336899.9459380526,
        "CAM__007": 450499,
        "CAM__008": 105605,
        "CAM__009": 278167,
        "CAM__010": 45681,
        "CAM__011": 882899,
        "CAM__012": 849283,
        "CAM__013": 191847,
        "CAM__014": 859469,
        "CAM__015": 208276,
        "CAM__016": 71858,
        "CAM__017": 540083,
        "CAM__018": 462616,
        "CAM__019": 763903,
        "CAM__020": 626497,
        "PAC__001": "I0ZJXRV29HDPUM2NB1P8YWXC2U6ZPN",
        "PAC__002": "LCEN78S9ZFFD54FT7W4IQRZ53DVOHO",
        "PAC__003": "08DT3NZOX1XC4U6KT462GIMJ1KH9R1",
        "PAC__004": "Clear",
        "PAC__005": "186BGJFTFDVEOECZ80ENVCKM5RZL4U",
        "PAC__006": "NIRRetarder",
        "PAC__007": "some string",
        "PAC__008": 332880.8796027036,
        "PAC__009": 39391.69758352268,
        "PAC__010": "Undefined",
        "PAC__011": 228814.6368968824,
        "WS___001": "CYWKXJOAROTHYHNBZOD8Z7VGJITI23",
        "WS___002": 516056.5759472652,
        "WS___003": 188143,
        "WS___004": 943419.0784243871,
        "WS___005": 282679.0410177523,
        "WS___006": 348537.5489154414,
        "WS___007": 870761.4045310392,
    }

    temp_dir = tmpdir_factory.mktemp("max_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu = fits.PrimaryHDU(temp_array)
    # Use the valid_header dict from above to overwrite the default header
    for (key, value) in headers.items():
        valid_hdu.header[key] = value
    valid_hdu_list = fits.HDUList([valid_hdu])
    valid_hdu_list.writeto(str(file_name))

    yield Path(str(file_name))


def test_translate_maxheaders(max_headers):
    """
    Translates a SPEC-0122 object with a large number of keywords
    to a SPEC-214 object and validates output against the SPEC-214 schema
    Given: A valid SPEC-0122 object with many header keywords
    When: Translating headers
    Then: For a fits file input, return a HDUList and do not raise an exception
          For a dict, HDUList, or header input, return a dictionary and do not raise an exception
    """

    convert_spec122_to_spec214(max_headers)


@pytest.fixture(scope="module")
def valid_compressed_spec_122_headers(tmpdir_factory):
    """
    Create a dict of valid spec 122 headers to be
    written to a compressed fits file and used in
    successful 214 translator tests below.
    """
    valid_comp_122_dict = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "2KJBWEFB4OUUBSFUIB5JKBSDF8JBSK",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
    }

    temp_dir = tmpdir_factory.mktemp("valid comp_122_headers_temp")
    file_name = temp_dir.join("tmp__comp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_comp_hdu = fits.PrimaryHDU(temp_array)
    # Use the valid_spec_122_dict from above to overwrite the default header
    for (key, value) in valid_comp_122_dict.items():
        valid_comp_hdu.header[key] = value
    valid_comp_hdu_list = fits.HDUList([valid_comp_hdu])
    valid_comp_hdu_list.writeto(str(file_name))

    yield {
        "valid_compressed_hdr.fits.fz": Path(file_name),
    }


@pytest.fixture(
    scope="function",
    params=[
        "valid_compressed_hdr.fits.fz",
    ],
)
def valid_compressed_spec_122_header(request, valid_compressed_spec_122_headers):
    yield valid_compressed_spec_122_headers[request.param]


def test_compressed_spec122_valid(valid_compressed_spec_122_header):
    """
    Translates a compressed SPEC-0122 object to a SPEC-214 object
    Given: A valid compressed SPEC-0122 file
    When: Translating headers
    Then: Return a HDUList and do not raise an exception
    """
    convert_spec122_to_spec214(valid_compressed_spec_122_header)


@pytest.fixture(scope="module")
def compressed_spec_122_headers_missing_required_keys(tmpdir_factory):
    """
    Create a dict of valid spec 122 headers to be
    written to a compressed fits file and used in
    successful 214 translator tests below.
    """
    comp_122_dict_missing_required_keys = {
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
    }

    temp_dir = tmpdir_factory.mktemp("comp_122_headers_missing_required_keys_temp")
    file_name = temp_dir.join("tmp__comp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    missing_required_keys_comp_hdu = fits.PrimaryHDU(temp_array)
    for (key, value) in comp_122_dict_missing_required_keys.items():
        missing_required_keys_comp_hdu.header[key] = value
    missing_required_keys_comp_hdu_list = fits.HDUList([missing_required_keys_comp_hdu])
    missing_required_keys_comp_hdu_list.writeto(str(file_name))

    yield {
        "missing_required_keys_compressed_hdr.fits.fz": Path(file_name),
    }


@pytest.fixture(
    scope="function",
    params=[
        "missing_required_keys_compressed_hdr.fits.fz",
    ],
)
def compressed_spec_122_header_missing_required_keys(
    request, compressed_spec_122_headers_missing_required_keys
):
    yield compressed_spec_122_headers_missing_required_keys[request.param]


def test_compressed_spec122_missing_required_keys(compressed_spec_122_header_missing_required_keys):
    """
    Translates a compressed SPEC-0122 object which is
    missing required keys to a SPEC-214 object
    Given: A valid compressed SPEC-0122 file
    When: Translating headers
    Then: Raises a KeyError exception
    """
    with pytest.raises(KeyError):
        convert_spec122_to_spec214(compressed_spec_122_header_missing_required_keys)

import pytest

from xkoranate.exceptions import XkorFileNotFoundException, XkorSearchFailedException


def test_file_not_found_exception_carries_type_and_name():
    exc = XkorFileNotFoundException("boom", "sport directory", "/some/path")
    assert str(exc) == "boom"
    assert exc.fileType() == "sport directory"
    assert exc.fileName() == "/some/path"


def test_file_not_found_exception_is_raisable():
    with pytest.raises(XkorFileNotFoundException) as excinfo:
        raise XkorFileNotFoundException("missing", "sport", "x.xml")
    assert excinfo.value.fileName() == "x.xml"


def test_search_failed_exception_is_raisable():
    with pytest.raises(XkorSearchFailedException):
        raise XkorSearchFailedException("not found")

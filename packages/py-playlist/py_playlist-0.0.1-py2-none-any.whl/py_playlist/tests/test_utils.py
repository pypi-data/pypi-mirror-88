import py_playlist.utils as utils


def test_version_defined():
    assert utils.__version__ is not None


def test_expand_path():
    assert utils.expand_path('~') != '~'

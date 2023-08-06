import py_playlist.logs as logs


def test_function_decorator():
    @logs.log_function
    def dummy(param):
        return param

    dummy(1)

    assert True  # no exceptions


def test_generator_decorator():
    @logs.log_generator
    def dummy(param):
        yield param

    dummy(1)

    assert True  # no exceptions

from app.reliability.errors import AppError, InvalidInputError


def test_invalid_input_error_is_app_error():
    err = InvalidInputError("bad input")
    assert isinstance(err, AppError)
    assert err.code == "INVALID_INPUT"

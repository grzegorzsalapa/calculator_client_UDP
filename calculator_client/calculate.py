from .UDP_client import get_result, CommunicationError


class CalculationError(Exception):
    def __init__(self, message: str):
        self.message = message


class RemoteCalculationError(Exception):
    pass


def _check_if_error_returned(str_to_check):
    try:
        float(str_to_check)
    except Exception:
        error_message = str_to_check
        raise RemoteCalculationError(error_message)


def calculate(expression: str, server_address: str):
    try:
        result = get_result(expression, server_address)
        _check_if_error_returned(result)

        return result

    except RemoteCalculationError as e:

        raise CalculationError(str(e))

    except CommunicationError as e:

        raise CalculationError(str(e))

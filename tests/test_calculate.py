from unittest.mock import MagicMock, patch
from calculator_client.calculate import calculate, CalculationError
import pytest


def _set_up_mocked_calculator_socket(recv_value=None):
    socket_instance = MagicMock(name="SocketInstance")
    socket_instance.recv = MagicMock(return_value=recv_value)
    socket_instance.sendto = MagicMock()

    socket_context = MagicMock(name="SocketContext")
    socket_context.__enter__ = MagicMock(return_value=socket_instance)

    socket_mock = MagicMock()
    socket_mock.socket = MagicMock(name="SocketModule", return_value=socket_context)

    return socket_mock


def test_that_received_result_on_socket_is_passed_properly_as_a_result_to_calculate():
    socket_mock = _set_up_mocked_calculator_socket(recv_value=b'6')

    with patch('calculator_client.UDP_client.socket', new=socket_mock):
        assert calculate('2+2*2', '') == '6'


def test_that_correct_binary_representation_of_expression_is_sent_on_socket():
    socket_mock = _set_up_mocked_calculator_socket(recv_value=b'6')

    with patch('calculator_client.UDP_client.socket', new=socket_mock):
        calculate('(2+2)*5/7-3+sde', '')
        socket_mock.socket().__enter__().sendto.assert_called_once_with(b'(2+2)*5/7-3+sde', ('', 9011))


def test_that_server_address_is_passed_to_socket():
    socket_mock = _set_up_mocked_calculator_socket(recv_value=b'6')

    with patch('calculator_client.UDP_client.socket', new=socket_mock):
        calculate('2+2', '127.0.0.1')
        socket_mock.socket().__enter__().sendto.assert_called_once_with(b'2+2', ('127.0.0.1', 9011))


def test_that_returned_error_message_is_converted_to_exception():
    socket_mock = _set_up_mocked_calculator_socket(recv_value=b'Example error message.')

    with pytest.raises(CalculationError, match=r"Example error message."):
        with patch('calculator_client.UDP_client.socket', new=socket_mock):
            calculate('any_expression', 'any_address')

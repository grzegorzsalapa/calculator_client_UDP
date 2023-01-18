import socket


class CommunicationError(Exception):
    def __init__(self, message):
        self.message = message


PORT = 9011


def get_result(expression: str, server_address: str):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            expressionb = bytes(expression, 'utf-8')
            s.sendto(expressionb, (server_address, PORT))
            resultb = s.recv(1024)
            response = str(resultb)[2:][:-1]
    except Exception as e:
        raise CommunicationError(str(e))
    return response

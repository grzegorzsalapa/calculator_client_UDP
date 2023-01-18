from calculator_client import calculate, CalculationError


def main():
    try:
        server_address = _ask_for_server_address()
        while True:
            expression = _ask_for_expression()

            try:
                result = calculate(expression, server_address)

            except CalculationError as e:
                print(str(e), "\n")

            else:
                print(result, "\n")

    except KeyboardInterrupt:
        print("\rBye")


def _ask_for_server_address():
    server_address = input("Provide calculation server address:\n")
    print('')
    return server_address


def _ask_for_expression():
    expression = input("Provide simple math expression and press enter, "
                       "only integers allowed:\n")
    return expression


if __name__ == "__main__":
    main()

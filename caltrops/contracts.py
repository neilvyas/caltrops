from exceptions import InputContractError, OutputContractError


class input_output_contract:
    def __init__(self, input_contract, output_contract):
        self.input_contract = input_contract
        self.output_contract = output_contract

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            try:
                self.input_contract(*args, **kwargs)
            except AssertionError as e:
                raise InputContractError(e.message)

            output = f(*args, **kwargs)

            try:
                self.output_contract(output)
            except AssertionError as e:
                raise OutputContractError(e.message)

            return output
        return wrapped


def null_contract(*args, **kwargs):
    return


def input_contract(input_contract):
    return input_output_contract(input_contract, null_contract)


def output_contract(output_contract):
    return input_output_contract(null_contract, output_contract)


def all_contracts(*contracts):
    """Run a list of contracts in order.

    Note: this function is especially helpful because decorators make
    the order of evaluation a little less obvious.
    """
    def contract_(*args, **kwargs):
        for contract in contracts:
            contract(*args, **kwargs)
    return contract_


def any_contract(*contracts):
    """Try a list of contracts in order and pass if any of them pass.

    If none pass, raise an exception of the same type as the inputs
    (InputContractError/OutputContractError) with all messages
    concatenated.

    I don't really know /why/ you'd want this, maybe if your function
    has branching behavior but you only need at least one branch?
    You should consider refactoring.

    You can, of course, compose any_contract and all_contracts for
    really convoluted contracts (they are "or" and "and", respectively.)
    """
    def contract_(*args, **kwargs):
        messages = []
        for contract in contracts:
            try:
                contract(*args, **kwargs)
            except AssertionError as e:
                messages.append(e.message)
        else:
            message = "\n".join(messages)
            raise type(e)(message)
    return contract_

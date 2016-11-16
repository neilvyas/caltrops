from exceptions import InputContractError, OutputContractError


class input_contract:
    def __init__(self, contract):
        self.contract = contract

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            try:
                self.contract(*args, **kwargs)
            except AssertionError as e:
                raise InputContractError(e.message)
            return f(*args, **kwargs)
        return wrapped


class output_contract:
    def __init__(self, contract):
        self.contract = contract

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            output = f(*args, **kwargs)
            try:
                self.contract(output)
            except AssertionError as e:
                raise OutputContractError(e.message)
            return output
        return wrapped


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

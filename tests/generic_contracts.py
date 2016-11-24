from caltrops import (input_contract, output_contract, all_contracts, exception_wrapper,
                      Error)


class Errors:
    InputContractError = 'InputContractError'
    OutputContractError = 'OutputContractError'

    NUM_TYPE = "num isn't an int."
    STR_TYPE = "string_ isn't a string."
    MULTIPLIER_TYPE = "multiplier isn't an int."
    MULTIPLIER_SIZE = 'multiplier is too small.'
    OUTPUT_TYPE = 'output is not a string.'


def string_is_always_str(string_, num_, **kwargs):
    assert isinstance(string_, str), Errors.STR_TYPE


def num_is_always_int(string_, num_, **kwargs):
    assert isinstance(num_, int), Errors.NUM_TYPE


def multiplier_ge_1(*args, **kwargs):
    multiplier = kwargs.get('multiplier')
    if multiplier is not None:
        assert isinstance(multiplier, int), Errors.MULTIPLIER_TYPE
        assert multiplier >= 1, Errors.MULTIPLIER_SIZE


def output_is_always_str(output):
    assert isinstance(output, str), Errors.OUTPUT_TYPE


@exception_wrapper
@output_contract(output_is_always_str)
@input_contract(all_contracts(
    string_is_always_str,
    num_is_always_int,
    multiplier_ge_1,
))
def arbitrary_computation(string_, num_, multiplier=1):
    # Get the output contract to fire.
    if num_ == 6:
        return 6

    return string_ + str(num_) * multiplier

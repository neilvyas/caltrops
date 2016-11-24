from caltrops import (input_contract, output_contract, all_contracts, exception_wrapper,
                      Error)
import unittest


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


class ExampleGuardedFunction(unittest.TestCase):
    def _parameterized_test(self, inputs, expected_output):
        if len(inputs) == 3:
            string_, num_, multiplier = inputs
            res = arbitrary_computation(string_, num_, multiplier=multiplier)
        else:
            string_, num_ = inputs
            res = arbitrary_computation(string_, num_)

        self.assertEqual(res, expected_output)

    def test__contracts_pass(self):
        self._parameterized_test(("a", 5), "a5")

    def test__num_type(self):
        self._parameterized_test(
            ("a", "a"),
            Error(Errors.InputContractError, Errors.NUM_TYPE),
        )

    def test__string_type_and_short_circuiting_order(self):
        """This test case covers little more than one thing, thanks to how we defined
        arbitrary_computation. In particular, we test that

        1. all_contracts runs the contracts in the order they were given, so the string
        input contract runs first and short-circuits.

        2. the string input contract actually functions as desired.
        """
        self._parameterized_test(
            (6, "a"),
            Error(Errors.InputContractError, Errors.STR_TYPE),
        )

    def test__multiplier_type(self):
        self._parameterized_test(
            ("a", 5, "six "),
            Error(Errors.InputContractError, Errors.MULTIPLIER_TYPE)
        )

    def test__multiplier_size(self):
        self._parameterized_test(
            ("a", 5, -1),
            Error(Errors.InputContractError, Errors.MULTIPLIER_SIZE)
        )

    def test__output_type(self):
        self._parameterized_test(
            ("a", 6),
            Error(Errors.OutputContractError, Errors.OUTPUT_TYPE)
        )


if __name__ == "__main__":
    unittest.main()

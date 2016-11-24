from caltrops import Error
from generic_contracts import arbitrary_computation
from generic_contracts import Errors


class TestExampleGuardedFunction:
    def _parameterized_test(self, inputs, expected_output):
        if len(inputs) == 3:
            string_, num_, multiplier = inputs
            res = arbitrary_computation(string_, num_, multiplier=multiplier)
        else:
            string_, num_ = inputs
            res = arbitrary_computation(string_, num_)

        assert res == expected_output

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

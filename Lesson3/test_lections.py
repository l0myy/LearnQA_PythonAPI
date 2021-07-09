class TestExample:
    def test_check_math(self):
        a = 5
        b = 9
        assert a + b == 14

    def test_check_math2(self):
        a = 5
        b = 9
        expected_sum = 11
        assert a + b == expected_sum, f"Sum of variable a and b is not equal to {expected_sum}"


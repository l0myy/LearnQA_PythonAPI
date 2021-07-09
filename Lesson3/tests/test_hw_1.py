
class TestHomeWork1:
    def test_length_of_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) <= 15, f"Your phrase longer then 15 symbols."

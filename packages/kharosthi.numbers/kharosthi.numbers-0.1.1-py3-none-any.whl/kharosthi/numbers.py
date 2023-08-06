import re
from typing import List, SupportsInt


class KharosthiNumber:

    int_to_kharosthi = {
        1: "𐩀",
        2: "𐩁",
        3: "𐩂",
        4: "𐩃",
        10: "𐩄",
        20: "𐩅",
        100: "𐩆",
        1000: "𐩇",
    }

    kharosthi_to_int = dict((v, k) for k, v in int_to_kharosthi.items())

    valid_regex = re.compile(r"[^𐩀𐩁𐩂𐩃𐩄𐩅𐩆𐩇]")

    number: str
    int_number: int

    def __init__(self, number: str) -> None:
        self.validate(number)
        self.number = number
        self.int_number = self._kharosthi_to_int(number)

    def validate(self, number: str):
        # check that the number is a string and only contains valid digits
        if not type(number) is str:
            raise ValueError("Invalid input: Not a string")

        # check that it only contains valid characters
        # solution found here: https://stackoverflow.com/a/1325265/306458
        if bool(self.valid_regex.search(number)):
            raise ValueError("Invalid input: Contains invalid characters")

    @classmethod
    def _int_to_kharosthi(cls, number: int) -> str:
        result = ""

        # TODO: Calculate!
        # Find the biggest kharosthi common divisor(?)
        while number > 0:
            khar = cls.int_to_kharosthi.get(number)
            if khar:
                result += khar
                break

            gcd = 4  # start at 4, since all numbers 4 or below are directly representable with a kharosthi digit
            for key in cls.int_to_kharosthi.keys():
                if key < number:
                    gcd = key
                    continue
                break

            quotitient, remainder = divmod(number, gcd)
            if gcd >= 100 and quotitient > 1:
                result += cls._int_to_kharosthi(quotitient) + cls.int_to_kharosthi[gcd]
            else:
                result += cls.int_to_kharosthi[gcd] * quotitient
            number = remainder

        if result:
            return result

        # we can't convert this number
        raise ValueError("Input can't be converted to a Kharosthi number")

    def _kharosthi_to_int(self, number: str) -> int:
        result = 0
        # convert to list of ints
        int_list = [self.kharosthi_to_int[x] for x in number]

        singles: List[int] = []
        hundreds: List[int] = []
        hundreds_present = 0
        thousands: List[int] = []
        thousands_present = 0
        bucket = singles
        while len(int_list):
            x = int_list.pop()
            if x == 100:
                bucket = hundreds
                if hundreds_present == 100:
                    raise ValueError("Invalid Kharosthi representation")
                hundreds_present = 100
            elif x == 1000:
                bucket = thousands
                if thousands_present == 1000:
                    raise ValueError("Invalid Kharosthi representation")
                thousands_present = 1000
            else:
                bucket.append(x)

        singles_sum = sum(singles)
        if singles_sum >= 100:
            raise ValueError("Invalid Kharosthi representation")
        hundreds_sum = sum(hundreds) * 100 if len(hundreds) else hundreds_present
        if hundreds_sum >= 1000:
            raise ValueError("Invalid Kharosthi representation")
        thousands_sum = sum(thousands) * 1000 if len(thousands) else thousands_present
        if thousands_sum >= 10000:
            raise ValueError(
                "Invalid Kharosthi representation. Max representable number is 9999"
            )

        result = singles_sum + hundreds_sum + thousands_sum

        if result == 0:
            raise ValueError("Can't be converted to an int")
        return result

    def __str__(self) -> str:
        return self.number

    def __int__(self) -> int:
        return self.int_number

    def __add__(self, other):
        return self.__class__.from_int(self.int_number + int(other))

    def __sub__(self, other):
        return self.__class__.from_int(self.int_number - int(other))

    def __eq__(self, o: object) -> bool:
        if hasattr(o, "__int__"):
            return self.int_number == int(o)  # type: ignore

        return False

    @classmethod
    def from_int(cls, int_number: int):
        return cls(cls._int_to_kharosthi(int_number))

    def to_int(self) -> int:
        return self._kharosthi_to_int(self.number)

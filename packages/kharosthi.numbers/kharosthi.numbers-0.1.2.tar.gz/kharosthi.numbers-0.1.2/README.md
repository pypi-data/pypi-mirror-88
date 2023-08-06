# Kharosthi numbers
A naive representation of Kharosthi numerals, and a way to do simple arithmetic on them (actually, we're cheating and doing arithmetic on `int` versions of the numbers).

Currently only supports numbers less than 10000. The naive conversion algorithm currently can't deal with arbitrarily big numbers, so we only support "𐩇" with a maximum value of 9 in front of it.

Also, 0 and negative integers are not representable in Kharosthi, and not valid numbers.

## Requirements
Python >= 3.6

## Usage
```python
from kharosthi.numbers import KharosthiNumber as K

sum = K.from_int(5) + K.from_int(50)

# 7 - 4 = 3
int(difference) = K("𐩃𐩂") - K("𐩃")
```

Reference: https://en.wikipedia.org/wiki/Kharosthi#Numerals

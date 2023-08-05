# Decimal to doubleword

This package contains a function to easily generate the values
assigned to bytes 19 - 22 when using the Modbus TCP on the
Igus Dryve D1 controller.

## How to use

Import with:

```python
from decimaldoubleword import ddConverter as conv
```

Now calling conv() with a decimal argument returns a correctly
formatted list in the shape of (Byte 19, Byte 20, Byte 21, Byte 22)

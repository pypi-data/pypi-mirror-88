"""Function to convert a decimal integer to four byte doubleword"""

__version__ = '1.0.0'

def ddConverter(decimalInput):
    '''
    Takes a decimal integer and returns a list of decimal byte values\n
    100 -> 0000.0000.0000.0000.0000.0000.0110.0100 -> Byte22=0, Byte21=0, Byte20=0, Byte19=100\n
    List is inverted for simplicity reasons: Byte19 = Index[0], Byte20 = Index[1] etc...
    '''
    if decimalInput < 0:
        isNegativFlag = True
    else:
        isNegativFlag = False
    
    byteDecimal = bin(decimalInput)
    
    # pad with zeros to fill 4 bytes
    if isNegativFlag:
        fourByteDecimal = str(byteDecimal[3:]).zfill(32)
    else:
        fourByteDecimal = str(byteDecimal[2:]).zfill(32)
    
    # seperate in four bytes
    if isNegativFlag:
        byte22 = 255 - int(fourByteDecimal[:8], 2)
        byte21 = 255 - int(fourByteDecimal[9:16], 2)
        byte20 = 255 - int(fourByteDecimal[17:24], 2)
        byte19 = 256 - int(fourByteDecimal[24:], 2)
    else:
        byte22 = int(fourByteDecimal[:8], 2)
        byte21 = int(fourByteDecimal[9:16], 2)
        byte20 = int(fourByteDecimal[17:24], 2)
        byte19 = int(fourByteDecimal[24:], 2)
    
    decimalList = (byte19, byte20, byte21, byte22)
        
    return decimalList
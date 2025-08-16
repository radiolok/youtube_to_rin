"""
    Python Character Mapping Codec koi7_n1.
    Written by Artem Kashkanov(@radiolok).
    Edited by Mihail Serebryakov(@simsanutiy).
"""

import codecs

### Codec APIs

class Codec(codecs.Codec):

    def encode(self,input,errors='strict'):
        return codecs.charmap_encode(input,errors,encoding_table)

    def decode(self,input,errors='strict'):
        return codecs.charmap_decode(input,errors,decoding_table)

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input,self.errors,encoding_table)[0]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return codecs.charmap_decode(input,self.errors,decoding_table)[0]

class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

### encodings module API

def getregentry():
    return codecs.CodecInfo(
        name='koi7-n1',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )


### Decoding Table

decoding_table = (
    '\x00'     #  0x00 -> NULL
    '\x00'     #  0x01 -> START OF HEADING
    'ш'     #  0x02 -> START OF TEXT
    '\x00'     #  0x03 -> END OF TEXT
    '\x00'     #  0x04 -> END OF TRANSMISSION
    '\x00'     #  0x05 -> ENQUIRY
    '\x00'     #  0x06 -> ACKNOWLEDGE
    '\x07'     #*  0x07 -> звонок
    '\x08'     #*  0x08 -> возврат на шаг
    '\t'       #*  0x09 -> HORIZONTAL TABULATION
    '\n'       #*  0x0A -> перевод строки
    '\x00'     #*  0x0B -> VERTICAL TABULATION
    '\x00'     #*  0x0C -> FORM FEED
    '\r'       #  0x0D -> CARRIAGE RETURN
    '\x00'     #  0x0E -> SHIFT OUT
    '\x00'     #  0x0F -> SHIFT IN
    '\x00'     #  0x10 -> DATA LINK ESCAPE
    '\x00'     #  0x11 -> DEVICE CONTROL ONE
    '\x00'     #  0x12 -> DEVICE CONTROL TWO
    '\x00'     #  0x13 -> DEVICE CONTROL THREE
    '\x00'     #  0x14 -> DEVICE CONTROL FOUR
    '\x00'     #  0x15 -> NEGATIVE ACKNOWLEDGE
    '\x00'     #  0x16 -> SYNCHRONOUS IDLE
    '\x00'     #  0x17 -> END OF TRANSMISSION BLOCK
    '\x00'     #  0x18 -> CANCEL
    '\x00'     #  0x19 -> END OF MEDIUM
    '\x00'     #  0x1A -> SUBSTITUTE
    '\x00'     #  0x1B -> ESCAPE
    '\x00'     #  0x1C -> FILE SEPARATOR
    '\x00'     #  0x1D -> GROUP SEPARATOR
    '\x00'     #  0x1E -> RECORD SEPARATOR
    '\x00'     #  0x1F -> UNIT SEPARATOR
    ' '        #*  0x20 -> SPACE
    '!'        #*  0x21 -> EXCLAMATION MARK
    '"'        #*  0x22 -> QUOTATION MARK
    '#'        #*  0x23 -> NUMBER SIGN
    'Ч'        #*  0x24 -> CURRENCY SIGN
    '%'        #*  0x25 -> PERCENT SIGN
    'Ъ'        #*  0x26 -> AMPERSAND
    "ъ"        #*  0x27 -> APOSTROPHE
    '('        #*  0x28 -> LEFT PARENTHESIS
    ')'        #*  0x29 -> RIGHT PARENTHESIS
    '?'        #*  0x2A -> ASTERISK
    '+'        #*  0x2B -> PLUS SIGN
    ','        #*  0x2C -> COMMA
    '-'        #*  0x2D -> HYPHEN-MINUS
    '.'        #*  0x2E -> FULL STOP
    '/'        #*  0x2F -> SOLIDUS
    '0'        #*  0x30 -> DIGIT ZERO
    '1'        #*  0x31 -> DIGIT ONE
    '2'        #*  0x32 -> DIGIT TWO
    '3'        #*  0x33 -> DIGIT THREE
    '4'        #*  0x34 -> DIGIT FOUR
    '5'        #*  0x35 -> DIGIT FIVE
    '6'        #*  0x36 -> DIGIT SIX
    '7'        #*  0x37 -> DIGIT SEVEN
    '8'        #*  0x38 -> DIGIT EIGHT
    '9'        #*  0x39 -> DIGIT NINE
    ':'        #*  0x3A -> COLON
    ';'        #*  0x3B -> SEMICOLON
    '<'        #*  0x3C -> LESS-THAN SIGN
    '='        #*  0x3D -> EQUALS SIGN
    '>'        #*  0x3E -> GREATER-THAN SIGN
    '?'        #*  0x3F -> QUESTION MARK
    'Ю'        #*  0x40 -> COMMERCIAL AT
    'А'        #*  0x41 -> LATIN CAPITAL LETTER A
    'Б'        #*  0x42 -> LATIN CAPITAL LETTER B
    'Ц'        #*  0x43 -> LATIN CAPITAL LETTER C
    'Д'        #*  0x44 -> LATIN CAPITAL LETTER D
    'Е'        #*  0x45 -> LATIN CAPITAL LETTER E
    'Ф'        #*  0x46 -> LATIN CAPITAL LETTER F
    'Г'        #*  0x47 -> LATIN CAPITAL LETTER G
    'Х'        #*  0x48 -> LATIN CAPITAL LETTER H
    'И'        #*  0x49 -> LATIN CAPITAL LETTER I
    'Й'        #*  0x4A -> LATIN CAPITAL LETTER J
    'К'        #*  0x4B -> LATIN CAPITAL LETTER K
    'Л'        #*  0x4C -> LATIN CAPITAL LETTER L
    'М'        #*  0x4D -> LATIN CAPITAL LETTER M
    'Н'        #*  0x4E -> LATIN CAPITAL LETTER N
    'О'        #*  0x4F -> LATIN CAPITAL LETTER O
    'П'        #*  0x50 -> LATIN CAPITAL LETTER P
    'Я'        #*  0x51 -> LATIN CAPITAL LETTER Q
    'Р'        #*  0x52 -> LATIN CAPITAL LETTER R
    'С'        #*  0x53 -> LATIN CAPITAL LETTER S
    'Т'        #*  0x54 -> LATIN CAPITAL LETTER T
    'У'        #*  0x55 -> LATIN CAPITAL LETTER U
    'Ж'        #*  0x56 -> LATIN CAPITAL LETTER V
    'В'        #*  0x57 -> LATIN CAPITAL LETTER W
    'Ь'        #*  0x58 -> LATIN CAPITAL LETTER X
    'Ы'        #*  0x59 -> LATIN CAPITAL LETTER Y
    'З'        #*  0x5A -> LATIN CAPITAL LETTER Z
    'Ш'        #*  0x5B -> LEFT SQUARE BRACKET
    'Э'       #*  0x5C -> REVERSE SOLIDUS
    'Щ'        #*  0x5D -> RIGHT SQUARE BRACKET
    '^'        #*  0x5E -> CIRCUMFLEX ACCENT
    '_'        #*  0x5F -> LOW LINE
    'ю'   #*  0x60 -> CYRILLIC CAPITAL LETTER YU
    'а'   #*  0x61 -> CYRILLIC CAPITAL LETTER A
    'б'   #*  0x62 -> CYRILLIC CAPITAL LETTER BE
    'ц'   #*  0x63 -> CYRILLIC CAPITAL LETTER TSE
    'д'   #*  0x64 -> CYRILLIC CAPITAL LETTER DE
    'е'   #*  0x65 -> CYRILLIC CAPITAL LETTER IE
    'ф'   #*  0x66 -> CYRILLIC CAPITAL LETTER EF
    'г'   #*  0x67 -> CYRILLIC CAPITAL LETTER GHE
    'х'   #*  0x68 -> CYRILLIC CAPITAL LETTER HA
    'и'   #*  0x69 -> CYRILLIC CAPITAL LETTER I
    'й'   #*  0x6A -> CYRILLIC CAPITAL LETTER SHORT I
    'к'   #*  0x6B -> CYRILLIC CAPITAL LETTER KA
    'л'   #*  0x6C -> CYRILLIC CAPITAL LETTER EL
    'м'   #*  0x6D -> CYRILLIC CAPITAL LETTER EM
    'н'   #*  0x6E -> CYRILLIC CAPITAL LETTER EN
    'о'   #*  0x6F -> CYRILLIC CAPITAL LETTER O
    'п'   #*  0x70 -> CYRILLIC CAPITAL LETTER PE
    'я'   #*  0x71 -> CYRILLIC CAPITAL LETTER YA
    'р'   #*  0x72 -> CYRILLIC CAPITAL LETTER ER
    'с'   #*  0x73 -> CYRILLIC CAPITAL LETTER ES
    'т'   #*  0x74 -> CYRILLIC CAPITAL LETTER TE
    'у'   #*  0x75 -> CYRILLIC CAPITAL LETTER U
    'ж'   #*  0x76 -> CYRILLIC CAPITAL LETTER ZHE
    'в'   #*  0x77 -> CYRILLIC CAPITAL LETTER VE
    'ь'   #*  0x78 -> CYRILLIC CAPITAL LETTER SOFT SIGN
    'ы'   #*  0x79 -> CYRILLIC CAPITAL LETTER YERU
    'з'   #*  0x7A -> CYRILLIC CAPITAL LETTER ZE
    '?'   #*  0x7B -> CYRILLIC CAPITAL LETTER SHA
    '?'   #*  0x7C -> CYRILLIC CAPITAL LETTER E
    'щ'   #*  0x7D -> CYRILLIC CAPITAL LETTER SHCHA
    'ч'   #*  0x7E -> CYRILLIC CAPITAL LETTER CHE
    '?'   #*  0x7F -> забой
)

### Encoding table
encoding_table=codecs.charmap_build(decoding_table)

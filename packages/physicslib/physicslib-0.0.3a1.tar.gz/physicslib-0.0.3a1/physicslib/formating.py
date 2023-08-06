"""Module with functions for pretty printing of physicslib objects."""


__superscripts = {
    "0": "\u2070",
    "1": "\u00B9",
    "2": "\u00B2",
    "3": "\u00B3",
    "4": "\u2074",
    "5": "\u2075",
    "6": "\u2076",
    "7": "\u2077",
    "8": "\u2078",
    "9": "\u2079",
    "-": "\u207B"
}


def superscripted(n: int) -> str:
    """Superscripted integer"""
    string = str(n)
    superscripted_str = ""
    for ch in string:
        superscripted_str += __superscripts[ch]
    return superscripted_str

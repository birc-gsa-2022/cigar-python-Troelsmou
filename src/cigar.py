"""A module for translating between edit strings and cigar strings."""

import re


def split_pairs(cigar: str) -> list(tuple((int, str))):
    """Split a CIGAR string into a list of integer-operation pairs.
    Args:
        cigar (str): A CIGAR string
    Returns:
        list[tuple[int, str]]: A list of pairs, where the first element is
        an integer and the second an edit operation.
    >>> split_pairs("1M1D6M1I4M")
    [(1, 'M'), (1, 'D'), (6, 'M'), (1, 'I'), (4, 'M')]
    """

    cigar_list = []
    for i in range(0, len(cigar), 2):
        cigar_list.append((int(cigar[i]), cigar[i+1]))
    return (cigar_list)

def cigar_to_edits(cigar: str) -> str:
    """Expand the compressed CIGAR encoding into the full list of edits.
    Args:
        cigar (str): A CIGAR string
    Returns:
        str: The edit operations the CIGAR string describes.
    >>> cigar_to_edits("1M1D6M1I4M")
    'MDMMMMMMIMMMM'
    """
    edits_str = ""
    for i in range(0, len(cigar), 2):
        for j in range(int(cigar[i])): # Loop for each repetition of a CIGAR descriptor (M, I, D)
            edits_str += cigar[i+1]
    return (edits_str)

def split_blocks(x: str) -> list():
    """Split a string into blocks of equal character.
    Args:
        x (str): A string, but we sorta think it would be edits.
    Returns:
        list[str]: A list of blocks.
    >>> split_blocks('MDMMMMMMIMMMM')
    ['M', 'D', 'MMMMMM', 'I', 'MMMM']
    """
    block_list = []
    current_letter = x[0]
    current_block = ""
    for i in range(len(x)):
        if x[i] == current_letter:
            current_block += x[i]
        else:
            current_letter = x[i]
            block_list.append(current_block)
            current_block = x[i]
    block_list.append(current_block) # Putting this outside the loop so there isn't an if statement
                                     # which is checked each iteration but it will still save
                                     # the last block
    return (block_list)

def edits_to_cigar(edits: str) -> str:
    """Encode a sequence of edits as a CIGAR.
    Args:
        edits (str): A sequence of edit operations
    Returns:
        str: The CIGAR encoding of edits.
    >>> edits_to_cigar('MDMMMMMMIMMMM')
    '1M1D6M1I4M'
    """
    block_list = split_blocks(edits)
    CIGAR_str = ""
    for i in block_list:
        edit = str(len(i)) + i[0]
        CIGAR_str += edit

    return (CIGAR_str)
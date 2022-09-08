"""A module for translating between alignments and edits sequences."""


def get_edits(p, q):
    """Extract the edit operations from a pairwise alignment.
    Args:
        p (str): The first row in the pairwise alignment.
        q (str): The second row in the pairwise alignment.
    Returns:
        str: The list of edit operations as a string.
    >>> get_edits('ACCACAGT-CATA', 'A-CAGAGTACAAA')
    ('ACCACAGTCATA', 'ACAGAGTACAAA', 'MDMMMMMMIMMMM')
    """
    assert(len(p) == len(q))
    read = p.replace("-", "")
    ref = q.replace("-", "")
    CIGAR = ""
    for i in range(len(p)):
        if p[i] == "-":
            CIGAR += "I"
        elif q[i] == "-":
            CIGAR += "D"
        else:
            CIGAR += "M"

    return (read, ref, CIGAR)

def local_align(p: str, x: str, i: int, edits: str) -> tuple((str, str)):
    """Align two sequences from a sequence of edits.
    Args:
        p (str): The read string we have mapped against x
        x (str): The longer string we have mapped against
        i (int): The location where we have an approximative match
        edits (str): The list of edits to apply, given as a string
    Returns:
        tuple[str, str]: The two rows in the pairwise alignment
    >>> local_align("ACCACAGTCATA", "GTACAGAGTACAAA", 2, "MDMMMMMMIMMMM")
    ('ACCACAGT-CATA', 'A-CAGAGTACAAA')
    """
    x = x[i:]
    read = ""
    ref = ""
    deletions = 0 # Keeps track of deletions and insertions
    insertions = 0 # Critique is welcomed, couldn't find another way to make it work
    for i in range(len(edits)):
        if edits[i] == "M":
            read += p[i - insertions] # Inserts a base based on how many bases are in the alignment already
            ref += x[i - deletions]
        if edits[i] == "D":
            read += p[i - insertions]
            ref += "-"
            deletions += 1
        if edits[i] == "I":
            ref += x[i - deletions]
            read += "-"
            insertions += 1

    return (read, ref)

def align(p: str, q: str, edits: str) -> tuple((str, str)):
    """Align two sequences from a sequence of edits.
    Args:
        p (str): The first sequence to align.
        q (str): The second sequence to align
        edits (str): The list of edits to apply, given as a string
    Returns:
        tuple[str, str]: The two rows in the pairwise alignment
    >>> align("ACCACAGTCATA", "ACAGAGTACAAA", "MDMMMMMMIMMMM")
    ('ACCACAGT-CATA', 'A-CAGAGTACAAA')
    """
    # A full alignment here is just one that starts at index zero.
    # If the strings are valid input, all of q will be aligned.

    return local_align(p, q, 0, edits)

def edit_dist(p: str, x: str, i: int, edits: str) -> int:
    """Get the distance between p and the string that starts at x[i:]
    using the edits.
    Args:
        p (str): The read string we have mapped against x
        x (str): The longer string we have mapped against
        i (int): The location where we have an approximative match
        edits (str): The list of edits to apply, given as a string
    Returns:
        int: The distance from p to x[i:?] described by edits
    >>> edit_dist("accaaagta", "cgacaaatgtcca", 2, "MDMMIMMMMIIM")
    5
    """
    read, ref = local_align(p, x, i, edits)
    distance = 0
    for i in range(len(read)):
        if read[i] == ref[i]:
            continue
        distance += 1
    return (distance)
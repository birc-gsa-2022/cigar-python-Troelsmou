"""A module for translating between alignments and edits sequences."""


def get_edits(p: str, q: str) -> tuple[str, str, str]:
    """Extract the edit operations from a pairwise alignment.

    Args:
        p (str): The first row in the pairwise alignment.
        q (str): The second row in the pairwise alignment.

    Returns:
        str: The list of edit operations as a string.

    >>> get_edits('ACCACAGT-CATA', 'A-CAGAGTACAAA')
    ('ACCACAGTCATA', 'ACAGAGTACAAA', 'MDMMMMMMIMMMM')

    """
    assert len(p) == len(q)
    edits = [None] * len(p)
    for i, _ in enumerate(p):
        if p[i] == '-':
            edits[i] = 'I'
        elif q[i] == '-':
            edits[i] = 'D'
        else:
            edits[i] = 'M'
    return (p.replace('-', ''), q.replace('-', ''), "".join(edits))


def local_align(p: str, x: str, i: int, edits: str) -> tuple[str, str]:
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
    j, k = 0, 0
    row_p, row_q = [], []
    for op in edits:
        match op:
            case 'M':
                row_p.append(p[j])
                row_q.append(x[i+k])
                j += 1
                k += 1
            case 'D':
                row_p.append(p[j])
                row_q.append('-')
                j += 1
            case 'I':
                row_p.append('-')
                row_q.append(x[i+k])
                k += 1

    return "".join(row_p), "".join(row_q)


def align(p: str, q: str, edits: str) -> tuple[str, str]:
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
    return -1

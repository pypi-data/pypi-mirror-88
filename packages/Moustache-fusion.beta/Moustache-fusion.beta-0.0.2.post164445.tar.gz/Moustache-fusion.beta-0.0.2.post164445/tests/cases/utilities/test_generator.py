# -*- coding: utf-8 -*-

from itertools import islice
from moustache_fusion.utilities import alphabet_generator, sequence_generator


def test_alphabet_generator():
    expected = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD']
    assert list(islice(alphabet_generator(), 30)) == expected


def test_sequence_generator():
    expected = ['A', 'B', 'C', 'AA', 'AB', 'AC', 'BA', 'BB', 'BC', 'CA', 'CB', 'CC', 'AAA', 'AAB', 'AAC', 'ABA', 'ABB',
                'ABC', 'ACA', 'ACB']
    assert list(islice(sequence_generator('ABC'), 20)) == expected

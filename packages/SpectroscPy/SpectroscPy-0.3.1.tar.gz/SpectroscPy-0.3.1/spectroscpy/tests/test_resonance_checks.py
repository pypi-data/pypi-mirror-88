# SpectroscPy 0.3.1
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

# Test module for resonance_checks

import pytest
from spectroscpy import is_fermi_resonance, is_11_resonance, add_fermi_resonance

def test_is_fermi_resonance():

    assert is_fermi_resonance(5.0e-21, 2.0e-21, 1) == 0
    assert is_fermi_resonance(2.0e-21, 1.0e-21, 1) == 0

    assert is_fermi_resonance(2.0e-21, 2.0e-21, 1) == 0
    assert is_fermi_resonance(2.0e-21, 3.0e-21, 1) == 1

    assert is_fermi_resonance(2.0e-21, 2.0e-21, 0) == 1
    assert is_fermi_resonance(2.0e-21, 1.0e-21, 0) == 0


def test_add_fermi_resonance():

    fermi = []
    new = [1, 2, 3, 4]

    fermi = add_fermi_resonance(fermi, new)

    assert [[1, 2, 3, 4]] == fermi

    new = [1, 1, 0, 4]
    fermi = add_fermi_resonance(fermi, new)

    assert [[1, 2, 3, 4], [1, 0, 1, 4]] == fermi

    new = [1, 2, 3, 4]
    fermi = add_fermi_resonance(fermi, new)

    assert [[1, 2, 3, 4], [1, 0, 1, 4]] == fermi

    new = [2, 1, 3, 4]
    fermi = add_fermi_resonance(fermi, new)

    assert [[1, 2, 3, 4], [1, 0, 1, 4], [2, 1, 3, 4]] == fermi

    new = [2, 3, 1, 4]
    fermi = add_fermi_resonance(fermi, new)

    assert [[1, 2, 3, 4], [1, 0, 1, 4], [2, 1, 3, 4]] == fermi


def test_is_11_resonance():

    # Too large delta, too small K
    assert is_11_resonance(5.0e-21, 1.0e-22, 'quartic') == 0
    # Too large delta, but large enough K
    assert is_11_resonance(5.0e-21, 3.0e-22, 'quartic') == 0
    # Small enough delta, but too small K, in both K/v^2 and K
    assert is_11_resonance(1.0e-21, 1.0e-22, 'quartic') == 0
    # Very small delta, but too small K/v^2
    assert is_11_resonance(1.0e-23, 1.0e-24, 'quartic') == 0
    # Small enough delta, large enough enough K
    assert is_11_resonance(1.0e-21, 3.0e-22, 'quartic') == 1
    # Very small delta, too small K, but K/v^2 large enough
    assert is_11_resonance(1.0e-23, 1.0e-22, 'quartic') == 1

    # Too large delta, too small K
    assert is_11_resonance(5.0e-21, 1.0e-45, 'cubic') == 0
    # Too large delta, but large enough K
    assert is_11_resonance(5.0e-21, 5.0e-45, 'cubic') == 0
    # Small enough delta, but too small K, in both K/v^2 and K
    assert is_11_resonance(1.0e-21, 1.0e-45, 'cubic') == 0
    # Very small delta, but too small K/v^2
    assert is_11_resonance(1.0e-23, 7.0e-47, 'cubic') == 0
    # Small enough delta, large enough enough K
    assert is_11_resonance(1.0e-21, 5.0e-45, 'cubic') == 1
    # Very small delta, too small K, but K/v^2 large enough
    assert is_11_resonance(1.0e-23, 2.0e-46, 'cubic') == 1

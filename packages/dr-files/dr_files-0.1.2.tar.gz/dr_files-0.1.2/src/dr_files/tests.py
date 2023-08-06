import filecmp

import numpy as np
import pytest

from dr_files.utilities import dr_to_csv, dr_to_tdms, dr_to_values, dr_to_wav


def test_values():
    _, signals = dr_to_values("./fixtures/demo.dr")
    assert pytest.approx(np.mean(signals[0] ** 2), 0.001) == 2.324


def test_wav():
    dr_to_wav("./fixtures/demo.dr", "/tmp/dr.wav")
    assert filecmp.cmp("./fixtures/demo.wav", "/tmp/dr.wav", shallow=True)


def test_tdms():
    dr_to_tdms("./fixtures/demo.dr", "/tmp/dr.tdms")
    assert filecmp.cmp("./fixtures/demo.tdms", "/tmp/dr.tdms", shallow=True)


def test_csv():
    dr_to_csv("./fixtures/demo.dr", "/tmp/dr.csv")
    assert filecmp.cmp("./fixtures/demo.csv", "/tmp/dr.csv", shallow=True)

# coding: utf-8

from sullyutil import freeport


def test_freeport():
    port = freeport()
    assert isinstance(port, int)
    

# -*- coding = UTF-8 -*-
# Autohr   : yang
# File     : case.py
# project  : UIAutoProject
# time     : 2020/12/4 18:05
# Describe : 
# ---------------------------------------
import pytest


class TestCase:

    @pytest.fixture(scope="function")
    def setUp(self, getdriver, flush_browser): ...

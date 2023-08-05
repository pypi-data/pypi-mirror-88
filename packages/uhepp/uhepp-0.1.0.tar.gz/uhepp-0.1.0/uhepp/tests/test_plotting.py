
# Copyright (C) 2020 Frank Sauerburger

import unittest
from uhepp import UHeppHist

class UHepPlotingTestCase(unittest.TestCase):
    """Check the implementation of various plotting methods"""

    def test_update_style_map(self):
        """Check that all allowed values are wired to the correct output"""
        kwds= {}
        UHeppHist._update_style(kwds, {"linewidth": 1.2,
                                      "linestyle": ':',
                                      "color": (1, 2, 3),
                                      "edgecolor": (2, 2, 3)})

        self.assertEqual(kwds, {"linewidth": 1.2,
                                "linestyle": ':',
                                "color": (1, 2, 3),
                                "edgecolor": (2, 2, 3)})


    def test_update_style_missing(self):
        """Check that missing input values keep the output unchanged"""
        kwds = {"linestyle": ':', "color": (1, 2, 3)}
        UHeppHist._update_style(kwds, {})
        self.assertEqual(kwds, {"linestyle": ':', "color": (1, 2, 3)})

    def test_update_style_aux(self):
        """Check that additional input values are ignored"""
        kwds = {}
        UHeppHist._update_style(kwds, {"linestyle": ":", "whatever": 3})
        self.assertEqual(kwds, {"linestyle": ':'})

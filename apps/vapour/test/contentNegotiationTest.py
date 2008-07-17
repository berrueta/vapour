#!/usr/bin/python
# -*- coding: utf8 -*-

import unittest
import sys
sys.path.append("../src/")
from vapour.cup.common import getBestFormat

class ContentNegotiationTest(unittest.TestCase):

    def setUp(self):
        pass

    def testFirefox(self):
        self.assertEquals(getBestFormat("text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"), "html")

    def testOnlyRdf(self):
        self.assertEquals(getBestFormat("application/rdf+xml"), "rdf")

    def testRdfAndHtml(self):
        self.assertEquals(getBestFormat("application/rdf+xml, text/html"), "html")

    def testRdfAndHtmlWithQ(self):
        self.assertEquals(getBestFormat("application/rdf+xml,text/html;q=0.9"), "rdf")
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()

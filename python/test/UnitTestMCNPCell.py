#!/usr/env/python3

import unittest
import sys
sys.path.append("..")
from MCNPCellCard import MCNPCellCard
from CellCard import CellCard

class TestMCNPCellMethods(unittest.TestCase):

    # TODO definitely add some more robust testing of the position of the
    # logical operations - Very Important
    
    def test_simple_cell(self):
        card_string = "1 1 -1.0 -4 5 -6 7"
        card = MCNPCellCard(card_string)
        self.assertEqual(card.text_string, card_string)
        self.assertEqual(card.cell_id, 1)
        self.assertEqual(card.cell_density, -1.0)

    def test_more_complex_cell(self):
        card_string = "2 3 -14.0 (-4 5 -6 7):(9 12 13)"
        card = MCNPCellCard(card_string)
        self.assertEqual(card.text_string, card_string)
        self.assertEqual(card.cell_id, 2)
        self.assertEqual(card.cell_material_number, 3)
        self.assertEqual(card.cell_density, -14.0)
        
if __name__ == '__main__':
    unittest.main()

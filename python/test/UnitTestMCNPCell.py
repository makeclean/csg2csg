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

    def test_mcnp_detect_keywords_all(self):
        string = "2 3 -14.0 1 imp:n=1 imp:p=1 u=3 fill=12 vol=150"
        cell_card = MCNPCellCard(string)
        new_string =  cell_card._MCNPCellCard__detect_keywords(['imp','u','fill','vol'],string)
        self.assertEqual(new_string, "2 3 -14.0 1 ")

    def test_mcnp_detect_keywords_imp(self):
        string = "2 3 -14.0 1 imp:n=1 imp:p=1 "
        cell_card = MCNPCellCard(string)
        new_string =  cell_card._MCNPCellCard__detect_keywords(['imp'],string)
        self.assertEqual(new_string, "2 3 -14.0 1 ")

    def test_mcnp_detect_keywords_uni(self):
        string = "2 3 -14.0 1 u=1 "
        cell_card = MCNPCellCard(string)
        new_string =  cell_card._MCNPCellCard__detect_keywords(['u'],string)
        self.assertEqual(new_string, "2 3 -14.0 1 ")

    def test_mcnp_detect_keywords_fill(self):
        string = "2 3 -14.0 1 fill=3"
        cell_card = MCNPCellCard(string)
        new_string =  cell_card._MCNPCellCard__detect_keywords(['fill'],string)
        self.assertEqual(new_string, "2 3 -14.0 1 ")

    def test_mcnp_detect_keywords_vol(self):
        string = "2 3 -14.0 1 vol=300"
        cell_card = MCNPCellCard(string)
        new_string =  cell_card._MCNPCellCard__detect_keywords(['vol'],string)
        self.assertEqual(new_string, "2 3 -14.0 1 ")
        
if __name__ == '__main__':
    unittest.main()

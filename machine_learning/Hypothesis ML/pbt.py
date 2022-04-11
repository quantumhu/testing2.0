
"""
Created on Mon Mar  7 15:00:25 2022

@author: claremcmullen
"""

import unittest
from unittest import TestCase
from hypothesis import given, strategies, settings

from model import TitanicModel
from schema import TitanicModelInput, TitanicModelOutput


class ModelPropertyBasedTests(TestCase):

    def setUp(self) -> None:
        self.counter = 0
        self.model = TitanicModel()

    def tearDown(self) -> None:
        print("Generated and tested {} examples.".format(self.counter))

    @settings(deadline=None, max_examples=1000)
    @given(strategies.builds(TitanicModelInput))
    def test_model_input(self, data):
        # act
        result = self.model.predict(data=data)

        # assert
        self.assertTrue(type(result) is TitanicModelOutput)

        self.counter += 1


if __name__ == '__main__':
    unittest.main()
# test_CombinedAttributesAdder.py
import numpy as np
import unittest

from production.scripts import CombinedAttributesAdder


class TestCombinedAttributesAdder(unittest.TestCase):
    """
    Test suite for the CombinedAttributesAdder class.
    """

    def test_transform(self):
        """
        Test the transform method of the CombinedAttributesAdder class.
        This test ensures that the transformed data matches the expected values.
        """
        data = np.array([
            [2000, 500, 1000, 400],
            [3000, 600, 2000, 600],
            [1000, 200, 500, 250]
        ])

        rooms_ix, bedrooms_ix, population_ix, households_ix = 0, 1, 2, 3
        adder = CombinedAttributesAdder(rooms_ix, bedrooms_ix, population_ix, households_ix)
        transformed_data = adder.transform(data)

        expected_data = np.array([
            [2000, 500, 1000, 400, 5.0, 2.5, 0.25],
            [3000, 600, 2000, 600, 5.0, 3.3333333333333335, 0.2],
            [1000, 200, 500, 250, 4.0, 2.0, 0.2]
        ])

        np.testing.assert_almost_equal(transformed_data, expected_data)

    def test_inverse_transform(self):
        """
        Test the inverse_transform method of the CombinedAttributesAdder class.
        This test ensures that the original data is correctly reconstructed from
        the transformed data.
        """
        data = np.array([
            [2000, 500, 1000, 400, 5.0, 2.5, 0.25],
            [3000, 600, 2000, 600, 5.0, 3.3333333333333335, 0.2],
            [1000, 200, 500, 250, 4.0, 2.0, 0.2]
        ])

        rooms_ix, bedrooms_ix, population_ix, households_ix = 0, 1, 2, 3
        adder = CombinedAttributesAdder(rooms_ix, bedrooms_ix, population_ix, households_ix)
        original_data = adder.inverse_transform(data)

        expected_data = np.array([
            [2000, 500, 1000, 400],
            [3000, 600, 2000, 600],
            [1000, 200, 500, 250]
        ])

        np.testing.assert_almost_equal(original_data, expected_data)


if __name__ == '__main__':
    unittest.main()

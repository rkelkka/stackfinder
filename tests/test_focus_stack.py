import focus_stack
import unittest
import os
import json

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'test_metadata.json')

# Configuration to produce expected stacks from the test data
TEST_CONFIG = {
    'timestamp_threshold_sec': '0.5',
    'continuous_drive': '0',
    'min_stack_size': '2'
}

EXPECTED_STACKS = [
    "2023-08-13_18-09-33.33__IMG_8783-IMG_8882__100",
    "2023-08-13_18-10-17.66__IMG_8883-IMG_8982__100",
    "2023-08-13_18-12-46.67__IMG_8983-IMG_9002__020",
    "2023-08-13_18-13-26.51__IMG_9003-IMG_9062__060",
    "2023-08-13_18-14-15.31__IMG_9063-IMG_9122__060",
    "2023-08-13_18-19-17.91__IMG_9127-IMG_9136__010",
    "2023-08-13_18-20-14.00__IMG_9137-IMG_9146__010"
]

class TestFocusStack(unittest.TestCase):

    def setUp(self):
        self.testfile = open(TESTDATA_FILENAME)
        self.testdata = json.load(self.testfile)

    def tearDown(self):
        self.testfile.close()

    """
    Test focus stack search
    """
    def test_search_stacks(self):
        stacks = focus_stack.search(self.testdata, TEST_CONFIG["timestamp_threshold_sec"], TEST_CONFIG["continuous_drive"], TEST_CONFIG["min_stack_size"] )
        self.assertEqual(len(stacks), 7)
        stack_labels = [focus_stack.get_stack_label(s) for s in stacks]
        self.assertListEqual(stack_labels, EXPECTED_STACKS)
if __name__ == '__main__':
    unittest.main()
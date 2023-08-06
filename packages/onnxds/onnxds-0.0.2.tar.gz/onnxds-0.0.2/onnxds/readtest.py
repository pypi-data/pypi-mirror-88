import unittest

import onnxds.read_dataset as helper

class ReadTest(unittest.TestCase):
    def test_single_entry(self):
        dsgen = helper.load('onnxds/mnist.onnx')
        self.assertIsNotNone(dsgen)
        it = next(dsgen)
        self.assertIsInstance(it, dict)
        self.assertIn('label', it)
        self.assertIn('image', it)
        label = it['label']
        image = it['image']
        self.assertEqual((1,), label.shape)
        self.assertEqual((1, 28, 28, 1), image.shape)

    def test_batch_entry(self):
        dsgen = helper.load('onnxds/mnist_5batch.onnx')
        self.assertIsNotNone(dsgen)
        it = next(dsgen)
        self.assertIsInstance(it, dict)
        self.assertIn('label', it)
        self.assertIn('image', it)
        label = it['label']
        image = it['image']
        self.assertEqual((5,), label.shape)
        self.assertEqual((5, 28, 28, 1), image.shape)

if __name__ == "__main__":
    unittest.main()

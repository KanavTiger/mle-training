import pytest
from mypackage.train import train_model

def test_train_model():
    # Test the training function
    assert train_model('test_data', 'test_output') is not None


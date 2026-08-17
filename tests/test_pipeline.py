"""
Basic tests for the crypto data validation logic used in
bigquery/transform_query.sql. These check the *rules* in Python
so they can run automatically, without needing a live BigQuery connection.
"""

def is_valid_row(open_, high, low, close, volume, market_cap):
    """Mirrors the validation rules in transform_query.sql"""
    if close is None or open_ is None:
        return False
    if volume < 0 or market_cap < 0:
        return False
    if high < low:
        return False
    if not (low <= open_ <= high):
        return False
    if not (low <= close <= high):
        return False
    return True


def test_valid_row_passes():
    assert is_valid_row(open_=100, high=110, low=95, close=105, volume=1000, market_cap=50000) is True


def test_negative_volume_fails():
    assert is_valid_row(open_=100, high=110, low=95, close=105, volume=-5, market_cap=50000) is False


def test_high_lower_than_low_fails():
    assert is_valid_row(open_=100, high=90, low=95, close=105, volume=1000, market_cap=50000) is False


def test_close_outside_high_low_fails():
    assert is_valid_row(open_=100, high=110, low=95, close=200, volume=1000, market_cap=50000) is False


def test_missing_close_fails():
    assert is_valid_row(open_=100, high=110, low=95, close=None, volume=1000, market_cap=50000) is False

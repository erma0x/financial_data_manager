import pytest
from datetime import datetime, time
import pytz
import holidays
import random

from ..source.market_open import is_weekend, is_us_holiday, calculate_time_difference, market_is_open

def test_is_weekend():
    # Test for a weekend day
    weekend_day = datetime(2023, 7, 8, 12, 0, 0)  # A Saturday
    assert is_weekend(weekend_day) == True

    # Test for a weekday
    weekday = datetime(2023, 7, 10, 12, 0, 0)  # A Monday
    assert is_weekend(weekday) == False

def test_is_us_holiday():
    # Test for a US holiday
    us_holiday = datetime(2023, 7, 4, 12, 0, 0)  # July 4th, 2023
    assert is_us_holiday(us_holiday) == True

    # Test for a non-US holiday
    non_us_holiday = datetime(2023, 7, 10, 12, 0, 0)  # Not a US holiday
    assert is_us_holiday(non_us_holiday) == False

def test_calculate_time_difference():
    # Test the time difference calculation
    desired_time = time(10, 30, 0)  # 10:30:00
    time_difference = calculate_time_difference(desired_time)

    # Assert that the time difference is within a certain range (e.g., 0 to 1 hour)
    assert 0 <= time_difference.total_seconds() <= 3600

def test_market_is_open(mocker):
    mocker.patch('my_script.datetime')  # Mock the datetime module

    # Test when the market is open
    mocker.datetime.now.return_value = datetime(2023, 7, 10, 12, 0, 0)  # A Monday, within market hours
    assert market_is_open() == True

    # Test when the market is closed due to a US holiday
    mocker.datetime.now.return_value = datetime(2023, 7, 4, 12, 0, 0)  # July 4th, 2023
    assert market_is_open() == False

    # Test when the market is closed on a weekend
    mocker.datetime.now.return_value = datetime(2023, 7, 8, 12, 0, 0)  # A Saturday
    assert market_is_open() == False

    # Test when the market is closed outside market hours
    mocker.datetime.now.return_value = datetime(2023, 7, 10, 18, 0, 0)  # A Monday, after market hours
    assert market_is_open() == False

    # Test when the market is closed before market hours
    mocker.datetime.now.return_value = datetime(2023, 7, 11, 8, 0, 0)  # A Tuesday, before market hours
    assert market_is_open() == False

    # Test when the market is closed due to random conditions
    mocker.datetime.now.return_value = datetime(2023, 7, 11, 12, 0, 0)  # A Tuesday, within market hours
    mocker.is_us_holiday.return_value = False
    mocker.is_weekend.return_value = False
    assert market_is_open() == False

@pytest.mark.parametrize("print_event", [True, False])
def test_market_is_open_print_event(mocker, print_event):
    mocker.patch('my_script.datetime')  # Mock the datetime module
    mocker.patch('my_script.clear_screen')  # Mock the clear_screen function

    mocker.datetime.now.return_value = datetime(2023, 7, 10, 12, 0, 0)  # A Monday, within market hours
    assert market_is_open(print_event=print_event) == True

    mocker.clear_screen.assert_called_once() if print_event else mocker.clear_screen.assert_not_called()

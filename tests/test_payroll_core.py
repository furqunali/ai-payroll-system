import pytest
from payroll_core.calculator import calculate_pay
from payroll_core.models import Employee


def test_regular_pay():
    result = calculate_pay(Employee("E1", "Ada", 20), 40)
    assert result.total_hours == 40
    assert result.gross_pay == 800


def test_overtime_pay():
    result = calculate_pay(Employee("E2", "Lin", 20), 45)
    assert result.overtime_hours == 5
    assert result.gross_pay == 950


def test_negative_hours_rejected():
    with pytest.raises(ValueError):
        calculate_pay(Employee("E3", "Sam", 20), -1)


def test_negative_rate_rejected():
    with pytest.raises(ValueError):
        Employee("E4", "Kim", -1)

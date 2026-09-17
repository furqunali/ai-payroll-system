"""Deterministic payroll calculations with explicit overtime rules."""
from .models import Employee, PayResult


def calculate_pay(employee: Employee, hours: float, overtime_after: float = 40.0) -> PayResult:
    if hours < 0:
        raise ValueError("hours cannot be negative")
    if overtime_after <= 0:
        raise ValueError("overtime_after must be positive")
    regular = min(hours, overtime_after)
    overtime = max(0.0, hours - overtime_after)
    gross = regular * employee.hourly_rate + overtime * employee.hourly_rate * 1.5
    return PayResult(employee.employee_id, regular, overtime, round(gross, 2))

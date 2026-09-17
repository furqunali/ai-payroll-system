"""Typed payroll domain models."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Employee:
    employee_id: str
    name: str
    hourly_rate: float

    def __post_init__(self):
        if not self.employee_id.strip():
            raise ValueError("employee_id is required")
        if self.hourly_rate < 0:
            raise ValueError("hourly_rate cannot be negative")


@dataclass(frozen=True)
class PayResult:
    employee_id: str
    regular_hours: float
    overtime_hours: float
    gross_pay: float

    @property
    def total_hours(self) -> float:
        return self.regular_hours + self.overtime_hours

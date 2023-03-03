from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


def age_validator(date_of_birth, restriction_age):
    years_of_age = (datetime.today().date() - date_of_birth) // timedelta(days=365.2422)
    if years_of_age < restriction_age:
        raise ValidationError("You must be at least 18 years old to sign up!")

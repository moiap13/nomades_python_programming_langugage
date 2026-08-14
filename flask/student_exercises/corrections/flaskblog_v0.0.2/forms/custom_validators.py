import string

from wtforms.validators import ValidationError

def validate_password(form, field):
  if len(field.data) < 8:
    raise ValidationError("Password must be at least 8 characters long")
  if not any(c.isupper() for c in field.data):
    raise ValidationError("Password must contain at least one uppercase letter")
  if not any(c.islower() for c in field.data):
    raise ValidationError("Password must contain at least one lowercase letter")
  if not any(c.isdigit() for c in field.data):
    raise ValidationError("Password must contain at least one number")
  if not any(c in string.punctuation for c in field.data):
    raise ValidationError("Password must contain at least one special character")

  return field.data

def validate_pp(form, field):
  if field.data.content_type not in ["image/jpg", "image/jpeg", "image/png"]:
    raise ValidationError(f"Invalid file type {field.data.content_type} is not part of ['image/jpg', 'image/jpeg', 'image/png']")

  return field.data
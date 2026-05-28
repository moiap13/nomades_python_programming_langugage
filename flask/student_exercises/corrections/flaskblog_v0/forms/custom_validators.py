from wtforms.validators import ValidationError

def validate_password(form, field):
  return True
  data = field.data
  if len(data) < 8:
    raise ValidationError("Password must be at least 8 characters long")
  if not any([char in ascii_lowercase for char in data]):
    raise ValidationError("Password must contain at least one lower case")
  if not any([char in ascii_uppercase for char in data]):
    raise ValidationError("Password must contain at least one upper case")
  if not any([char in digits for char in data]):
    raise ValidationError("Password must contain at least one digit")
  if not any([char in punctuation for char in data]):
    raise ValidationError("Password must contain at least one special char")

def validate_image(form, field):
  allowed_pp_types: list[str] = ['image/png', 'image/jpeg', 'image/jpg']

  if field.data.content_type not in allowed_pp_types:
    raise ValidationError('Only JPG and PNG image files supported')
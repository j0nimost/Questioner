from ..models.usermodel import user_schema, login_schema
from ..models.meetupmodel import meetup_schema, image_schema

config = {
    'user': user_schema,
    'login': login_schema,
    'meetup': meetup_schema,
    'images': image_schema
}

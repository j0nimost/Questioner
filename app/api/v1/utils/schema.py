from ..models.meetupmodel import meetup_schema, rsvp_schema
from ..models.questionmodel import question_schema, vote_schema
from ..models.commentmodel import comment_schema


config = {
    'meetup': meetup_schema,
    'rsvp': rsvp_schema,
    'question': question_schema,
    'vote': vote_schema,
    'comment': comment_schema
}

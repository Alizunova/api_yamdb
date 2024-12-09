MAX_EMAIL_LENGHT = 254
MAX_TEXT_LENGTH = 256
MAX_SCORE_VALUE = 10
MAX_USERNAME_LENGHT = 150
MIN_SCORE_VALUE = 1
SHORT_TEXT_LENGTH = 25

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

CHOICES = (
    ('admin', ADMIN),
    ('moderator', MODERATOR),
    ('user', USER),
)

BAD_USERNAME = [
    'me',
    ADMIN,
    MODERATOR,
    USER
]

EMAIL_MAX_LENGHT = 254
USERNAME_MAX_LENGHT = 150
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
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

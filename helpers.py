from itsdangerous import URLSafeTimedSerializer
import hashlib, binascii, os

SECRET_KEY = "97e5782c0ef1621d168ed4229ac95f148d1d09a9abaa490d7349d363f16cc7b3"
SECURITY_PASSWORD_SALT = '86343d47f9f472d4d992a87faf8e831e83e3a6659bea49d2bed48dd6f0b4e1be'


class InvalidTokenError(Exception):
    pass


def generate_confirmation_token(email):
    """ Generates a password creation token """
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    """ Confirms given password generation token """
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except Exception:
        raise InvalidTokenError("Token is expired.")
    return email


def hash_password(password):
    """Hash a password for storing."""
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  SECRET_KEY.encode('utf-8'), 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return pwdhash.decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  SECRET_KEY.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

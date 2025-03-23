import hashlib
import base64
import validators
from datetime import datetime, timedelta
import re

def generate_short_code(url, length=7):
    """Generate a short code from a URL using a hash function."""
    hash_object = hashlib.md5(url.encode())
    hash_digest = hash_object.digest()
    # Use base64 encoding to get alphanumeric result
    b64_encoded = base64.b64encode(hash_digest).decode()
    # Remove non-alphanumeric characters
    alphanumeric = re.sub(r'[^a-zA-Z0-9]', '', b64_encoded)
    return alphanumeric[:length]

def is_valid_url(url):
    """Check if the provided URL is valid."""
    return validators.url(url)

def calculate_expiration_date(days=None):
    """Calculate the expiration date based on days from now."""
    if days is None:
        return None
    return datetime.now() + timedelta(days=days)
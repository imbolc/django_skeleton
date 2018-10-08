from pathlib import Path
from django.core.management import utils

path = Path(__file__).resolve().parents[1] / 'var/secret.txt'
if not path.exists():
    print('Secret key generated')
    path.write_text(utils.get_random_secret_key())

SECRET_KEY = path.read_text()

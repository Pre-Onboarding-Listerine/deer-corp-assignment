import os

import yaml
from dotenv import load_dotenv


load_dotenv(verbose=True)

SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

with open("yamls/discounts.yaml") as f:
    discounts = yaml.load(f, Loader=yaml.FullLoader)

with open("yamls/fines.yaml") as f:
    fines = yaml.load(f, Loader=yaml.FullLoader)

with open("yamls/exceptions.yaml") as f:
    except_options = yaml.load(f, Loader=yaml.FullLoader)

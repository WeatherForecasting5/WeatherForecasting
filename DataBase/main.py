import datetime
from models import *

# Core Functionality
with db:
    db.create_tables([Type, City, Configuration, Source])

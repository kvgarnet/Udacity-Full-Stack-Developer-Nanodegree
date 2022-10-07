# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import os
load_dotenv()
DB_NAME = os.environ.get("DATABASE_NAME")
TEST_DB_NAME = os.environ.get("TEST_DATABASE_NAME")
DB_USER=os.environ.get("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASS")

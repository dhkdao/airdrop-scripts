from datetime import datetime, timezone
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import math
import pandas as pd
import random


def airdrop_monthly_alloc(config, output, type):
    print(config)
    print(output)
    print(type)

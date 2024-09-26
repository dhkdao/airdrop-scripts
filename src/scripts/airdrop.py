from datetime import datetime, timezone
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import math
import pandas as pd
from rich import print
import typer
import random


def airdrop_monthly_alloc(config_file, output, type):
    config = json.loads(config_file.read())

    # Check that all required fields exist
    required_keys = ["dhk_distribution", "reference_date", "tokens", "apis"];
    for key in required_keys:
        if key not in config or config[key] == "":
            print(f"Required key {key} is missing from the input config file");
            raise typer.Exit(code = 1)


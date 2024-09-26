from datetime import datetime, timezone
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# import math
import pandas as pd
from rich import print
import typer


class Airdrop:
    def check_config(config):
        # Check that all required fields exist
        required_keys = ["dhk_distribution", "reference_date", "tokens", "apis"]

        for key in required_keys:
            if key not in config or config[key] == "":
                print(f"Required key {key} is missing in the config")
                raise typer.Exit(code=1)

        return True

    def __init__(self, config_file):
        config = json.loads(config_file.read())
        if Airdrop.check_config(config):
            self.config = config
        self.reference_date = datetime(config["reference_date"], tzinfo=timezone.utc)

    # API doc:
    #   https://min-api.cryptocompare.com/documentation?key=Historical&cat=dataPriceHistorical
    def fetch_price(self, from_symbol, to_symbol="USD"):
        date = self.config["reference_date"]
        api = self.apis["cryptocompare"]
        endpoint, apikey = api["endpoint"], api["apikey"]
        parameters = {
            "fsym": from_symbol,
            "tsyms": to_symbol,
            "calculationType": "MidHighLow",
            "ts": date.timestamp(),
        }
        headers = {
            "Accepts": "application/json",
            "authorization": f"Apikey {apikey}",
        }

        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(endpoint, params=parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            raise Exception(f"fetch_price connection error: {e}")

        if from_symbol not in data:
            raise Exception(
                f"{from_symbol}: unable to fetch price for, returning: {data}"
            )

        return data[from_symbol][to_symbol]

    # API doc: https://docs.cosmostation.io/apis/reference/utilities/staking-apr
    def fetch_staking_apr(self, staking_network):
        api = self.apis["mintscan"]
        endpoint, apikey = api["endpoint"], api["apikey"]

        endpoint = endpoint.replace(":network", staking_network)
        headers = {
            "Accepts": "application/json",
            "authorization": f"Bearer {apikey}",
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(endpoint)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            raise Exception(f"fetch_staking_apr connection error: {e}")

        if "apr" not in data:
            raise Exception(
                f"{staking_network}: unable to fetch staking_apr, returning: {data}"
            )

        return float(data["apr"])

    def monthly_alloc(self, output, type):
        columns = [
            "token",
            "price",
            "staking-amt",
            "staking-val",
            "staking-apr",
            "reward",
            "dhk-distribution-pc",
            "dhk-distribution",
        ]

        # Used later in panda
        lst = []

        for t in self.config["tokens"]:
            token, staking_amt = t["token"], t["qty"]
            token_price = t["price"] if "price" in t else self.fetch_price(token)

            staking_val = token_price * staking_amt
            staking_apr = 0
            if "staking_apr" in t:
                staking_apr = t["staking_apr"]
            elif "network" in t:
                staking_apr = self.fetch_staking_apr(t["network"])

            reward = staking_apr * staking_val

            lst.append(
                [
                    token,
                    token_price,
                    staking_amt,
                    staking_val,
                    staking_apr,
                    reward,
                    0,
                    0,
                ]
            )

        # Panda
        df = pd.DataFrame(lst, columns=columns)
        return df

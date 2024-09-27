import json
import os
import pytest
import typer
from dotenv import load_dotenv
from scripts import Airdrop


load_dotenv()

UNKNOWN_TOKEN = "HASH"
KNOWN_TOKEN = "ATOM"
INVALID_CONFIG_FILEPATH = os.path.join(
    os.path.dirname(__file__), "../fixtures/config-invalid-1.json"
)

print("INVALID_CONFIG_FILEPATH", INVALID_CONFIG_FILEPATH)


def get_config():
    return json.loads(
        """{
        "dhk_distribution": 100000,
        "reference_date": "2024-08-27",
        "tokens": [
            { "token": "AKT", "network": "akash", "qty": 188787 },
            { "token": "ATOM", "network": "cosmos", "qty": 592015 }
        ],
        "apis": {
            "cryptocompare": {
                "endpoint": "https://min-api.cryptocompare.com/data/pricehistorical"
            },
            "mintscan": {
                "endpoint": "https://apis.mintscan.io/v1/:network/apr"
            }
        }
    }"""
    )


def get_config_with_cryptocompare_apikey_env():
    config = get_config()
    config["apis"]["cryptocompare"]["apikey"] = os.getenv("CRYPTOCOMPARE_APIKEY")
    return config


class TestAirdropClass:
    def test_fetch_price_on_unknown_token_should_return_none(self):
        config = get_config_with_cryptocompare_apikey_env()
        airdrop = Airdrop(config)
        price = airdrop.fetch_price(UNKNOWN_TOKEN)
        assert price is None

    def test_fetch_price_on_known_token_should_return_value(self):
        config = get_config_with_cryptocompare_apikey_env()
        airdrop = Airdrop(config)
        price = airdrop.fetch_price(KNOWN_TOKEN)
        assert isinstance(price, float)

    def test_on_config_missing_key_should_raise_exception(self):
        with open(INVALID_CONFIG_FILEPATH, "r") as f:
            config = json.loads(f.read())

        with pytest.raises(typer.Exit) as excinfo:
            Airdrop(config)

        assert excinfo.type is typer.Exit

    def test_fetch_staking_apr(self):
        pass

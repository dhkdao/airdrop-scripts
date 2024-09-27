# DHK Tokens Airdrop Scripts

A Python script to retrieve historical token prices and compute DHK tokens to distribute out each month.

- [DHK airdrop template master speadsheet](https://docs.google.com/spreadsheets/d/1QliDXE6yMNnPxhqraLqhTDnRQ0vbpvapLYoMC0vFgSc/edit?usp=sharing)

## Data Sources

Token price:
- <https://www.cryptocompare.com/>

Staking APR:
- <https://www.mintscan.io/> (operated by [Cosmostation](https://cosmostation.io/))

## Usage

```bash
pip install dhkdao-airdrop

# Get help
dhkdao-airdrop --help

# Run script with api keys set in config.json
dhkdao_airdrop config.json -o output -t type

# Run script with api keys set in env vars
CRYPTOCOMPARE_APIKEY="cc-apikey" MINTSCAN_APIKEY="ms-apikey" dhkdao_airdrop config.json -o output -t type
```

Options:

- `-o`: Output file path. If skipped, output is printed on screen.
- `-t`: [table|csv|json]. Output type.

You can have api keys set in the input config file or env var. Env vars will override the one set in config file.

### Input Config

An example is as followed.

```json
{
    "dhk_distribution": 100000,
    "reference_date": "2024-08-27",
    "tokens": [
        { "token": "AKT", "network": "akash", "qty": 188787 },
        { "token": "ATOM", "network": "cosmos", "qty": 592015 }
    ],
    "apis": {
        "cryptocompare": {
            "endpoint": "https://min-api.cryptocompare.com/data/pricehistorical",
            "apikey": "cryptocompare-123456"
        },
        "mintscan": {
            "endpoint": "https://apis.mintscan.io/v1/:network/apr",
            "apikey": "mintscan-123456"
        }
    }
}
```

The config used to run for 2024 Sep output are [here](./configs/config-202409.json).


- Most of the time, you only need to change the `reference_date` and the `tokens`.


## Development

Please copy `.env.example` over to `.env` and fills in the API_KEYs inside.

```bash
# sync all the dependencies
pdm sync -d

# show the help text
pdm exe --help

# Run the regular command
pdm exe input.json -o output -t json

# Run test cases with no output capture
pdm test:no-capture
```


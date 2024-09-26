# DHK Tokens Airdrop Scripts

A [Python script](./notebooks/airdrop.ipynb) to retrieve historical token prices and compute DHK tokens to distribute out each month.

- [DHK airdrop template master speadsheet](https://docs.google.com/spreadsheets/d/1QliDXE6yMNnPxhqraLqhTDnRQ0vbpvapLYoMC0vFgSc/edit?usp=sharing)

## Data Sources

Token price:
- <https://www.cryptocompare.com/>

Staking APR:
- <https://www.mintscan.io/> (operated by [Cosmostation](https://cosmostation.io/))

## Development

Please copy `.env.example` over to `.env` and fills in the API_KEYs inside.

```bash
pdm sync -d    # sync all the dependencies
pdm exe --help # show the help file
pdm exe input.json -o output -t json
```

- accept a file path, the input config file in json format.
- flag `-o`: accept a file path, the output file path.
- flag `-t`: accept one of the ["table", "json", "csv"], specifying the output format.

## Command

```bash
pip install dhkdao-airdrop
CRYPTOCOMPARE_APIKEY=abc MINTSCAN_APIKEY=abc dhkdao-airdrop -c input.json -o output -t json
```

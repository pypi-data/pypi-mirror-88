import pandas as pd
import os
import requests
import time

URL = "https://api.etherscan.io/api?"
KEY = os.getenv("ETHERSCAN_TOKEN")


def erc20(data):
    """
    :param data: either symbol (dont'care for upper/lowercase, or address (checks for starting with 0x and decides)
    :return: list of [symbol or address, decimals]
    """
    url = "https://tokens.coingecko.com/uniswap/all.json"
    r = None

    while True:
        try:
            r = requests.get(url).json()
        except requests.exceptions.Timeout:
            time.sleep(5)
            continue
        except requests.exceptions.TooManyRedirects as e:
            print(f"URL cannot be reached. {e}")
            break
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        else:
            break

    r = pd.DataFrame(r["tokens"])

    if data.startswith("0x"):
        ret = r.loc[r["address"] == data, ["symbol", "decimals"]]
        ret.reset_index(drop=True, inplace=True)
        return ret.loc[0]

    else:
        ret = r.loc[r["symbol"] == data, ["address", "decimals"]]
        ret.reset_index(drop=True, inplace=True)
        return ret.loc[0]


def get_abi(address):
    """
    :param address: str of abi ethereum address
    :return: string of abi
    """
    r = None
    url = URL + f"module=contract&action=getabi&address={address}&apiKey={KEY}"

    while True:
        try:
            r = requests.get(url).json()
        except requests.exceptions.Timeout:
            time.sleep(5)
            continue
        except requests.exceptions.TooManyRedirects as e:
            print(f"URL cannot be reached. {e}")
            break
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        else:
            break

    if r["status"] != "1":
        return 1
    else:
        return r["result"]


def get_transactions_by_account(account):
    """
    queries etherscan and gets all the transactions that involve a certain acount
    :param account:
    :return:
    """
    r = None

    url = (
        URL + f"module=account&action=txlist&address={account}&startblock=0&"
        f"endblock=99999999&sort=asc&apikey={KEY}"
    )
    while True:
        try:
            r = requests.get(url).json()
        except requests.exceptions.Timeout:
            time.sleep(5)
            continue
        except requests.exceptions.TooManyRedirects as e:
            print(f"URL cannot be reached. {e}")
            break
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        else:
            break

    if r["status"] != "1":
        return 1
    else:
        return r["result"]


def get_contract_src(address):
    """
    :param address: str ethereum address
    :return: [contractName, sourceCode]
    """

    r = None
    url = URL + f"module=contract&action=getsourcecode&address={address}&apiKey={KEY}"

    while True:
        try:
            r = requests.get(url).json()
        except requests.exceptions.Timeout:
            time.sleep(5)
            continue
        except requests.exceptions.TooManyRedirects as e:
            print(f"URL cannot be reached. {e}")
            break
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        else:
            break

    if r["status"] != "1":
        return 1
    else:
        return r["result"][0]['ContractName'], r["result"][0]['SourceCode']

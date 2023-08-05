import w3u


def test_erc20_address():
    assert w3u.erc20("DAI")["address"] == "0x6b175474e89094c44da98b954eedeac495271d0f"


def test_erc20_symbol():
    assert w3u.erc20("0x6b175474e89094c44da98b954eedeac495271d0f")["symbol"] == "DAI"


def test_erc20_dec():
    assert w3u.erc20("DAI")["decimals"] == 18


def test_get_transactions_by_account():
    assert (
            w3u.get_transactions_by_account("0x7fBaF24Be5Fb8eaefA5aDd9AF3F7052d3fF52E40")
            != 1
    )


def test_get_abi():
    assert w3u.get_abi("0x6b175474e89094c44da98b954eedeac495271d0f") != 1


def test_get_contract_src():
    assert w3u.get_contract_src("0x6b175474e89094c44da98b954eedeac495271d0f") != 1

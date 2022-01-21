from brownie import Lottery, accounts, config, network
from web3 import Web3

# Simple test to verify connectivity to mainnet-fork
def test_get_enterance_fee():
    # arrange
    account = accounts[0]
    
    # act
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )

    # assert
    assert lottery.getEntranceFee() > Web3.toWei(0.017, "ether")

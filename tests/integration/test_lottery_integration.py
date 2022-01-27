from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link, get_contract
from web3 import Web3
import pytest
import time

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()


    # Arrange
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entrance_fee})
    lottery.enter({"from": account, "value": entrance_fee})
    fund_with_link(lottery)

    # Act
    lottery.endLottery({"from": account})
    time.sleep(60)

    assert lottery.lastWinner() == account
    assert lottery.balance == 0


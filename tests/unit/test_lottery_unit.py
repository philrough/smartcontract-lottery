from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link, get_contract
from web3 import Web3
import pytest

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

def test_get_entrance_fee2():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()

    # Act
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()

    # Assert
    assert entrance_fee == expected_entrance_fee

def test_enter_lottery_state_throws_exception():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    # Arrange
    lottery = deploy_lottery()

    # Act
    entrance_fee = lottery.getEntranceFee()
    account = get_account()

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": account, "value": entrance_fee})
    
def test_enter_when_lottery_open():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    # Arrange
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    account = get_account()
    lottery.startLottery({"from": account})

    # Act
    lottery.enter({"from": account, "value": entrance_fee})

    # Assert
    assert lottery.players(0) == account

def test_end_when_lottery_open():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    # Arrange
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entrance_fee})
    fund_with_link(lottery)

    # Act
    lottery.endLottery({"from": account})

    # Assert
    assert lottery.lottery_state() == 2

def test_can_pick_winner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    # Arrange
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    account1 = get_account(index=0)
    account2 = get_account(index=1)
    account3 = get_account(index=2)
    lottery.startLottery({"from": account1})
    lottery.enter({"from": account1, "value": entrance_fee})
    lottery.enter({"from": account2, "value": entrance_fee})
    lottery.enter({"from": account3, "value": entrance_fee})
    fund_with_link(lottery)
    
       # Act
    end_tx = lottery.endLottery({"from": account1})
    request_id = end_tx.events["RequestedRandomness"]["requestId"]
    STATIC_RAND = 777
    get_contract("vrf_coordinator").callBackWithRandomness(request_id, STATIC_RAND, lottery.address, {"from": account1})

    # Assert
    assert lottery.lastWinner() == account1
    assert lottery.balance() == 0

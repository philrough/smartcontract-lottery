from scripts.helpful_scripts import get_account, get_contract, config, fund_with_link
from brownie import Lottery, network, config
import time

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account}
        )
    print("Deployed Lottery Contract")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery started")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    enter_tx = lottery.enter({"from": account, "value": value})
    enter_tx.wait(1)
    print("Account entered with an amount of ", value)

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    print("Now for the winner")
    ending_tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)
    time.sleep(60)
    # calculate winner
    print(f"And the winner is {lottery.lastWinner()}")




def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()


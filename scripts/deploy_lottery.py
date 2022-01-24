from scripts.helpful_scripts import get_account, get_contract, config
from brownie import Lottery, network, config

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

def main():
    deploy_lottery()

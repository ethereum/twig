# Example test file, safe to delete

import pytest


@pytest.fixture
def name_registry_package(twig_deployer):
    # returns an ethpm.package instance loaded with a "name_registry" deployment
    return twig_deployer.deploy("name_registry")


@pytest.fixture
def name_registry(name_registry_package):
    # returns a name_registry web3.contract instance
    return name_registry_package.deployments.get_instance("name_registry")


def test_name_registry_lookup(name_registry, name_registry_package):
    w3 = name_registry_package.w3
    name = b"Ongo Gablogian"
    name_registry.functions.register(name, w3.eth.accounts[0]).transact()
    registered_address = name_registry.functions.lookup(name).call()
    assert registered_address == w3.eth.accounts[0]

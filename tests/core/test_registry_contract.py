import logging

import pytest

import pytest_ethereum as pte
from pytest_ethereum.testing import Log

PACKAGE_ID = b'\xd0Y\xe8\xa6\xeaZ\x8b\xbf\x8d\xd0\x97\xa7\xb8\x92#\x16\xdc\xb7\xf0$\xe8"\x0bV\xd3\xc9\xe7\x18\x8ajv@'  # noqa: E501
V1_RELEASE_ID = b"Y^&\xf1\xb2${\xac\xc5~2\x80\x7f\x80Y\xe0\xb0\x83}\xd9\xc4~iF\x99A\x96\xbd)\xc9\xca\x97"  # noqa: E501
V2_RELEASE_ID = b"\x04Y,\xb9\xce\xd5A>\x1b\t\xe8{\x08\x9b\xf6\x96\xa0^\xfbv\xee\x87\xc8\xc4\x12Yc_\xacm\x93\x8a"  # noqa: E501

logging.getLogger("evm").setLevel(logging.INFO)


@pytest.fixture
def registry(deployer):
    pkg = deployer.deploy("registry")
    return pkg.deployments.get_contract_instance("registry")


def test_registry_init(registry, w3):
    assert registry.functions.owner().call() == w3.eth.accounts[0]


def test_registry_generate_release_id(registry):
    release_id = registry.functions.generate_release_id(b"package", b"1.0.0").call()
    assert release_id == V1_RELEASE_ID


def test_registry_release(registry):
    release_id = registry.functions.release(b"package", b"1.0.0", b"google.com").call()
    assert release_id == V1_RELEASE_ID


def test_registry_get_package_data_raises_exception_if_package_doesnt_exist(registry):
    with pte.tx_fail():
        registry.functions.get_package_data(PACKAGE_ID).call()


def test_registry_get_package_data(registry, w3):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    package_data = registry.functions.get_package_data(b'package').call()
    assert package_data[0][:7] == b"package"
    assert package_data[1] == 1
    registry.functions.release(b"package", b"1.0.1", b"google.com").transact()
    package_data_2 = registry.functions.get_package_data(b'package').call()
    assert package_data_2[0][:7] == b"package"
    assert package_data_2[1] == 2


def test_registry_get_release_id_by_package_and_count(registry):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    registry.functions.release(b"package", b"1.0.1", b"google.com").transact()
    release_id_1 = registry.functions.get_release_id_by_package_and_count(
        b"package", 1
    ).call()
    release_id_2 = registry.functions.get_release_id_by_package_and_count(
        b"package", 2
    ).call()
    assert release_id_1 == V1_RELEASE_ID
    assert release_id_2 == V2_RELEASE_ID
    with pte.tx_fail():
        registry.functions.get_release_id_by_package_and_count(b"package", 3).call()


def test_registry_logs_release_event(registry, w3):
    tx_hash = registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert Log(
        registry.events.Release,
        _package=b"package",
        _version=b"1.0.0",
        _uri=b"google.com",
    ).exact_match(receipt)


def test_registry_get_release_data(registry):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    release_data = registry.functions.get_release_data(b'package', b'1.0.0').call()
    assert release_data[0][:7] == b"package"
    assert release_data[1][:5] == b"1.0.0"
    assert release_data[2][:10] == b"google.com"


def test_registry_release_auth(registry, w3):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    with pte.tx_fail():
        registry.functions.release(b"package", b"1.0.1", b"googlex.com").transact(
            {"from": w3.eth.accounts[1]}
        )


def test_cannot_release_different_uri_for_same_version(registry):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    with pte.tx_fail():
        registry.functions.release(b"package", b"1.0.0", b"googlex.com").transact()


def test_registry_update_release(registry):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    registry.functions.release(b"package", b"1.0.1", b"yahoo.com").transact()
    release_data = registry.functions.get_release_data(b'package', b'1.0.1').call()
    assert release_data[0][:7] == b"package"
    assert release_data[1][:5] == b"1.0.1"
    assert release_data[2][:9] == b"yahoo.com"


@pytest.mark.parametrize(
    "args",
    (
        (b"package", b"", b"google.com"),
        (b"", b"1.0.0", b"google.com"),
        (b"package", b"1.0.0", b""),
    ),
)
def test_release_with_empty_values_raises_exception(registry, args):
    with pte.tx_fail():
        registry.functions.release(*args).transact()


def test_registry_transfer_owner(registry, w3):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    release_count = registry.functions.release_count().call()
    assert release_count == 1
    registry.functions.transfer_owner(w3.eth.accounts[1]).transact()
    w3.testing.mine(1)
    owner = registry.functions.owner().call()
    assert owner == w3.eth.accounts[1]
    # test you cannot release unless from owner
    with pte.tx_fail():
        registry.functions.release(b"package", b"1.0.1", b"yahoo.com").transact()
    registry.functions.release(b"package", b"1.0.1", b"yahoo.com").transact(
        {"from": w3.eth.accounts[1]}
    )
    release_count = registry.functions.release_count().call()
    assert release_count == 2


def test_registry_get_all_package_ids(registry):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    registry.functions.release(b"package", b"1.0.1", b"yahoo.com").transact()
    registry.functions.release(b"package1", b"1.0.0", b"espn.com").transact()
    registry.functions.release(b"package2", b"1.0.0", b"cnn.com").transact()
    package_count = registry.functions.package_count().call()
    release_count = registry.functions.release_count().call()
    assert package_count == 3
    assert release_count == 4
    package_id_0 = registry.functions.get_package_id(0).call()
    release_id_0 = registry.functions.get_release_id(0).call()
    release_id_1 = registry.functions.get_release_id(1).call()
    assert package_id_0 == PACKAGE_ID
    assert release_id_0 == V1_RELEASE_ID
    assert release_id_1 == V2_RELEASE_ID

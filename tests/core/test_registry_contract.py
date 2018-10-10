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


def test_registry_get_release_id(registry):
    # requires release to exist
    with pte.tx_fail():
        registry.functions.getReleaseId(b"package", b"1.0.0").call()
    with pte.tx_fail():
        registry.functions.getReleaseId(b"package", b"1.0.1").call()
    # cut releases
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    registry.functions.release(b"package", b"1.0.1", b"google.com").transact()
    v1_release_id = registry.functions.getReleaseId(b"package", b"1.0.0").call()
    v2_release_id = registry.functions.getReleaseId(b"package", b"1.0.1").call()
    assert v1_release_id == V1_RELEASE_ID
    assert v2_release_id == V2_RELEASE_ID


def test_registry_generate_release_id(registry):
    # doesn't require release to exist
    v1_release_id = registry.functions.generateReleaseId(b"package", b"1.0.0").call()
    v2_release_id = registry.functions.generateReleaseId(b"package", b"1.0.1").call()
    assert v1_release_id == V1_RELEASE_ID
    assert v2_release_id == V2_RELEASE_ID


def test_registry_get_package_name(registry):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    package_name = registry.functions.getPackageName(PACKAGE_ID).call()
    assert package_name.rstrip(b"\x00") == b"package"


def test_registry_get_package_data(registry):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    registry.functions.release(b"package", b"1.0.1", b"google1.com").transact()
    package_data = registry.functions.getPackageData(b"package").call()
    assert package_data[0].rstrip(b"\x00") == b"package"
    assert package_data[1] == PACKAGE_ID
    assert package_data[2] == 2


def test_registry_get_package_name_raises_exception_if_package_doesnt_exist(registry):
    with pte.tx_fail():
        registry.functions.getPackageName(PACKAGE_ID).call()


def test_registry_release(registry):
    release_id = registry.functions.release(b"package", b"1.0.0", b"google.com").call()
    assert release_id == V1_RELEASE_ID


def test_registry_get_all_package_ids(registry):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    registry.functions.release(b"package_2", b"1.0.0", b"cnn.com").transact()
    all_package_ids = registry.functions.getAllPackageIds(0, 5).call()
    assert all_package_ids[0] == PACKAGE_ID
    assert all_package_ids[1] != b"\x00" * 32
    assert all_package_ids[2] == b"\x00" * 32
    assert all_package_ids[3] == b"\x00" * 32
    assert all_package_ids[4] == b"\x00" * 32
    # test with different offset
    all_offset_ids = registry.functions.getAllPackageIds(1, 5).call()
    assert all_offset_ids[0] != b"\x00" * 32
    assert all_offset_ids[1] == b"\x00" * 32
    assert all_offset_ids[2] == b"\x00" * 32
    assert all_offset_ids[3] == b"\x00" * 32
    assert all_offset_ids[4] == b"\x00" * 32
    # offset must be less than total package count
    with pte.tx_fail():
        registry.functions.getAllPackageIds(3, 5).call()
    # length variable must be 5
    with pte.tx_fail():
        registry.functions.getAllPackageIds(1, 6).call()


def test_registry_get_all_release_ids(registry):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    registry.functions.release(b"package", b"1.0.1", b"google1.com").transact()
    registry.functions.release(b"package", b"1.1.0", b"google2.com").transact()
    all_release_ids = registry.functions.getAllReleaseIds(b"package", 0, 5).call()
    assert all_release_ids[0] == V1_RELEASE_ID
    assert all_release_ids[1] == V2_RELEASE_ID
    assert all_release_ids[2] != b"\x00" * 32
    assert all_release_ids[3] == b"\x00" * 32
    assert all_release_ids[4] == b"\x00" * 32
    # test with offset
    all_release_ids = registry.functions.getAllReleaseIds(b"package", 2, 5).call()
    assert all_release_ids[0] != b"\x00" * 32
    assert all_release_ids[1] == b"\x00" * 32
    assert all_release_ids[2] == b"\x00" * 32
    assert all_release_ids[3] == b"\x00" * 32
    assert all_release_ids[4] == b"\x00" * 32
    # length input arg must be 5
    with pte.tx_fail():
        registry.functions.getAllReleaseIds(b"package", 0, 4).call()
    # package must exist
    with pte.tx_fail():
        registry.functions.getAllReleaseIds(b"invalid", 0, 5).call()
    # offset must be below package release count
    with pte.tx_fail():
        registry.functions.getAllReleaseIds(b"package", 4, 5).call()


def test_registry_get_release_data(registry):
    registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    registry.functions.release(b"package", b"1.0.1", b"google1.com").transact()
    v1_data = registry.functions.getReleaseData(V1_RELEASE_ID).call()
    v2_data = registry.functions.getReleaseData(V2_RELEASE_ID).call()
    assert v1_data[0].rstrip(b"\x00") == b"package"
    assert v1_data[1].rstrip(b"\x00") == b"1.0.0"
    assert v1_data[2].rstrip(b"\x00") == b"google.com"
    assert v2_data[0].rstrip(b"\x00") == b"package"
    assert v2_data[1].rstrip(b"\x00") == b"1.0.1"
    assert v2_data[2].rstrip(b"\x00") == b"google1.com"


def test_registry_logs_release_event(registry, w3):
    tx_hash = registry.functions.release(b"package", b"1.0.0", b"google.com").transact()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert Log(
        registry.events.Release,
        _package=b"package",
        _version=b"1.0.0",
        _uri=b"google.com",
    ).exact_match(receipt)


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
    release_data = registry.functions.getReleaseData(V2_RELEASE_ID).call()
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
    release_count = registry.functions.releaseCount().call()
    assert release_count == 1
    registry.functions.transferOwner(w3.eth.accounts[1]).transact()
    w3.testing.mine(1)
    owner = registry.functions.owner().call()
    assert owner == w3.eth.accounts[1]
    # test you cannot release unless from owner
    with pte.tx_fail():
        registry.functions.release(b"package", b"1.0.1", b"yahoo.com").transact()
    registry.functions.release(b"package", b"1.0.1", b"yahoo.com").transact(
        {"from": w3.eth.accounts[1]}
    )
    release_count = registry.functions.releaseCount().call()
    assert release_count == 2

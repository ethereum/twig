# Events
Release: event({_package: indexed(bytes32), _version: bytes32, _uri: bytes32})

owner: public(address)

# Package Data: (package_id => value)
packages: public(
    {
        exists: bool,
        created_at: timestamp,
        updated_at: timestamp,
        name: bytes32,
        release_count: int128,
    }[bytes32]
)

#  Release Data: (release_id => value)
releases: public(
    {
        exists: bool,
        created_at: timestamp,
        package_id: bytes32,
        version: bytes32,
        uri: bytes32,
    }[bytes32]
)


# package_id#release_count => release_id
package_release_index: bytes32[bytes32]
# Total number of packages in registry
package_count: public(int128)
# Total number of releases in registry
release_count: public(int128)
# Total package number (int128) => package_id (bytes32)
package_ids: bytes32[int128]
# Total release number (int128) => release_id (bytes32)
release_ids: bytes32[int128]

EMPTY_BYTES: bytes32


@public
def __init__():
    self.owner = msg.sender


@public
def transfer_owner(new_owner: address):
    """
    Change ownership of contract.
    """
    assert self.owner == msg.sender
    self.owner = new_owner


@public
def generate_release_id(name: bytes32, version: bytes32) -> bytes32:
    """
    Return the `release_id` associated with a given package name and release version.
    """
    release_concat: bytes[64] = concat(name, version)
    release_id: bytes32 = sha3(release_concat)
    return release_id


@public
def get_package_data_by_id(package_id: bytes32) -> (bytes32, int128):
    """
    Return a package name and release count associated with a given `package_id`.
    # todo refactor w/ get_package_data
    """
    assert self.packages[package_id].exists == True
    return (self.packages[package_id].name, self.packages[package_id].release_count)


@public
def get_package_data(name: bytes32) -> (bytes32, int128):
    """
    Return a package name and release count associated with a given package name.
    """
    package_id: bytes32 =  sha3(name)
    assert self.packages[package_id].exists == True
    return (self.packages[package_id].name, self.packages[package_id].release_count)


@public
def get_release_data_by_id(release_id: bytes32) ->  (bytes32, bytes32, bytes32, bytes32):
    assert self.releases[release_id].exists == True
    package_name: bytes32 = self.packages[self.releases[release_id].package_id].name
    version: bytes32 = self.releases[release_id].version
    uri: bytes32 = self.releases[release_id].uri
    return (package_name, version, uri, release_id)


@public
def get_release_data(name: bytes32, release_version: bytes32) -> (bytes32, bytes32, bytes32, bytes32):
    """
    Return package name, release version, and manifest uri associated with a given `release_id`.
    todo refactor with get-release_data_by_id
    """
    release_id: bytes32 = self.generate_release_id(name, release_version)
    assert self.releases[release_id].exists == True
    package_name: bytes32 = self.packages[self.releases[release_id].package_id].name
    version: bytes32 = self.releases[release_id].version
    uri: bytes32 = self.releases[release_id].uri
    return (package_name, version, uri, release_id)


@public
def get_package_id(index: int128) -> bytes32:
    """
    Return the `package_id` associated with the package identified by the given index.
    """
    assert index <= self.package_count
    return self.package_ids[index]


@public
def get_release_id(index: int128) -> bytes32:
    """
    Return the `release_id` associated with the release identified by the given index.
    """
    assert index <= self.release_count
    return self.release_ids[index]


@private
def generate_package_release_id(package_id: bytes32, count: int128) -> bytes32:
    """
    Create the package_release_id associated with a given package_id and a release count.
    """
    count_bytes: bytes32 = convert(count, "bytes32")
    package_release_tag: bytes[64] = concat(package_id, count_bytes)
    package_release_id: bytes32 = sha3(package_release_tag)
    return package_release_id


@public
def get_release_id_by_package_and_count(name: bytes32, count: int128) -> bytes32:
    """
    Return the `release_id` associated with a given package name and release count.
    """
    package_id: bytes32 = sha3(name)
    assert self.packages[package_id].exists
    assert count <= self.packages[package_id].release_count
    package_release_id: bytes32 = self.generate_package_release_id(package_id, count)
    return self.package_release_index[package_release_id]


@private
def cut_release(
    release_id: bytes32,
    package_id: bytes32,
    version: bytes32,
    uri: bytes32,
    name: bytes32,
):
    self.releases[release_id] = {
        exists: True,
        created_at: block.timestamp,
        package_id: package_id,
        version: version,
        uri: uri,
    }
    self.packages[package_id].release_count += 1
    self.release_ids[self.release_count] = release_id
    self.release_count += 1
    package_release_id: bytes32 = self.generate_package_release_id(package_id, self.packages[package_id].release_count)
    self.package_release_index[package_release_id] = release_id
    log.Release(name, version, uri)


@public
def release(name: bytes32, version: bytes32, uri: bytes32) -> bytes32:
    """
    Return a relase_id after publishing a release.
    """
    assert uri != self.EMPTY_BYTES
    assert name != self.EMPTY_BYTES
    assert version != self.EMPTY_BYTES
    assert self.owner == msg.sender

    package_id: bytes32 = sha3(name)
    release_id: bytes32 = self.generate_release_id(name, version)

    if self.packages[package_id].exists == True:
        self.packages[package_id] = {
            exists: True,
            created_at: self.packages[package_id].created_at,
            updated_at: block.timestamp,
            name: name,
            release_count: self.packages[package_id].release_count,
        }
        assert self.releases[release_id].exists == False
        self.cut_release(release_id, package_id, version, uri, name)
        return release_id
    else:
        self.packages[package_id] = {
            exists: True,
            created_at: block.timestamp,
            updated_at: block.timestamp,
            name: name,
            release_count: 0,
        }
        self.package_ids[self.package_count] = package_id
        self.package_count += 1
        self.cut_release(release_id, package_id, version, uri, name)
        return release_id

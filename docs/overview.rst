Overview
========


Start your own Vyper project
----------------------------

Twig lets you write tests using `web3.py <https://github.com/ethereum/web3.py/>`__ and `pytest-ethereum <https://github.com/ethereum/pytest-ethereum>`__ against your `Vyper <https://github.com/ethereum/vyper>`__ smart contracts.


Twig setup
~~~~~~~~~~

- clone twig repo
- ``python -m venv venv`` (note: requires >=python3.6)
- ``. venv/bin/activate``
- ``pip install -e .``


Project setup
~~~~~~~~~~~~~

.. NOTE:: ``contracts/name_registry.vy`` and ``tests/test_name_registry.py`` have been included as examples on how to get started, but are safe to delete.

- create your vyper contract file in ``contracts/``
  (i.e. ``root/contracts/example.vy``)

- write your vyper contract test file in ``tests/``
  (i.e. ``root/tests/test_example.py``)

- create your contract instance to test against using ``pytest-ethereum``'s `deployer <https://pytest-ethereum.readthedocs.io/en/latest/overview.html#deployer`__. In the following example, the ``my_contract`` fixture returns a ``web3.contract`` instance for testing against.

.. code:: python

   @pytest.fixture
   def my_contract_package(twig_deployer):
       # returns an ethpm.Package instance loaded with a "my_contract" deployment on the ethpm.Package.w3 instance
       return twig_deployer.deploy("my_contract")

   @pytest.fixture
   def my_contract(my_contract_package):
       # returns an my_contract web3.contract instance to test against
       return my_contract_package.deployments.get_instance("my_contract")

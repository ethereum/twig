Overview
========


Start your own Vyper project
----------------------------

Twig lets you write tests using ``web3.py`` and ``pytest-ethereum`` against your ``Vyper`` smart contracts.


Twig setup
~~~~~~~~~~

- clone twig repo
- ``python -m venv venv`` (note: requires python3.6)
- ``. venv/bin/activate``
- ``pip install -e .``


Project setup
~~~~~~~~~~~~~

.. NOTE:: ``twig/contracts/name_registry.vy`` and ``tests/contracts/test_name_registry.py`` have been included as examples on how to get started, but are safe to delete.

- create your vyper contract file in ``twig/contracts/``
  (i.e. ``twig/contracts/example.vy``)

- write your vyper contract test file in ``tests/contracts/``
  (i.e. ``twig/contracts/test_example.py``)

- create your contract's ``Deployer`` fixture in your test file.

.. code:: python

   @pytest.fixture
   def example_package(deployer):
       # returns an ethpm.Package instance loaded with a "example" deployment on the ethpm.Package.w3 instance
       return deployer.deploy("example")
    
   @pytest.fixture
   def example(example_package):
       # returns an example web3.contract instance
       return example_package.deployments.get_instance("example")



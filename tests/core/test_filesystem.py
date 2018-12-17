from twig.filesystem import collect_sources


def test_collect_sources(test_contracts_dir):
    sources = collect_sources(test_contracts_dir)
    filenames = [source.name for source in sources]
    assert set(filenames) == set(
        ["registry.vy", "simple_open_auction.vy", "crowdfund.vy"]
    )

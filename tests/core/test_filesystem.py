from twig.filesystem import collect_sources


def test_collect_sources(tmp_contracts):
    sources = collect_sources(tmp_contracts)
    filenames = [source.name for source in sources]
    assert set(filenames) == set(
        ["registry.vy", "simple_open_auction.vy", "crowdfund.vy"]
    )

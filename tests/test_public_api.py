from elosam.application import EloSam


def test_public_api_exists() -> None:
    app = EloSam()

    assert app is not None

    assert hasattr(app, "execute")

    assert hasattr(app, "runtime")
import pytest

from elosam.builder.models import BuildSpecification
from elosam.builder.validator import ValidationError
from elosam.builder.validator import Validator


def test_validator_accepts_valid_specification() -> None:
    Validator().validate(
        BuildSpecification(
            kind="capability",
            name="vision",
        )
    )


def test_validator_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        Validator().validate(
            BuildSpecification(
                kind="capability",
                name="",
            )
        )
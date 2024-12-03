import pytest
from src.app.main import get_the_tallest_character, GenderEnum

@pytest.mark.asyncio
@pytest.mark.parametrize("gender, has_work", [
    pytest.param(GenderEnum.female, True, id="Woman with work"),
    pytest.param(GenderEnum.male, True, id="Man with work"),
    pytest.param(GenderEnum.female, False, id="Woman without work"),
    pytest.param(GenderEnum.male, False, id="Man without work"),
])
async def test_get_the_tallest_character(gender, has_work):
    tallest_hero = await get_the_tallest_character(gender, has_work)

    assert tallest_hero is not None
    assert tallest_hero.get("appearance").get("gender") == gender.value
    assert (tallest_hero.get("work").get("occupation") not in [None, "-"]) == has_work

 
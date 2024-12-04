import pytest
from pytest_mock import MockerFixture
from fastapi import HTTPException
from httpx import Response
from src.app.main import get_the_tallest_character, GenderEnum


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "gender, has_work",
    [
        pytest.param(GenderEnum.female, True, id="Woman with work"),
        pytest.param(GenderEnum.male, True, id="Man with work"),
        pytest.param(GenderEnum.female, False, id="Woman without work"),
        pytest.param(GenderEnum.male, False, id="Man without work"),
    ],
)
async def test_get_the_tallest_character(gender, has_work):
    tallest_hero = await get_the_tallest_character(gender, has_work)

    assert tallest_hero is not None
    assert tallest_hero.get("appearance").get("gender") == gender.value
    assert (tallest_hero.get("work").get("occupation") not in [None, "-"]) == has_work


@pytest.mark.asyncio
async def test_api_failure(mocker: MockerFixture):
    mock_get = mocker.patch(
        "httpx.AsyncClient.get",
        return_value=Response(status_code=500, text="failed to load data from API"),
    )
    with pytest.raises(HTTPException) as ex:
        await get_the_tallest_character(GenderEnum.male, True)

    assert ex.value.status_code == 500
    assert ex.value.detail == "failed to load data from API"

    mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_no_match_heroes(mocker: MockerFixture):
    mock_get = mocker.patch(
        "httpx.AsyncClient.get",
        return_value=Response(
            status_code=200,
            json=[
                {"appearance": {"gender": "Female"}, "work": {"occupation": "-"}},
                {"appearance": {"gender": "Male"}, "work": {"occupation": "-"}},
            ],
        ),
    )

    result = await get_the_tallest_character(GenderEnum.male, True)

    assert result is None
    mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_no_heroes(mocker: MockerFixture):
    mock_get = mocker.patch(
        "httpx.AsyncClient.get", return_value=Response(status_code=200, json=[])
    )

    result = await get_the_tallest_character(GenderEnum.male, True)

    assert result is None
    mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_two_heroes(mocker: MockerFixture):
    mock_get = mocker.patch(
        "httpx.AsyncClient.get",
        return_value=Response(
            status_code=200,
            json=[
                {
                    "appearance": {"gender": "Female", "height": ["6'2", "188 cm"]},
                    "work": {"occupation": "teacher"},
                },
                {
                    "appearance": {"gender": "Female", "height": ["6'2", "188 cm"]},
                    "work": {"occupation": "cowboy"},
                },
            ],
        ),
    )

    result = await get_the_tallest_character(GenderEnum.female, True)

    assert result.get("work").get("occupation") == "teacher"
    mock_get.assert_called_once()

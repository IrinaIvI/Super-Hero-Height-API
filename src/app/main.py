from fastapi import FastAPI, HTTPException
from typing import Optional
import httpx

app = FastAPI()

URL = "https://akabab.github.io/superhero-api/api/all.json"


@app.get("/")
async def get_the_tallest_character(gender: str, has_work: bool) -> Optional[dict]:
    """Функция по вычислению самого высокого героя."""
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="failed to load data from API")

        heroes = response.json()

        filtered_heroes = [
            hero
            for hero in heroes
            if hero.get("appearance", {}).get("gender") == gender
            and (hero.get("work", {}).get("occupation") not in [None, "-"]) == has_work
        ]

        if not filtered_heroes:
            return None

        tallest_hero = max(
            filtered_heroes,
            key=lambda hero: float(
                hero.get("appearance").get("height")[1].split(" ")[0]
            ),
        )

        return tallest_hero

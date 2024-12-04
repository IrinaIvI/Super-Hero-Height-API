from fastapi import FastAPI, HTTPException
from typing import Optional
from enum import Enum
from httpx import AsyncClient
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

URL = "https://akabab.github.io/superhero-api/api/all.json"


class GenderEnum(Enum):
    """Перечисление гендера."""
    male = "Male"
    female = "Female"

def parse_height(height_str: str) -> float:
    if height_str and "-" not in height_str:
        if "'" in height_str:
            feet, inches = height_str.split("'")[:2]
            feet = float(feet.strip())  

            inches = inches.strip()
            if inches:
                inches = float(inches)  
            else:
                inches = 0.0 
        else:
            feet = float(height_str)
            inches = 0.0

        return feet * 12 + inches
    
    return 0.0


@app.get("/")
async def get_the_tallest_character(gender: GenderEnum, has_work: bool) -> Optional[dict] :
    """Функция по вычислению самого высокого героя."""

    async with AsyncClient() as client:
        response = await client.get(URL)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="failed to load data from API")

        heroes = response.json()

        filtered_heroes = [
            hero
            for hero in heroes
            if hero.get("appearance", {}).get("gender") == gender.value
            and (hero.get("work", {}).get("occupation") not in [None, "-"]) == has_work
        ]

        if not filtered_heroes:
            return None

        tallest_hero = max(
            filtered_heroes,
            key=lambda hero: 
            max(float(hero.get("appearance").get("height")[1].split(" ")[0]), parse_height(hero.get("appearance").get("height")[0].split(" ")[0])),
        )

        return tallest_hero

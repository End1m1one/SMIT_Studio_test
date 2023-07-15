from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from models import Rate
from tortoise_config import TORTOISE_ORM
import json


app = FastAPI()

with open("rates.json", "r") as file:
    rates_data = json.load(file)

# Инициализация базы данных и подключение модели
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


# Модель данных для POST-запроса
class CalculationInput(BaseModel):
    date: str
    cargo_type: str
    declared_price: str


# Маршрут для обработки POST-запросов
@app.post("/calc")
async def calculate_cost(input_data: CalculationInput):
    try:
        # Получение даты, типа груза и заявленной цены из запроса
        date = input_data.date
        cargo_type = input_data.cargo_type
        declared_price = float(input_data.declared_price)

        # Получение ставки из данных о ставках
        rates = rates_data.get(date)
        if rates:
            for rate in rates:
                if rate["cargo_type"] == cargo_type:
                    rate_value = float(rate["rate"])
                    cost = declared_price * rate_value
                    return JSONResponse(content={"cost": str(cost)})

        # Если ставка не найдена
        return JSONResponse(content={"error": "Rate not found"})
    except Exception as e:
        # Обработка ошибок
        error_message = str(e) if str(e) else "Unknown error occurred"
        raise HTTPException(status_code=400, detail={"error": error_message})


async def init_models():
    await Rate.all().first()


@app.on_event("startup")
async def startup_event():
    await init_models()

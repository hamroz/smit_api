import datetime
from fastapi import FastAPI, HTTPException, Body, status
from fastapi.exceptions import RequestValidationError
from tortoise.contrib.fastapi import register_tortoise
from starlette.responses import PlainTextResponse
from starlette.requests import Request
from models import Tariff
from schemas import CargoRate, TariffIn, TariffUpdate, InsuranceIn
from typing import List, Dict

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(str(exc.errors()), status_code=400)


@app.get("/tariffs/")
async def get_all_tariffs():
    return await Tariff.all().values()


@app.get("/tariffs/{id}")
async def get_tariff(id: int):
    tariff = await Tariff.filter(id=id).first()
    if not tariff:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return tariff


@app.post("/load_tariffs/", status_code=status.HTTP_201_CREATED)
async def load_tariffs(tariffs: Dict[str, List[CargoRate]] = Body(..., embed=False)):
    for date, tariff_list in tariffs.items():
        for tariff in tariff_list:
            existing_tariff = await Tariff.filter(
                date=date, cargo_type=tariff.cargo_type
            ).first()
            if existing_tariff:
                return {
                    "status": "error",
                    "message": "A record with the same date and cargo type already exists.",
                }
            await Tariff.create(
                date=date, cargo_type=tariff.cargo_type, rate=tariff.rate
            )
    return {"status": "tariffs loaded"}


@app.post("/calculate_insurance/{id}")
async def calculate_insurance(id: int, insurance: InsuranceIn):
    tariff = await Tariff.filter(id=id).first()
    if not tariff:
        raise HTTPException(status_code=404, detail="Tariff not found")
    insurance_cost = tariff.rate * insurance.declared_value
    return {
        "id": tariff.id,
        "date": str(tariff.date),
        "cargo_type": tariff.cargo_type,
        "rate": tariff.rate,
        "insurance_cost": insurance_cost,
    }


@app.put("/update_tariff/{id}")
async def update_tariff(id: int, tariff_update: TariffUpdate):
    tariff = await Tariff.filter(id=id).first()
    if not tariff:
        raise HTTPException(status_code=404, detail="Tariff not found")
    if tariff_update.rate is not None:
        tariff.rate = tariff_update.rate
    if tariff_update.cargo_type is not None:
        tariff.cargo_type = tariff_update.cargo_type
    if tariff_update.date is not None:
        try:
            tariff.date = datetime.datetime.strptime(
                tariff_update.date, "%Y-%m-%d"
            ).date()
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. It should be YYYY-MM-DD."
            )
    await tariff.save()
    return {"status": "tariff updated"}


@app.delete("/delete_tariff/{id}")
async def delete_tariff(id: int):
    tariff = await Tariff.filter(id=id).first()
    if not tariff:
        raise HTTPException(status_code=404, detail="Tariff not found")
    await tariff.delete()
    return {"status": "tariff deleted"}


register_tortoise(
    app,
    db_url="postgres://uca_rec_user:Elephant@123@localhost:5432/test",
    modules={"models": ["main"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI(title="Inventory Management API")

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]


class Product(BaseModel):
    ProductID: int
    Name: str
    UnitPrice: float = Field(gt=0)
    StockQuantity: int = Field(ge=0)
    Description: str


def clean(doc):
    doc.pop("_id", None)
    return doc


@app.get("/getSingleProduct")
def get_single_product(product_id: int):
    product = collection.find_one({"ProductID": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return clean(product)


@app.get("/getAll")
def get_all():
    products = list(collection.find())
    return [clean(p) for p in products]


@app.post("/addNew")
def add_new(product: Product):
    existing = collection.find_one({"ProductID": product.ProductID})
    if existing:
        raise HTTPException(status_code=400, detail="ProductID already exists")
    collection.insert_one(product.dict())
    return {"message": "Product added successfully", "ProductID": product.ProductID}


@app.delete("/deleteOne")
def delete_one(product_id: int):
    result = collection.delete_one({"ProductID": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product {product_id} deleted"}


@app.get("/startsWith")
def starts_with(letter: str):
    if len(letter) != 1 or not letter.isalpha():
        raise HTTPException(status_code=400, detail="Please provide a single letter")
    regex = f"^{letter}"
    products = list(collection.find({"Name": {"$regex": regex, "$options": "i"}}))
    return [clean(p) for p in products]


@app.get("/paginate")
def paginate(start_id: int, end_id: int):
    products = list(
        collection.find({"ProductID": {"$gte": start_id, "$lte": end_id}})
        .sort("ProductID", 1)
        .limit(10)
    )
    return [clean(p) for p in products]


@app.get("/convert")
def convert(product_id: int):
    product = collection.find_one({"ProductID": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        rate = response.json()["rates"]["EUR"]
    except Exception:
        raise HTTPException(status_code=503, detail="Could not fetch exchange rate")
    price_usd = product["UnitPrice"]
    price_eur = round(price_usd * rate, 2)
    return {
        "ProductID": product_id,
        "Name": product["Name"],
        "PriceUSD": price_usd,
        "PriceEUR": price_eur,
        "ExchangeRate": rate
    }


from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
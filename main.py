
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import redis
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="frontend/templates")
# Verbindung zur KeyDB-Instanz (ersetze HOST und PORT durch die tatsächlichen Werte)
redis_host = 'keydb'  # Beispiel: 'localhost'
redis_port = 6379  # Beispiel: 6379
rdb = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

class Item(BaseModel):
    name: str


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/item")
async def create_item(item: Item):
    # Erstelle ein neues Element in der KeyDB
    item_id = rdb.incr("item_id_counter")
    key = f"item:{item_id}"
    rdb.hset(key, "name", item.name)
    return {"item_id": item_id, "name": item.name}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # Lies ein Element aus der KeyDB
    key = f"item:{item_id}"
    name = rdb.hget(key, "name")
    if name is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "name": name}

@app.get("/items/", response_model=list)
async def read_all_items():
    # Hier liest du alle Items aus der KeyDB
    items = []
    item_keys = rdb.keys("item:*")
    for key in item_keys:
        item_id = key.split(":")[-1]
        item = rdb.hgetall(key)
        items.append({"item_id": item_id, **item})
    return items
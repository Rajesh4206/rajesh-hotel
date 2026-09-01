from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI(title="Rajesh Hotel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup - permanent dabba
engine = create_engine("sqlite:///./hotel.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

class OrderTable(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)

Base.metadata.create_all(bind=engine)

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def home():
    return {"message": "Rajesh Hotel API is Live ra!"}

@app.post("/order")
def create_order(item: Item):
    db = Session()
    new_order = OrderTable(name=item.name, price=item.price)
    db.add(new_order)
    db.commit()
    db.close()
    return {"message": f"{item.name} saved to REAL DB!"}

@app.get("/all-orders")
def get_all_orders():
    db = Session()
    orders = db.query(OrderTable).all()
    db.close()
    return orders

@app.delete("/order/{order_id}")
def delete_order(order_id: int):
    db = Session()
    order = db.query(OrderTable).filter(OrderTable.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
        db.close()
        return {"message": f"Order {order_id} deleted ra!"}
    else:
        db.close()
        return {"message": "Id dorakaledu ra!"}

@app.put("/order/{order_id}")
def update_order(order_id: int, item: Item):
    db = Session()
    order = db.query(OrderTable).filter(OrderTable.id == order_id).first()
    if order:
        order.name = item.name
        order.price = item.price
        db.commit()
        db.close()
        return {"message": f"Order {order_id} updated!"}
    else:
        db.close()
        return {"message": "Id dorakaledu!"}

@app.get("/search")
def search_order(name: str):
    db = Session()
    orders = db.query(OrderTable).filter(OrderTable.name.ilike(f"%{name}%")).all()
    db.close()
    return orders

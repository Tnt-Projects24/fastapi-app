from fastapi import Depends,FastAPI
#import models.py
from models import Product
from database import DBSession, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()


database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome Siva"

#products = [
   #Product(1,"phone","sansumg",99,10),
   #Product(2,"tv","lg",99,10),
products = [
    Product(
        id=1,
        name="Galaxy Phone",
        description="Samsung Galaxy smartphone",
        price=699.99,
        quantity=12
    ),
    Product(
        id=2,
        name="Dell Laptop",
        description="Dell 14-inch business laptop",
        price=1299.99,
        quantity=8
    ),
    Product(
        id=3,
        name="LG Smart TV",
        description="LG 55-inch 4K Smart TV",
        price=899.99,
        quantity=6
    ),
    Product(
        id=4,
        name="Apple Watch",
        description="Apple Watch Series smartwatch",
        price=399.99,
        quantity=15
    ),
    Product(
        id=5,
        name="Sony Headphones",
        description="Sony wireless noise-canceling headphones",
        price=349.99,
        quantity=10 
    ),
]

def get_db():
    db =DBSession()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = DBSession() 
    count = db.query(database_models.Product).count()
    print ("TOTAL=",count)
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
   
    db_products= db.query(database_models.Product).all()
    return db_products #products


@app.get("/products/{id}")
def get_product_by_id(id: int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
       return db_product
    return "Product not found"


@app.post("/products")
def add_produt(product: Product, db: Session = Depends(get_db)):
    #products.append (product)
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products")
def update_produt(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return f"Product {product.id} updated successfully"
    else:
        return "product not found"
#    for i in range (len(products)):
#        if products[i].id == id:
#            products[i] = product
#            return "Product updated successfuly"
#    return "No product found"



@app.delete("/products")
def delete_produt(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
       db.delete(db_product)
       db.commit()
       return f"Product {id} removed successfully"
    # for i in range (len(products)):
    #     if products[i].id == id:
    #         del products[i]
    #         return "Product deleted successfuly"
    return "No product found"
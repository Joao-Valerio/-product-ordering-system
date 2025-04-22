from peewee import *
from datetime import datetime

myDb = SqliteDatabase('dados.db')

class BaseModel(Model):
    class Meta:
        database = myDb

class User(BaseModel):
    name = CharField()
    cpf = CharField(unique=True)


class Product(BaseModel):
    productName = CharField()
    price = TextField()
    
class Order(BaseModel):
   user = ForeignKeyField(User, backref='pedidos')
   orderDate = DateTimeField(default=datetime.now)
   totalPrice = FloatField()

class productOrder(BaseModel):
    pedido = ForeignKeyField(Order, backref='itens')
    produto = ForeignKeyField(Product)
    quantidade = IntegerField(default=1)

myDb.connect()
myDb.create_tables([User, Product, Order, productOrder])
from services.db_service import db_service
from datetime import datetime
from models import User, Restaurant, Category, Dish, SideDish, Table, Waiter, SideDishOptions, Order, OrderDetail
import random

names = ["Pepe", "Juan", "Pablo", "Fede", "Marcos", "Martin", "Monica", "Lucia", "Paola", "Victoria", "Martina", "Daniela", "Agostina", "Agustin", "Gustavo", "La Meles"]
order_states = ["processing", "waiting", "preparation", "cancelled", "delivered"]
platos_pricipales = ["Milanesa al plato", "Huevo frito", "Sushi", "Pollo a la mostaza", "Tortilla de papa", "Pizza"]
sanguches = ["Pebete", "Lomito", "Lomo ultra mega XXL", "Pizzalomo", "Sanguche de milanesa", "Hamburgesa", "Hamburguesa de hongos"]
pastas = ["Fideos con tuco", "Lasagña", "Ravioles caseros", "Sorrentinos"]
rellenos = [ "Tarta de acelga", "Tarta de choclo", "Empanadas criollas", "Empanadas arabes", "Empandas de atun", "Empanadas de pollo", "Empanadas de acelga", "Empanadas de soja", "Tacos"]
side_dishes = ["Papas fritas", "Pure", "Ensalada", "Papas al horno", "Ensalada rusa", "Rabas"]
drinks = ["Cocucha bien fria", "Priteado", "Prity", "Fernandito", "Birrita bien helada", "Levite", "Jugo de naranja exprimida", "Limonada", "Agua mineral","Gin tonic", "Sprite", "Fanta"]

def create_mocks_in_db():
    db_service.create_object(User(id = 1, user = "admin", password = "admin", email = "admin@seminario.com"))
    db_service.create_object(Restaurant(id = 1, name = "Pepe", last_name = "Argento", user = 1))
    db_service.create_object(Category(id = 1, name = "Bebidas", restaurant = 1))
    db_service.create_object(Category(id = 2, name = "Sanguches", restaurant = 1))
    db_service.create_object(Category(id = 3, name = "Pastas", restaurant = 1))
    db_service.create_object(Category(id = 4, name = "Rellenos", restaurant = 1))
    db_service.create_object(Category(id = 5, name = "Platos principales", restaurant = 1))
    for i in range(6):
        db_service.create_object(Dish(id = 1+5*i,name = random.choice(platos_pricipales),description = "Wea re rica",preparation_time = random.randint(15,45),category = 5,price = random.randint(2000,7000)))
        db_service.create_object(Dish(id = 2+5*i,name = random.choice(sanguches),description = "Wea re grasosa",preparation_time = random.randint(5,30),category = 2,price = random.randint(1000,5000)))
        db_service.create_object(Dish(id = 3+5*i,name = random.choice(pastas),description = "Como los que hacia la nona :(",preparation_time = random.randint(20,45),category = 3,price = random.randint(3000,8000)))
        db_service.create_object(Dish(id = 4+5*i,name = random.choice(rellenos),description = "Wea re ancha",reparation_time = random.randint(5,30),category = 4,price = random.randint(1500,3000)))
        db_service.create_object(Dish(id = 5+5*i,name = random.choice(drinks),description = "Wea re refrescante",preparation_time = random.randint(0,5),category = 1,price = random.randint(700,4000)))
        db_service.create_object(SideDish(id = 1+2*i,name = random.choice(side_dishes),description = "Wea para acompañar",extra_price = random.randint(500,1500)))
        db_service.create_object(SideDish(id = 2+2*i,name = random.choice(side_dishes),description = "Wea para acompañar",extra_price = random.randint(500,1500)))
        db_service.create_object(SideDishOptions(dish = 1+5*i,side_dish = 1+2*i))
        db_service.create_object(SideDishOptions(dish = 2+5*i,side_dish = 2+2*i))
    for i in range(15):
        db_service.create_object(Table(restaurant = 1))
    for i in range(3):
        db_service.create_object(Waiter(name = random.choice(names)))
    for i in range(10):
        price = random.randint(2000,7000)
        db_service.create_object(Order(id = i, table = random.randint(1,15) , total = price, created_at = datetime.now(), state = random.choice(order_states)))
        db_service.create_object(OrderDetail(dish_selected = random.randint(1,35), order = i, subtotal = price, customer = random.choice(names)))

    

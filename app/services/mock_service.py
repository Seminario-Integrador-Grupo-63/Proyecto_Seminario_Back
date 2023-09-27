from services.db_service import db_service
from datetime import datetime
from sqlmodel import select
from models import User, Restaurant, Category, Dish, SideDish, Table, Waiter, SideDishOptions, Order, OrderDetail
import random

names = ["Pepe", "Juan", "Pablo", "Fede", "Marcos", "Martin", "Monica", "Lucia", "Paola", "Victoria", "Martina", "Daniela", "Agostina", "Agustin", "Gustavo", "La Meles"]
order_states_names = ["processing", "waiting", "preparation", "cancelled", "delivered"]
platos_pricipales_names = ["Milanesa al plato", "Huevo frito", "Sushi", "Pollo a la mostaza", "Tortilla de papa", "Pizza"]
sanguches_names = ["Pebete", "Lomito", "Lomo ultra mega XXL", "Pizzalomo", "Sanguche de milanesa", "Hamburgesa", "Hamburguesa de hongos"]
pastas_names = ["Fideos con tuco", "Lasagña", "Ravioles caseros", "Sorrentinos"]
rellenos_names = [ "Tarta de acelga", "Tarta de choclo", "Empanadas criollas", "Empanadas arabes", "Empandas de atun", "Empanadas de pollo", "Empanadas de acelga", "Empanadas de soja", "Tacos"]
side_dishes_names = ["Papas fritas", "Pure", "Ensalada", "Papas al horno", "Ensalada rusa", "Rabas"]
drinks_names = ["Cocucha bien fria", "Priteado", "Prity", "Fernandito", "Birrita bien helada", "Levite", "Jugo de naranja exprimida", "Limonada", "Agua mineral","Gin tonic", "Sprite", "Fanta"]

def create_mocks_in_db():

    #Crear restaurante
    restaurant_1 = Restaurant(name = "Pepe", last_name = "Argento")
    db_service.create_object(restaurant_1)

    #Crear usuario
    statement = select(Restaurant).where(Restaurant.name == "Pepe")
    restaurant: Restaurant = db_service.get_with_filters(statement)[0]
    user_1 = User(user = "admin", password = "admin", email = "admin@seminario.com", role = "admin", restaurant = restaurant.id)
    db_service.create_object(user_1)

    #Crear categorias
    statement = select(Restaurant).where(Restaurant.name == "Pepe")
    restaurant: Restaurant = db_service.get_with_filters(statement)[0]
    category_1 = Category(name = "Bebidas", restaurant = restaurant.id)
    category_2 = Category(name = "Sanguches", restaurant = restaurant.id)
    category_3 = Category(name = "Pastas", restaurant = restaurant.id)
    category_4 = Category(name = "Rellenos", restaurant = restaurant.id)
    category_5 = Category(name = "Platos principales", restaurant = restaurant.id)
    db_service.create_object(category_1)
    db_service.create_object(category_2)
    db_service.create_object(category_3)
    db_service.create_object(category_4)
    db_service.create_object(category_5)

    #Crear platos
    statement = select(Category).where(Category.name == "Platos principales")
    plato_principal: Category = db_service.get_with_filters(statement)[0]

    statement = select(Category).where(Category.name == "Sanguches")
    sanguche: Category = db_service.get_with_filters(statement)[0]

    statement = select(Category).where(Category.name == "Pastas")
    pasta: Category = db_service.get_with_filters(statement)[0]

    statement = select(Category).where(Category.name == "Rellenos")
    relleno: Category = db_service.get_with_filters(statement)[0]

    statement = select(Category).where(Category.name == "Bebidas")
    bebida: Category = db_service.get_with_filters(statement)[0]

    for i in range(6):
        dish_1 = Dish(name = random.choice(platos_pricipales_names),description = "Wea re rica",preparation_time = random.randint(15,45),category = plato_principal.id, price = random.randint(2000,7000))
        dish_2 = Dish(name = random.choice(sanguches_names),description = "Wea re grasosa",preparation_time = random.randint(5,30),category = sanguche.id, price = random.randint(1000,5000))
        dish_3 = Dish(name = random.choice(pastas_names),description = "Como los que hacia la nona :(",preparation_time = random.randint(20,45),category = pasta.id, price = random.randint(3000,8000))
        dish_4 = Dish(name = random.choice(rellenos_names),description = "Wea re ancha",reparation_time = random.randint(5,30),category = relleno.id, price = random.randint(1500,3000))
        dish_5 = Dish(name = random.choice(drinks_names),description = "Wea re refrescante",preparation_time = random.randint(0,5),category = bebida.id ,price = random.randint(700,4000))
        db_service.create_object(dish_1)
        db_service.create_object(dish_2)
        db_service.create_object(dish_3)
        db_service.create_object(dish_4)
        db_service.create_object(dish_5)

    #Crear guarniciones
        side_dish_1 = SideDish(name = random.choice(side_dishes_names),description = "Wea para acompañar",extra_price = random.randint(500,1500))
        side_dish_2 = SideDish(name = random.choice(side_dishes_names),description = "Wea para acompañar",extra_price = random.randint(500,1500))
        db_service.create_object(side_dish_1)
        db_service.create_object(side_dish_2)

    #Adjuntar guarniciones
        side_dishes: SideDish = db_service.get_list_from_db(SideDish)
        dishes: Dish = db_service.get_list_from_db(Dish)
        selected_dish_1 = random.choice(dishes)
        selected_dish_2 = random.choice(dishes)

        side_dish_option_1 = SideDishOptions(dish = selected_dish_1.id, side_dish = random.choice(side_dishes).id)
        side_dish_option_2 = SideDishOptions(dish = selected_dish_2.id, side_dish = random.choice(side_dishes).id)
        db_service.create_object(side_dish_option_1)
        db_service.create_object(side_dish_option_2)

    #Crear tablas
    for i in range(15):
        table_1 = Table(restaurant = restaurant.id)
        db_service.create_object(table_1)

    #Crear mosos
    for i in range(3):
        waiter_1 = Waiter(name = random.choice(names))
        db_service.create_object(waiter_1)

    #Cear ordenes
    for i in range(10):
        tables: Table = db_service.get_list_from_db(Table)
        dishes: Dish = db_service.get_list_from_db(Dish)
        dish = random.choice(dishes)

        selected_table_1 = random.choice(tables)
        db_service.create_object(Order(table = selected_table_1.id , total = dish.price, created_at = datetime.now(), state = random.choice(order_states_names)))

    #Crear detalles de ordenes

        statement = "SELECT MAX(id) FROM order"
        order: Category = db_service.get_with_filters(statement)[0]
    
        db_service.create_object(OrderDetail(dish_selected = dish.id, order = order.id, subtotal = dish.price, customer = random.choice(names)))
from services.db_service import db_service
from datetime import datetime
from sqlmodel import select
from models import TableSector, User, Restaurant, Category, Dish, SideDish, Table, Waiter, SideDishOptions, Order, OrderDetail
import random
import resources.mock_data as rsc

names = ["Pepe","Carlos", "Juan", "Pablo", "Fede", "Marcos", "Martin", "Monica", "Lucia", "Paola", "Victoria", "Martina", "Daniela", "Agostina", "Agustin", "Gustavo", "Manuela", "Manuel", "Domingo", "Maria", "Marta", "Ezequiel", "Pedro", "Lautaro"]
lastanames = ["Perez", "Garcia", "Lopez", "Rodriguez", "Tobares", "Aranda", "Vega", "Fernandez", "Amuchastegui", "Lupi", "Flores", "Tapia", "Rueda", "Juncos", "Alvarez", "Muñoz"]
order_states_names = ["processing", "waiting", "preparation", "cancelled", "delivered"]
platos_pricipales_names = ["Milanesa al plato", "Huevo frito", "Sushi", "Pollo a la mostaza", "Tortilla de papa", "Pizza"]
sanguches_names = ["Pebete", "Lomito", "Lomo ultra mega XXL", "Pizzalomo", "Sandwich de milanesa", "Hamburgesa", "Hamburguesa de hongos"]
pastas_names = ["Fideos con tuco", "Lasagña", "Ravioles caseros", "Sorrentinos"]
rellenos_names = [ "Tarta de acelga", "Tarta de choclo", "Empanadas criollas", "Empanadas arabes", "Empandas de atun", "Empanadas de pollo", "Empanadas de acelga", "Empanadas de soja", "Tacos"]
side_dishes_names = ["Papas fritas", "Pure", "Ensalada", "Papas al horno", "Ensalada rusa", "Rabas"]
drinks_names = ["Cocucha bien fria", "Priteado", "Prity", "Fernandito", "Birrita bien helada", "Levite", "Jugo de naranja exprimida", "Limonada", "Agua mineral","Gin tonic", "Sprite", "Fanta"]
images=[rsc.agua, rsc.fanta, rsc.prity, rsc.hongos, rsc.muzza, rsc.pepperoni, rsc.bebidas, rsc.sanguches, rsc.pizzas, rsc.lomito, rsc.hamburguesa, rsc.mila]

def create_mocks():
    models_list = [User,OrderDetail, SideDishOptions, Dish, SideDish, Waiter, Order,Table, Category, TableSector, Restaurant]
    for model in models_list:
        db_service.delete_dable(model)

    name = random.choice(names)
    lastname = random.choice(lastanames)
    #Crear restaurante
    restaurant_1 = Restaurant(name = name, last_name = lastname)
    db_service.create_object(restaurant_1)

    #Crear usuario
    statement = select(Restaurant).where(Restaurant.name == name)
    restaurant: Restaurant = db_service.get_with_filters(statement)[0]
    user_1 = User(user = "admin", password = "admin", email = "admin@seminario.com", role = "admin", restaurant = restaurant.id)
    db_service.create_object(user_1)

    #Crear categorias
    category_1 = Category(name = "Bebidas",
                          image= rsc.bebidas,
                          restaurant = restaurant.id)
    
    category_2 = Category(name = "Sandwichs",
                          image= rsc.sanguches,
                          restaurant = restaurant.id)
    
    category_3 = Category(name = "Pizzas",
                          image= rsc.pizzas,
                          restaurant = restaurant.id)
    
    db_service.create_object(category_1)
    db_service.create_object(category_2)
    db_service.create_object(category_3)

    #Crear platos
    statement = select(Category).where(Category.name == "Bebidas" and Category.restaurant == restaurant.id)
    pizza: Category = db_service.get_with_filters(statement)[0]

    statement = select(Category).where(Category.name == "Sandwichs" and Category.restaurant == restaurant.id)
    sanguche: Category = db_service.get_with_filters(statement)[0]

    statement = select(Category).where(Category.name == "Pizzas" and Category.restaurant == restaurant.id)
    bebida: Category = db_service.get_with_filters(statement)[0]


    dish_1 = Dish(restaurant= restaurant.id,
                  name = 'Agua mineral',
                  image= rsc.agua,
                  description = "Botella de 500ml.",
                  preparation_time = 0,
                  category = bebida.id,
                  price = 400)
    
    dish_2 = Dish(restaurant= restaurant.id,
                  name = 'Fanta',
                  image= rsc.fanta,
                  description = "Botella de 500ml.",
                  preparation_time = 0,
                  category = bebida.id,
                  price = 700)

    dish_3 = Dish(restaurant= restaurant.id,
                  name = 'Prity',
                  image= rsc.prity,
                  description = "Botella de 500ml.",
                  preparation_time = 0,
                  category = bebida.id,
                  price = 500)

    dish_4 = Dish(restaurant= restaurant.id,
                  name = 'Lomo completo',
                  image= rsc.lomito,
                  description = "Exquisita carne de lomo de ternera con jamon, queso, huevo, lechuga, tomate y mayonesa.",
                  preparation_time = 20,
                  category = sanguche.id,
                  price = 3500)

    dish_5 = Dish(restaurant= restaurant.id,
                  name = 'Sandwich de milanesa completo',
                  image= rsc.mila,
                  description = "Milanesa de carne con jamon, queso, tomate, lechuga y mayonesa.",
                  preparation_time = 20,
                  category = sanguche.id,
                  price = 3200)

    dish_6 = Dish(restaurant= restaurant.id,
                  name = 'Hamburguesa',
                  image= rsc.hamburguesa,
                  description = "Carne simple con cebolla, lechuga, tomate, pepino, queso chedar, mostaza, mayonesa y ketchup.",
                  preparation_time = 20,
                  category = sanguche.id,
                  price = 3000)

    dish_7 = Dish(restaurant= restaurant.id,
                  name = 'Muzzarella',
                  image= rsc.muzza,
                  description = "Una masa bien crujiente con mucha muzzarella y aceitunas.",
                  preparation_time = 15,
                  category = pizza.id,
                  price = 2500)

    dish_8 = Dish(restaurant= restaurant.id,
                  name = 'Hongos',
                  image= rsc.hongos,
                  description = "Una masa bien crujiente con abundante muzzarella y champiñones salteados.",
                  preparation_time = 15,
                  category = pizza.id,
                  price = 3000)

    dish_9 = Dish(restaurant= restaurant.id,
                  name = 'Pepperoni',
                  image= rsc.pepperoni,
                  description = "Pizza al estilo italiano con fetas de pepperoni y abundante muzzarella.",
                  preparation_time = 15,
                  category = pizza.id,
                  price = 3000)

    db_service.create_object(dish_1)
    db_service.create_object(dish_2)
    db_service.create_object(dish_3)
    db_service.create_object(dish_4)
    db_service.create_object(dish_5)
    db_service.create_object(dish_6)
    db_service.create_object(dish_7)
    db_service.create_object(dish_8)
    db_service.create_object(dish_9)

    #Crear guarniciones
    side_dish_2 = SideDish(restaurant=restaurant.id,
                           name = 'Papas fritas',
                           description = '',
                           extra_price = 500)
    
    side_dish_1 = SideDish(restaurant=restaurant.id,
                           name = 'Aros de cebolla fritos',
                           description = '',
                           extra_price = 500)
    
    db_service.create_object(side_dish_1)
    db_service.create_object(side_dish_2)

    #Adjuntar guarniciones
    statement = select(Dish).where(Dish.name == 'Lomo completo' and Dish.restaurant == restaurant.id)
    select_dish_1: Dish = db_service.get_with_filters(statement)[0]
    
    statement = select(Dish).where(Dish.name == 'Sandwich de milanesa completo' and Dish.restaurant == restaurant.id)
    select_dish_2: Dish = db_service.get_with_filters(statement)[0]
    
    statement = select(Dish).where(Dish.name == 'Hamburguesa' and Dish.restaurant == restaurant.id)
    select_dish_3: Dish = db_service.get_with_filters(statement)[0]

    statement = select(SideDish).where(SideDish.name == 'Papas fritas' and SideDish.restaurant == restaurant.id)
    select_side_dish_1: SideDish = db_service.get_with_filters(statement)[0]

    statement = select(SideDish).where(SideDish.name == 'Aros de cebolla fritos' and SideDish.restaurant == restaurant.id)
    select_side_dish_2: SideDish = db_service.get_with_filters(statement)[0]
    

    side_dish_option_1 = SideDishOptions(dish = select_dish_1.id,
                                            side_dish = select_side_dish_1.id,
                                            extraPrice=500)
    
    side_dish_option_2 = SideDishOptions(dish = select_dish_1.id,
                                            side_dish = select_side_dish_2.id,
                                            extraPrice=500)
    
    side_dish_option_3 = SideDishOptions(dish = select_dish_2.id,
                                            side_dish = select_side_dish_1.id,
                                            extraPrice=500)
    
    side_dish_option_4 = SideDishOptions(dish = select_dish_2.id,
                                            side_dish = select_side_dish_2.id,
                                            extraPrice=500)
    
    side_dish_option_5 = SideDishOptions(dish = select_dish_3.id,
                                            side_dish = select_side_dish_1.id,
                                            extraPrice=500)
    
    side_dish_option_6 = SideDishOptions(dish = select_dish_3.id,
                                            side_dish = select_side_dish_2.id,
                                            extraPrice=500)
    
    db_service.create_object(side_dish_option_1)
    db_service.create_object(side_dish_option_2)
    db_service.create_object(side_dish_option_3)
    db_service.create_object(side_dish_option_4)
    db_service.create_object(side_dish_option_5)
    db_service.create_object(side_dish_option_6)

    #Crear Sectores y mesas
    for i in range(1,3):
        sector = TableSector(name=f"sector {i}", restaurant=restaurant.id)
        sector: TableSector = db_service.create_object(sector)
    
        #Crear mesas
        for i in range(1, 15):
            table_1 = Table(restaurant = restaurant.id, sector=sector.id)
            db_service.create_object(table_1)  
                                      
    # Crear mesa con codigo
    sector = TableSector(name=f"sector 4", restaurant=restaurant.id)
    sector: TableSector = db_service.create_object(sector)
    table_qr_code = Table(restaurant = restaurant.id, qr_id = "a", sector=sector.id)
    db_service.create_object(table_qr_code)

    #Crear mosos
    for i in range(1, 3):
        waiter_name = f'{random.choice(names)} {random.choice(lastanames)}'
        waiter_1 = Waiter(name = waiter_name )
        db_service.create_object(waiter_1)
        
    return {"restaurant_id": restaurant.id}
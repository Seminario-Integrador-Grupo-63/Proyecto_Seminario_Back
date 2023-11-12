from services.db_service import db_service
from datetime import datetime
from sqlmodel import select
from models import TableSector, User, Restaurant, Category, Dish, SideDish, Table, Waiter, SideDishOptions, Order, OrderDetail
import random
import resources.mock_data as rsc

names = ["Pepe","Carlos", "Juan", "Pablo", "Fede", "Marcos", "Martin", "Monica", "Lucia", "Paola", "Victoria", "Martina", "Daniela", "Agostina", "Agustin", "Gustavo", "Manuela", "Manuel", "Domingo", "Maria", "Marta", "Ezequiel", "Pedro", "Lautaro"]
lastanames = ["Perez", "Garcia", "Lopez", "Rodriguez", "Tobares", "Aranda", "Vega", "Fernandez", "Frondizi", "Alfonsin","Sarmiento", "Belgrano", "Peron", "Milei", "Amuchastegui", "Lupi", "Flores", "Tapia", "Rueda", "Juncos", "Alvarez", "Muñoz"]
order_states_names = ["processing", "waiting", "preparation", "cancelled", "delivered"]
platos_pricipales_names = ["Milanesa al plato", "Huevo frito", "Sushi", "Pollo a la mostaza", "Tortilla de papa", "Pizza"]
sanguches_names = ["Pebete", "Lomito", "Lomo ultra mega XXL", "Pizzalomo", "Sanguche de milanesa", "Hamburgesa", "Hamburguesa de hongos"]
pastas_names = ["Fideos con tuco", "Lasagña", "Ravioles caseros", "Sorrentinos"]
rellenos_names = [ "Tarta de acelga", "Tarta de choclo", "Empanadas criollas", "Empanadas arabes", "Empandas de atun", "Empanadas de pollo", "Empanadas de acelga", "Empanadas de soja", "Tacos"]
side_dishes_names = ["Papas fritas", "Pure", "Ensalada", "Papas al horno", "Ensalada rusa", "Rabas"]
drinks_names = ["Cocucha bien fria", "Priteado", "Prity", "Fernandito", "Birrita bien helada", "Levite", "Jugo de naranja exprimida", "Limonada", "Agua mineral","Gin tonic", "Sprite", "Fanta"]
images=[rsc.agua, rsc.fanta, rsc.prity, rsc.hongos, rsc.muzza, rsc.pepperoni, rsc.bebidas, rsc.sanguches, rsc.pizzas, rsc.lomito, rsc.hamburguesa, rsc.mila]

def create_mocks_random():
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
    category_1 = Category(name = "Bebidas", image=random.choice(images), restaurant = restaurant.id)
    category_2 = Category(name = "Sanguches", image=random.choice(images), restaurant = restaurant.id)
    category_3 = Category(name = "Pastas", image=random.choice(images), restaurant = restaurant.id)
    category_4 = Category(name = "Rellenos", image=random.choice(images), restaurant = restaurant.id)
    category_5 = Category(name = "Platos principales", image=random.choice(images), restaurant = restaurant.id)
    db_service.create_object(category_1)
    db_service.create_object(category_2)
    db_service.create_object(category_3)
    db_service.create_object(category_4)
    db_service.create_object(category_5)

    #Crear platos
    statement = select(Category).where(Category.name == "Platos principales" and Category.restaurant == restaurant.id)
    plato_principal: Category = db_service.get_with_filters(statement)[0]

    statement = select(Category).where(Category.name == "Sanguches" and Category.restaurant == restaurant.id)
    sanguche: Category = db_service.get_with_filters(statement)[0]

    statement = select(Category).where(Category.name == "Pastas" and Category.restaurant == restaurant.id)
    pasta: Category = db_service.get_with_filters(statement)[0]

    statement = select(Category).where(Category.name == "Rellenos" and Category.restaurant == restaurant.id)
    relleno: Category = db_service.get_with_filters(statement)[0]

    statement = select(Category).where(Category.name == "Bebidas" and Category.restaurant == restaurant.id)
    bebida: Category = db_service.get_with_filters(statement)[0]

    for i in range(10):
        dish_1 = Dish(restaurant= restaurant.id, name = random.choice(platos_pricipales_names),image=random.choice(images), description = "Wea re rica",preparation_time = random.randint(15,45),category = plato_principal.id, price = random.randint(2000,7000))
        dish_2 = Dish(restaurant= restaurant.id, name = random.choice(sanguches_names),image=random.choice(images), description = "Wea re grasosa",preparation_time = random.randint(5,30),category = sanguche.id, price = random.randint(1000,5000))
        dish_3 = Dish(restaurant= restaurant.id, name = random.choice(pastas_names),image=random.choice(images), description = "Como los que hacia la nona :(",preparation_time = random.randint(20,45),category = pasta.id, price = random.randint(3000,8000))
        dish_4 = Dish(restaurant= restaurant.id, name = random.choice(rellenos_names),image=random.choice(images), description = "Wea re ancha",reparation_time = random.randint(5,30),category = relleno.id, price = random.randint(1500,3000))
        dish_5 = Dish(restaurant= restaurant.id, name = random.choice(drinks_names),image=random.choice(images), description = "Wea re refrescante",preparation_time = random.randint(0,5),category = bebida.id ,price = random.randint(700,4000))
        db_service.create_object(dish_1)
        db_service.create_object(dish_2)
        db_service.create_object(dish_3)
        db_service.create_object(dish_4)
        db_service.create_object(dish_5)

    #Crear guarniciones
        side_dish_2 = SideDish(restaurant=restaurant.id, name = random.choice(side_dishes_names),description = "Wea para acompañar",extra_price = random.randint(500,1500))
        side_dish_1 = SideDish(restaurant=restaurant.id, name = random.choice(side_dishes_names),description = "Wea para acompañar",extra_price = random.randint(500,1500))
        db_service.create_object(side_dish_1)
        db_service.create_object(side_dish_2)

    #Adjuntar guarniciones
    for i in range(50):
        statement = select(Dish).where(Dish.restaurant == restaurant.id)
        dishes: list[Dish] = db_service.get_with_filters(statement)

        statement = select(SideDish).where(SideDish.restaurant == restaurant.id)
        side_dishes: list[SideDish] = db_service.get_with_filters(statement)
        
        selected_dish = random.choice(dishes)
        selected_sidedish = random.choice(side_dishes)

        side_dish_option_1 = SideDishOptions(dish = selected_dish.id, side_dish = selected_sidedish.id, extraPrice=random.randint(100, 500))
        db_service.create_object(side_dish_option_1)

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

    #Cear ordenes
    for i in range(1, 10):
        statement = select(Table).where(Table.restaurant == restaurant.id)
        select_tables: list[Table] = db_service.get_with_filters(statement)

        #statement = select(SideDishOptions).where(SideDishOptions.restaurant == restaurant.id)
        #selected_sidedishoptions: list[SideDishOptions] = db_service.get_with_filters(statement)
        selected_sidedishoptions: list[SideDishOptions] = db_service.get_list_from_db(SideDishOptions)
        
        selected_sidedishoption = random.choice(selected_sidedishoptions)
        selected_table = random.choice(select_tables)
        db_service.create_object(Order(restaurant= restaurant.id, table = selected_table.id , total = selected_sidedishoption.extra_price, created_at = datetime.now(), state = random.choice(order_states_names)))

    #Crear detalles de ordenes

        statement = "SELECT * FROM public.order WHERE id = (SELECT MAX(id) FROM public.order);"
        order: Category = db_service.get_with_filters(statement)[0]

        customer_name = f'{random.choice(names)} {random.choice(lastanames)}'
        print(selected_sidedishoption)

        detail = OrderDetail(
            dish=selected_sidedishoption.dish,
            side_dish=selected_sidedishoption.side_dish, 
            order = order.id, 
            sub_total = selected_sidedishoption.extra_price, 
            customer = customer_name,
            amount=random.randint(1,5),
            customer_name=random.choice(names)
        )
        db_service.create_object(detail)
    
    return {"restaurant_id": restaurant.id}

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
    
    category_2 = Category(name = "Sanguches",
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

    statement = select(Category).where(Category.name == "Sanguches" and Category.restaurant == restaurant.id)
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
                  name = 'Lomito completo',
                  image= rsc.lomito,
                  description = "Exquisita carne de lomo de ternera con jamon, queso, huevo, lechuga, tomate y mayonesa.",
                  preparation_time = 20,
                  category = sanguche.id,
                  price = 3500)

    dish_5 = Dish(restaurant= restaurant.id,
                  name = 'Sanguche de milanesa completo',
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
    statement = select(Dish).where(Dish.name == 'Lomito completo' and Dish.restaurant == restaurant.id)
    select_dish_1: Dish = db_service.get_with_filters(statement)[0]
    
    statement = select(Dish).where(Dish.name == 'Sanguche de milanesa completo' and Dish.restaurant == restaurant.id)
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
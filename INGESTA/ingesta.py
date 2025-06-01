import pandas as pd
import random
from datetime import datetime, timedelta
import sqlite3
from faker import Faker
import os

fake = Faker('es_ES')
Faker.seed(42)

def generate_real_estate_data(num_records=1000):
    data = []

    brokers = ['RE/MAX', 'Century 21', 'Coldwell Banker', 'Keller Williams', 
               'Sotheby\'s', 'Realty One', 'eXp Realty', 'Compass', 'Berkshire Hathaway']
    status_options = ['lista para la venta', 'lista para construir']
    cities = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 
              'Málaga', 'Zaragoza', 'Murcia', 'Palma', 'Las Palmas',
              'Córdoba', 'Valladolid', 'Vigo', 'Gijón', 'Alicante']
    states = ['Madrid', 'Cataluña', 'Valencia', 'Andalucía', 'País Vasco',
              'Castilla y León', 'Galicia', 'Castilla-La Mancha', 'Canarias',
              'Murcia', 'Aragón', 'Extremadura', 'Baleares', 'Asturias', 'Navarra']
    streets = ['Calle Mayor', 'Avenida de la Constitución', 'Plaza del Sol',
               'Calle Gran Vía', 'Paseo de la Castellana', 'Ronda de Valencia',
               'Calle Serrano', 'Avenida Diagonal', 'Calle Alcalá', 'Plaza España']

    for i in range(num_records):
        city = random.choice(cities)
        state = random.choice(states)
        bedrooms = random.randint(1, 6)
        bathrooms = random.randint(1, min(bedrooms + 1, 4))
        house_size = random.randint(50, 500) 
        acre_lot = round(random.uniform(0.1, 2.0), 2)

        base_prices = {
            'Madrid': 4500, 'Barcelona': 4200, 'Valencia': 2800,
            'Sevilla': 2200, 'Bilbao': 3100, 'Málaga': 2600
        }
        base_price = base_prices.get(city, 2000)

        price = int(base_price * house_size + bedrooms * 20000 + bathrooms * 15000 + acre_lot * 50000)
        price += random.randint(-50000, 100000)
        price = max(price, 80000)

        prev_sold_date = fake.date_between(start_date='-2y', end_date='-30d')
        record = {
            'brokered_by': random.choice(brokers),
            'status': random.choice(status_options),
            'price': price,
            'bed': bedrooms,
            'bath': bathrooms,
            'acre_lot': acre_lot,
            'street': f"{random.choice(streets)} {random.randint(1, 200)}",
            'city': city,
            'state': state,
            'zip_code': f"{random.randint(10000, 99999)}",
            'house_size': house_size,
            'prev_sold_date': prev_sold_date.strftime('%Y-%m-%d')
        }

        data.append(record)
    
    return pd.DataFrame(data)

def save_to_csv(df, filename='/output/properties_batch.csv'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"✅ Dataset guardado en {filename}")

def save_to_sqlite(df, db_name='real_estate.db', table_name='properties'):
    """Guardar dataset en base de datos SQLite"""
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"✅ Dataset guardado en base de datos SQLite: {db_name}")

def main():
    print("🎯 Generando dataset de bienes raíces...")

    df = generate_real_estate_data(1000)

    print(f"\n📊 Registros: {len(df)} | Precio: €{df['price'].min():,} - €{df['price'].max():,}")
    print(f"Ciudades: {df['city'].nunique()} | Brokers: {df['brokered_by'].nunique()}")

    save_to_csv(df)
    save_to_sqlite(df)

    print("\n✅ Archivos generados:")
    print("- /tmp/properties_batch.csv")
    print("- real_estate.db")

if __name__ == "__main__":
    main()
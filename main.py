import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI
import re

load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=KEY)

def load_data(file_path):
    return pd.read_csv(file_path)

def enhance_description(product_name, short_description, long_description):
    instructions = f"""
    ### Optimización SEO: Crea una nueva descripción larga de producto, o modifica la ya existente, optimizada para SEO y única para este producto utilizando los datos proporcionados.
    - Nota: Enfocarse en términos específicos para evitar la canibalización de palabras clave.

    ### Generar Descripción Larga
    1. **Resumen:** Proporciona tres o más párrafos que resalten lo más distintivo del producto sin mencionar su nombre.
    2. **Características Principales:** Trata de poner lo más importante al principio.

    ### Ejemplo Estructurado
    "Este modelo representa una solución señalética distinta, diseñada específicamente para armonizar con la belleza de entornos al aire 
    libre y que no solo destaca por su robustez y durabilidad, sino también por su estética singular. Cada unidad se puede diseñar para que sea única, 
    gracias a la variabilidad en la altura de los palos que componen su estructura, creando una silueta irregular que añade un toque distintivo a cualquier paisaje.

    La funcionalidad se encuentra en el corazón del mismo, ofreciendo una amplia gama de opciones de personalización. Este hito permite a los 
    clientes elegir entre diversas soluciones de señalización, desde chapas básicas hasta opciones completamente personalizadas, con la 
    posibilidad de instalar el cartel informativo en una o ambas caras del muro. Esto garantiza una visibilidad óptima y adaptabilidad a 
    las necesidades específicas del entorno donde se ubique.

    Además, su enfoque en la sostenibilidad y durabilidad es evidente en el uso de madera de pino nórdico tratada en autoclave clase de uso 4, 
    asegurando resistencia contra los elementos y prolongando la vida útil del hito. Este tratamiento, junto con el certificado PEFC, subraya 
    el compromiso de Soluciones de Madera con la calidad y el respeto al medio ambiente"

    ### Datos del Producto
    - **Producto:** {product_name}
    - **Descripción larga:** {long_description}
    - **Descripción corta:** {short_description}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": instructions}
        ],
        max_tokens=450,
        temperature=0.6,
        top_p=0.6,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

def process_products(products):
    enhanced_products = []

    for _, product in products.iterrows():
        enhanced_desc = enhance_description(
            product['name'], product['short_description'], product['description']
        )
        print(f"Enhanced description for product '{product['name']}': {enhanced_desc}")
        enhanced_products.append({
            'name': product['name'],
            'enhanced_description': enhanced_desc
        })
    
    enhanced_df = pd.DataFrame(enhanced_products)
    enhanced_df.to_csv('data/enhanced_products.csv', index=False)

def build_category_tree(products):
    category_tree = {}
    for _, row in products.iterrows():
        categories = row['categories'].split('/')
        current_level = category_tree
        for category in categories:
            if category not in current_level:
                current_level[category] = {}
            current_level = current_level[category]
    return category_tree

def display_category_tree(category_tree, level=0, index=1):
    items = []
    for category, subcategories in category_tree.items():
        items.append((index, '  ' * level + category))
        index += 1
        if subcategories:
            subitems, index = display_category_tree(subcategories, level + 1, index)
            items.extend(subitems)
    for idx, name in items:
        print(f"{idx}. {name}")
    return items, index

def confirm_action(total_count):
    print(f"This action will enhance {total_count} products. Are you sure you want to proceed? (yes/no)")
    return input().strip().lower() == 'yes'

def improve_all_products():
    products = load_data('data/products.csv')
    total_count = len(products)
    print(f"There are {total_count} products to enhance.")

    if confirm_action(total_count):
        process_products(products)
        print("Product descriptions enhanced successfully.")

def improve_products_by_category():
    products = load_data('data/products.csv')
    category_tree = build_category_tree(products)
    
    while True:
        items, _ = display_category_tree(category_tree)
        choice = int(input("Choose a category (number): "))
        
        chosen_category = items[choice - 1][1].strip()
        chosen_category_regex = re.escape(chosen_category)

        filtered_products = products[products['categories'].str.contains(chosen_category_regex)]
        total_count = len(filtered_products)
        
        print(f"There are {total_count} products in the '{chosen_category}' category to enhance.")
        
        if confirm_action(total_count):
            process_products(filtered_products)
            print(f"Product descriptions in category '{chosen_category}' enhanced successfully.")

def display_menu():
    print("Welcome to E-Commerce Description Enhancer")
    print("Please choose what you want to improve:")
    print("1. Products")
    print("2. Exit")

def display_product_menu():
    print("Product Improvement Options:")
    print("1. Improve all products")
    print("2. Improve products by category")
    print("3. Back to main menu")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            while True:
                display_product_menu()
                product_choice = input("Enter your choice: ").strip()
                
                if product_choice == '1':
                    improve_all_products()
                elif product_choice == '2':
                    improve_products_by_category()
                elif product_choice == '3':
                    break
                else:
                    print("Invalid choice, please try again.")
        elif choice == '2':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

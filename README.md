
# WooCommerce Description Enhancer

## Project Overview

This project aims to improve the product descriptions of a WooCommerce store using AI. By leveraging the OpenAI API, we can optimize product descriptions to maintain a consistent and appealing format.

**Note:** This is the initial version of the project, which currently focuses on enhancing product descriptions. Future updates will include enhancements for categories, tags, and blog entries.

## Project Structure

- **data/**: Contains CSV files with data for products.
- **main.py**: The main script to run the description enhancement.
- **.env**: Stores environment variables, such as API keys.

## Setup Instructions

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/JMViJi/woocommerce-description-enhancer.git
    cd woocommerce-description-enhancer
    ```

2. **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```plaintext
    OPENAI_API_KEY=your_openai_api_key_here
    ```

5. **Prepare Your Data:**
    Ensure your product data is available in `data/products.csv` with the following columns:
    - `name`
    - `short_description`
    - `description`

## Usage

### Running the Enhancer Script
To enhance product descriptions, run the main script:
```bash
python main.py
```

You will be prompted to choose whether to enhance all products or products by category. Follow the prompts to complete the enhancement process.

## Example

Here is an example of how to enhance a single product's description:

```python
product = {
    'name': 'Folding Camping Chair',
    'short_description': 'A light and resistant chair, perfect for camping and outdoor activities.',
    'description': 'This folding chair is ideal for those who enjoy nature and need a practical and comfortable solution.',
}
AIdescription = enhance_description(producto['name'], producto['short_description'], producto['description'])
print(AIdescription)
```

## Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Shri_Hari98!",
    "database": "cake_shop"
}

def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    conn.autocommit = True  # Enable autocommit to avoid unnecessary locks
    return conn

#-------------------Customer table-----------------
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users), 200  # Add status code

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
        # Insert user data into the database
    cursor.execute("INSERT INTO customer (username, email) VALUES (%s, %s)", 
                       (data['name'], data['email']))
    conn.commit()  # Commit the transaction
    cursor.close()
    conn.close()
    return jsonify({"message": "User added"}), 201  # Return valid response with status code

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customer SET name = %s, email = %s WHERE user_id = %s",
                   (data['name'], data['quantity'], user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User updated successfully"})


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM customer WHERE user_id = %s", (user_id,))
    conn.commit()  # Commit the transaction
    cursor.close()
    conn.close()
    return jsonify({"message": "User deleted successfully"}), 200  # Return success with status code

#--------------Product table---------------
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, description) VALUES (%s, %s, %s)", 
                   (data['name'], data['price'], data['description']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Product added successfully"}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = %s, price = %s, description = %s WHERE product_id = %s",
                   (data['name'], data['price'], data['description'], product_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Product updated successfully"})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Product deleted successfully"})

# ------------------------- ORDER CRUD -------------------------
@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT orders.order_id, customer.username AS user_name, products.product_name AS product_name, 
               orders.quantity, orders.order_date 
        FROM orders
        JOIN customer ON orders.user_id = customer.user_id
        JOIN products ON orders.product_id = products.product_id
    """)
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, product_id, quantity) VALUES (%s, %s, %s)", 
                   (data['user_id'], data['product_id'], data['quantity']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Order placed successfully"}), 201

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET user_id = %s, product_id = %s, quantity = %s WHERE order_id = %s",
                   (data['user_id'], data['product_id'], data['quantity'], order_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Order updated successfully"})
    
        
if __name__ == '__main__':
    app.run(debug=True)

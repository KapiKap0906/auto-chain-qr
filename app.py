from flask import Flask, render_template, request, jsonify, redirect, url_for,flash
from datetime import datetime 
from main import  dispose_product, initialize_database, add_or_update_product
import sqlite3
import json
import csv


app = Flask(__name__)

app.secret_key = 'supersecretkey'  # Required for flashing messages

DATABASE = 'products.db'

# Helper function to fetch data from the database
def fetch_data():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product_tracking")
    rows = cursor.fetchall()
    conn.close()
    
    data = []
    for row in rows:
        data.append({
            "product_id": row[0],
            "product_name": row[1],
            "station_number": row[2],
            "in_time": str(row[3]),
            "out_time": str(row[4]) if row[4] else "-",
            "live": bool(row[5])
        })
    return data

# Helper function to fetch unique product ids
def fetch_unique_product_names():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT product_name FROM product_tracking")
    product_names = cursor.fetchall()
    conn.close()
    return [product_name[0] for product_name in product_names]

# Route for the main dashboard
@app.route('/')
def index():
    data = fetch_data()
    print(data)
    return render_template('index.html', data=data)

@app.route('/live_station_view')
def live_station_view():
    data = fetch_data()

    # Grouping raw materials by station number for live items
    active_stations = {}
    inactive_stations = {}

    for item in data:
        station = item['station_number']
        is_live = item['live']  # Assuming 'live' is the field that tells if the product is live
        
        if is_live:
            if station not in active_stations:
                active_stations[station] = []
            active_stations[station].append(item)
        else:
            if station not in inactive_stations:
                inactive_stations[station] = []
            inactive_stations[station].append(item)
    
    return render_template('live_station_view.html', 
                           active_stations=active_stations, 
                           inactive_stations=inactive_stations)


# Route for Live Raw Material View
@app.route('/live_raw_material_view', methods=['GET', 'POST'])
def live_raw_material_view():
    selected_product_name = request.args.get('selected_product_name')
    if request.method == 'POST':
        selected_product_name = request.form.get('selected_product_name')
    
    if selected_product_name:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_tracking WHERE product_name = ?", (selected_product_name,))
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            # Reverse the order to display newer entries first
            rows.reverse()
            print(rows)
            return render_template('live_raw_material_view.html', raw_material=selected_product_name, previous_entries=rows, product_names=fetch_unique_product_names())
        else:
            return "Raw material not found", 404
    
    # Handle GET request (initial page load)
    materials = {}
    for item in fetch_data():
        product_name = item['product_name']
        if product_name not in materials:
            materials[product_name] = []
        materials[product_name].append(item)
    
    # Get unique product ids for the dropdown
    product_names = fetch_unique_product_names()

    return render_template('live_raw_material_view.html', materials=materials, product_names=product_names, raw_material=selected_product_name)

@app.route('/api/search_raw_material', methods=['GET'])
def search_raw_material():
    raw_material_name = request.args.get('raw_material', '').lower()
    
    if not raw_material_name:
        return jsonify({"total": 0, "results": []})

    # Query the database for raw material entries that match the search term
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product_tracking WHERE LOWER(product_name) LIKE ?", ('%' + raw_material_name + '%',))
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    # Group results by product_name (raw material)
    seen_product_names = set()
    for row in rows:
        product_name = row[0]
        if product_name not in seen_product_names:
            seen_product_names.add(product_name)
            entries = [
                {
                    "station_number": item[1],
                    "in_time": str(item[2]),
                    "out_time": str(item[3]) if item[3] else "-",
                    "live": bool(item[4])
                }
                for item in rows if item[0] == product_name
            ]
            result.append({
                "raw_material": product_name,
                "previous_entries": entries
            })
    
    return jsonify({"total": len(result), "results": result})

# Route to add a product
# @app.route('/add_product', methods=['GET', 'POST'])
# def add_product_route():
#     if request.method == 'POST':
#         product_id = request.form['product_id']
#         product_name = request.form['product_name']

#         if not product_id or not product_name:
#             flash("Both Product ID and Product Name are required.", "error")
#         else:
#             add_product(product_id, product_name, DATABASE)
#             flash(f"Product '{product_name}' with ID '{product_id}' added successfully.", "success")
#         return redirect(url_for('add_product_route'))
#     return render_template('add_product.html')

# Route to add or update a product
@app.route('/add_or_update_product', methods=['GET', 'POST'])
def add_or_update_product_route():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        station_number = request.form['station_number']

        if not product_id or not product_name or not station_number:
            flash("All fields are required: Product ID, Product Name, and Station Number.", "error")
        else:
            add_or_update_product(product_id, product_name, station_number, DATABASE)
            flash(f"Product '{product_name}' with ID '{product_id}' added or updated successfully.", "success")
        return redirect(url_for('add_or_update_product_route'))

    return render_template('add_or_update_product.html')

# Route to dispose of a product
@app.route('/dispose_product', methods=['GET', 'POST'])
def dispose_product_route():
    if request.method == 'POST':
        product_id = request.form['product_id']

        if not product_id:
            flash("Product ID is required.", "error")
        else:
            dispose_product(product_id, DATABASE)
            flash(f"Product with ID '{product_id}' disposed successfully.", "success")
        return redirect(url_for('dispose_product_route'))

    return render_template('dispose_product.html')

@app.route('/audit', methods=['GET', 'POST'])
def audit():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No file provided", 400

        # Read product IDs from the uploaded CSV
        csv_file = file.read().decode('utf-8').splitlines()
        csv_reader = csv.reader(csv_file)
        product_ids = [row[0] for row in csv_reader]

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        # Find live items not in the CSV or inactive items present in the CSV
        cursor.execute('''
            SELECT product_id, live FROM product_tracking
        ''')
        all_products = cursor.fetchall()
        conn.close()

        discrepancies = {
            "missing_live": [],
            "scanned_untracked": []
        }

        for product_id, live in all_products:
            if product_id not in product_ids and live:
                discrepancies["missing_live"].append(product_id)  # Live product missing from CSV
            if product_id in product_ids and not live:
                discrepancies["scanned_untracked"].append(product_id)  # Product scanned but never been tracked as live

        # Redirect to the audit results page with discrepancies
        return redirect(url_for('audit_results', discrepancies=discrepancies))

    return '''
        <!doctype html>
        <head><link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}"></head>
        <title>Audit Products</title>
        <h1>Upload CSV for Audit</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">Upload</button>
        </form>
    '''
    
@app.route('/audit_results')
def audit_results():
    discrepancies = request.args.get('discrepancies')
    if discrepancies:
        discrepancies = eval(discrepancies)  # Convert string back to dictionary
    return render_template('audit_results.html', discrepancies=discrepancies)

if __name__ == '__main__':
    app.run(debug=True)

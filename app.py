from flask import Flask, render_template, request, jsonify
import sqlite3
import json

app = Flask(__name__)

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
            "station_number": row[1],
            "in_time": str(row[2]),
            "out_time": str(row[3]) if row[3] else "-",
            "live": bool(row[4])
        })
    return data

# Helper function to fetch unique product ids
def fetch_unique_product_ids():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT product_id FROM product_tracking")
    product_ids = cursor.fetchall()
    conn.close()
    return [product_id[0] for product_id in product_ids]

# Route for the main dashboard
@app.route('/')
def index():
    data = fetch_data()
    return render_template('index.html', data=data)

# Route for Live Station View
@app.route('/live_station_view')
def live_station_view():
    data = fetch_data()
    
    # Grouping raw materials by station number
    stations = {}
    for item in data:
        station = item['station_number']
        if station not in stations:
            stations[station] = []
        stations[station].append(item)
    
    return render_template('live_station_view.html', stations=stations)

# Route for Live Raw Material View
@app.route('/live_raw_material_view', methods=['GET', 'POST'])
def live_raw_material_view():
    selected_product_id = request.args.get('selected_product_id')
    if request.method == 'POST':
        selected_product_id = request.form.get('selected_product_id')
    
    if selected_product_id:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_tracking WHERE product_id = ?", (selected_product_id,))
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            # Reverse the order to display newer entries first
            rows.reverse()
            return render_template('live_raw_material_view.html', raw_material=selected_product_id, previous_entries=rows, product_ids=fetch_unique_product_ids())
        else:
            return "Raw material not found", 404
    
    # Handle GET request (initial page load)
    materials = {}
    for item in fetch_data():
        product_id = item['product_id']
        if product_id not in materials:
            materials[product_id] = []
        materials[product_id].append(item)
    
    # Get unique product ids for the dropdown
    product_ids = fetch_unique_product_ids()

    return render_template('live_raw_material_view.html', materials=materials, product_ids=product_ids, raw_material=selected_product_id)

@app.route('/api/search_raw_material', methods=['GET'])
def search_raw_material():
    raw_material_name = request.args.get('raw_material', '').lower()
    
    if not raw_material_name:
        return jsonify({"total": 0, "results": []})

    # Query the database for raw material entries that match the search term
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product_tracking WHERE LOWER(product_id) LIKE ?", ('%' + raw_material_name + '%',))
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    # Group results by product_id (raw material)
    seen_product_ids = set()
    for row in rows:
        product_id = row[0]
        if product_id not in seen_product_ids:
            seen_product_ids.add(product_id)
            entries = [
                {
                    "station_number": item[1],
                    "in_time": str(item[2]),
                    "out_time": str(item[3]) if item[3] else "-",
                    "live": bool(item[4])
                }
                for item in rows if item[0] == product_id
            ]
            result.append({
                "raw_material": product_id,
                "previous_entries": entries
            })
    
    return jsonify({"total": len(result), "results": result})

if __name__ == '__main__':
    app.run(debug=True)

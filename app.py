from flask import Flask, render_template
import sqlite3

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
            "in_time": row[2],
            "out_time": row[3] if row[3] else "-",
            "live": bool(row[4])
        })
    return data

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
@app.route('/live_raw_material_view')
def live_raw_material_view():
    data = fetch_data()
    
    # Grouping stations by raw material ID
    materials = {}
    for item in data:
        product_id = item['product_id']
        if product_id not in materials:
            materials[product_id] = []
        materials[product_id].append(item)
    
    return render_template('live_raw_material_view.html', materials=materials)

if __name__ == '__main__':
    app.run(debug=True)

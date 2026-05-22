from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# =========================
# MYSQL CONNECTION
# =========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",
    database="diesel_offer"
)

cursor = db.cursor()

print("Database Connected Successfully!")

# =========================
# LOGIN PAGE ROUTE
# =========================
@app.route("/")
def login_page():
    return render_template("login.html")


# =========================
# HOME PAGE ROUTE (FIXED)
# =========================
@app.route("/home")
def home():
    return render_template("home.html")


# =========================
# LOGIN API (FIXED JSON SAFETY)
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    query = """
        SELECT * FROM users
        WHERE username = %s AND password = %s
    """

    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


# =========================
# SAVE BILL
# =========================
@app.route("/save_bill", methods=["POST"])
def save_bill():
    data = request.json

    query = """
        INSERT INTO bills
        (mobile_number, vehicle_number, bill_number, fuel_liters, bill_date)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        data["mobile"],
        data["vehicle"],
        data["bill"],
        data["liters"],
        data["date"]
    )

    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Bill Saved Successfully!"})


# =========================
# GET ALL BILLS
# =========================
@app.route("/get_bills", methods=["GET"])
def get_bills():
    cursor.execute("SELECT * FROM bills")
    rows = cursor.fetchall()

    bills = []
    for row in rows:
        bills.append({
            "id": row[0],
            "mobile_number": row[1],
            "vehicle_number": row[2],
            "bill_number": row[3],
            "fuel_liters": row[4],
            "bill_date": str(row[5])
        })

    return jsonify(bills)


# =========================
# GET SINGLE BILL
# =========================
@app.route("/get_bill/<int:id>", methods=["GET"])
def get_bill(id):
    cursor.execute("SELECT * FROM bills WHERE id = %s", (id,))
    row = cursor.fetchone()

    if not row:
        return jsonify({"message": "Bill not found"})

    return jsonify({
        "id": row[0],
        "mobile_number": row[1],
        "vehicle_number": row[2],
        "bill_number": row[3],
        "fuel_liters": row[4],
        "bill_date": str(row[5])
    })


# =========================
# UPDATE BILL
# =========================
@app.route("/update_bill/<int:id>", methods=["PUT"])
def update_bill(id):
    data = request.json

    query = """
        UPDATE bills
        SET mobile_number=%s,
            vehicle_number=%s,
            bill_number=%s,
            fuel_liters=%s,
            bill_date=%s
        WHERE id=%s
    """

    values = (
        data["mobile"],
        data["vehicle"],
        data["bill"],
        data["liters"],
        data["date"],
        id
    )

    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Bill Updated Successfully!"})


# =========================
# DELETE BILL
# =========================
@app.route("/delete_bill/<int:id>", methods=["DELETE"])
def delete_bill(id):
    cursor.execute("DELETE FROM bills WHERE id = %s", (id,))
    db.commit()

    return jsonify({"message": "Bill Deleted Successfully!"})


# =========================
# SEARCH BILLS
# =========================
@app.route("/search_bills/<mobile>", methods=["GET"])
def search_bills(mobile):
    query = """
        SELECT * FROM bills
        WHERE mobile_number LIKE %s
    """

    cursor.execute(query, ("%" + mobile + "%",))
    rows = cursor.fetchall()

    bills = []
    for row in rows:
        bills.append({
            "id": row[0],
            "mobile_number": row[1],
            "vehicle_number": row[2],
            "bill_number": row[3],
            "fuel_liters": row[4],
            "bill_date": str(row[5])
        })

    return jsonify(bills)


# =========================
# ADD USER
# =========================
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json

    query = """
        INSERT INTO users
        (full_name, mobile_number, username, password, role)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        data["full_name"],
        data["mobile_number"],
        data["username"],
        data["password"],
        data["role"]
    )

    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "User Added Successfully!"})


# =========================
# DASHBOARD STATS
# =========================
@app.route("/dashboard_stats", methods=["GET"])
def dashboard_stats():

    cursor.execute("SELECT COUNT(*) FROM bills")
    total_bills = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(fuel_liters) FROM bills")
    total_fuel = cursor.fetchone()[0] or 0

    return jsonify({
        "total_bills": total_bills,
        "total_users": total_users,
        "total_fuel": float(total_fuel)
    })


# =========================
# BILLS BY DATE
# =========================
@app.route("/bills_by_date/<from_date>/<to_date>", methods=["GET"])
def bills_by_date(from_date, to_date):

    query = """
        SELECT * FROM bills
        WHERE bill_date BETWEEN %s AND %s
    """

    cursor.execute(query, (from_date, to_date))
    rows = cursor.fetchall()

    bills = []
    for row in rows:
        bills.append({
            "id": row[0],
            "mobile_number": row[1],
            "vehicle_number": row[2],
            "bill_number": row[3],
            "fuel_liters": row[4],
            "bill_date": str(row[5])
        })

    return jsonify(bills)


# =========================
# CHANGE PASSWORD
# =========================
@app.route("/change_password", methods=["PUT"])
def change_password():
    data = request.json

    cursor.execute("""
        SELECT * FROM users
        WHERE username=%s AND password=%s
    """, (data["username"], data["old_password"]))

    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "Old Password Incorrect!"})

    cursor.execute("""
        UPDATE users
        SET password=%s
        WHERE username=%s
    """, (data["new_password"], data["username"]))

    db.commit()

    return jsonify({"message": "Password Changed Successfully!"})


# =========================
# OFFER ACHIEVERS
# =========================
@app.route("/offer_achievers", methods=["GET"])
def offer_achievers():

    cursor.execute("""
        SELECT mobile_number, SUM(fuel_liters) AS total_fuel
        FROM bills
        GROUP BY mobile_number
        HAVING total_fuel >= 100
    """)

    rows = cursor.fetchall()

    return jsonify([
        {
            "mobile_number": row[0],
            "total_fuel": float(row[1])
        }
        for row in rows
    ])


# =========================
# REDEEM OFFER
# =========================
@app.route("/redeem_offer/<mobile_number>", methods=["POST"])
def redeem_offer(mobile_number):

    cursor.execute("""
        SELECT SUM(fuel_liters)
        FROM bills
        WHERE mobile_number=%s
    """, (mobile_number,))

    total_fuel = cursor.fetchone()[0] or 0

    if total_fuel >= 100:

        cursor.execute("""
            INSERT INTO redeemed_offers
            (mobile_number, total_fuel, reward_name)
            VALUES (%s, %s, %s)
        """, (mobile_number, total_fuel, "Free Oil Change"))

        db.commit()

        return jsonify({"message": "Offer Redeemed Successfully!"})

    return jsonify({"message": "Customer Not Eligible Yet!"})


# =========================
# REDEEM REPORTS
# =========================
@app.route("/redeem_reports", methods=["GET"])
def redeem_reports():

    cursor.execute("""
        SELECT * FROM redeemed_offers
        ORDER BY redeemed_date DESC
    """)

    rows = cursor.fetchall()

    return jsonify([
        {
            "id": row[0],
            "mobile_number": row[1],
            "total_fuel": float(row[2]),
            "reward_name": row[3],
            "redeemed_date": str(row[4])
        }
        for row in rows
    ])


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
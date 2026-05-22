from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL Connection

db = mysql.connector.connect(

    host="localhost",
    user="root",
    password="123",
    database="diesel_offer"

)

cursor = db.cursor()

print("Database Connected Successfully!")

# HOME ROUTE

@app.route("/")

def home():

    return "Flask Server Running"

# SAVE BILL API

@app.route("/save_bill", methods=["POST"])

def save_bill():

    data = request.json

    mobile = data["mobile"]
    vehicle = data["vehicle"]
    bill = data["bill"]
    liters = data["liters"]
    date = data["date"]

    query = """

    INSERT INTO bills
    (mobile_number, vehicle_number, bill_number, fuel_liters, bill_date)

    VALUES (%s, %s, %s, %s, %s)

    """

    values = (mobile, vehicle, bill, liters, date)

    cursor.execute(query, values)

    db.commit()

    return jsonify({

        "message": "Bill Saved Successfully!"

    })

# GET ALL BILLS

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

# GET SINGLE BILL

@app.route("/get_bill/<int:id>", methods=["GET"])

def get_bill(id):

    query = "SELECT * FROM bills WHERE id = %s"

    cursor.execute(query, (id,))

    row = cursor.fetchone()

    bill = {

        "id": row[0],
        "mobile_number": row[1],
        "vehicle_number": row[2],
        "bill_number": row[3],
        "fuel_liters": row[4],
        "bill_date": str(row[5])

    }

    return jsonify(bill)

# UPDATE BILL

@app.route("/update_bill/<int:id>", methods=["PUT"])

def update_bill(id):

    data = request.json

    mobile = data["mobile"]
    vehicle = data["vehicle"]
    bill = data["bill"]
    liters = data["liters"]
    date = data["date"]

    query = """

    UPDATE bills

    SET

    mobile_number = %s,
    vehicle_number = %s,
    bill_number = %s,
    fuel_liters = %s,
    bill_date = %s

    WHERE id = %s

    """

    values = (
        mobile,
        vehicle,
        bill,
        liters,
        date,
        id
    )

    cursor.execute(query, values)

    db.commit()

    return jsonify({

        "message": "Bill Updated Successfully!"

    })

# DELETE BILL

@app.route("/delete_bill/<int:id>", methods=["DELETE"])

def delete_bill(id):

    query = "DELETE FROM bills WHERE id = %s"

    cursor.execute(query, (id,))

    db.commit()

    return jsonify({

        "message": "Bill Deleted Successfully!"

    })

# RUN SERVER

@app.route("/search_bills/<mobile>", methods=["GET"])

def search_bills(mobile):

    query = """

    SELECT * FROM bills

    WHERE mobile_number LIKE %s

    """

    value = ("%" + mobile + "%",)

    cursor.execute(query, value)

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
# ADD USER API

@app.route("/add_user", methods=["POST"])

def add_user():

    data = request.json

    full_name = data["full_name"]
    mobile_number = data["mobile_number"]
    username = data["username"]
    password = data["password"]
    role = data["role"]

    query = """

    INSERT INTO users

    (
        full_name,
        mobile_number,
        username,
        password,
        role
    )

    VALUES (%s, %s, %s, %s, %s)

    """

    values = (
        full_name,
        mobile_number,
        username,
        password,
        role
    )

    cursor.execute(query, values)

    db.commit()

    return jsonify({

        "message": "User Added Successfully!"

    })

# DASHBOARD STATS API

@app.route("/dashboard_stats", methods=["GET"])

def dashboard_stats():

    # TOTAL BILLS

    cursor.execute(

        "SELECT COUNT(*) FROM bills"

    )

    total_bills = cursor.fetchone()[0]

    # TOTAL USERS

    cursor.execute(

        "SELECT COUNT(*) FROM users"

    )

    total_users = cursor.fetchone()[0]

    # TOTAL FUEL

    cursor.execute(

        "SELECT SUM(fuel_liters) FROM bills"

    )

    fuel_result = cursor.fetchone()[0]

    if fuel_result is None:

        fuel_result = 0

    return jsonify({

        "total_bills": total_bills,

        "total_users": total_users,

        "total_fuel": float(fuel_result)

    })


# LOGIN API

@app.route("/login", methods=["POST"])

def login():

    data = request.json

    username = data["username"]
    password = data["password"]

    query = """

    SELECT * FROM users

    WHERE username = %s
    AND password = %s

    """

    values = (
        username,
        password
    )

    cursor.execute(query, values)

    user = cursor.fetchone()

    if user:

        return jsonify({

            "success": True

        })

    else:

        return jsonify({

            "success": False

        })

# BILLS BY DATE API

@app.route(
    "/bills_by_date/<from_date>/<to_date>",
    methods=["GET"]
)

def bills_by_date(from_date, to_date):

    query = """

    SELECT * FROM bills

    WHERE bill_date
    BETWEEN %s AND %s

    """

    values = (
        from_date,
        to_date
    )

    cursor.execute(query, values)

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

# CHANGE PASSWORD API

@app.route(
    "/change_password",
    methods=["PUT"]
)

def change_password():

    data = request.json

    username = data["username"]
    old_password = data["old_password"]
    new_password = data["new_password"]

    # CHECK USER

    query = """

    SELECT * FROM users

    WHERE username = %s
    AND password = %s

    """

    values = (
        username,
        old_password
    )

    cursor.execute(query, values)

    user = cursor.fetchone()

    if user:

        update_query = """

        UPDATE users

        SET password = %s

        WHERE username = %s

        """

        update_values = (
            new_password,
            username
        )

        cursor.execute(
            update_query,
            update_values
        )

        db.commit()

        return jsonify({

            "message":
            "Password Changed Successfully!"

        })

    else:

        return jsonify({

            "message":
            "Old Password Incorrect!"

        })

# OFFER ACHIEVERS API

@app.route(
    "/offer_achievers",
    methods=["GET"]
)

def offer_achievers():

    query = """

    SELECT

    mobile_number,

    SUM(fuel_liters)
    AS total_fuel

    FROM bills

    GROUP BY mobile_number

    HAVING total_fuel >= 100

    """

    cursor.execute(query)

    rows = cursor.fetchall()

    achievers = []

    for row in rows:

        achievers.append({

            "mobile_number": row[0],

            "total_fuel": float(row[1])

        })

    return jsonify(achievers)


# REDEEM OFFER API

@app.route(
    "/redeem_offer/<mobile_number>",
    methods=["POST"]
)

def redeem_offer(mobile_number):

    # CHECK TOTAL FUEL

    query = """

    SELECT

    SUM(fuel_liters)

    FROM bills

    WHERE mobile_number = %s

    """

    cursor.execute(query, (mobile_number,))

    result = cursor.fetchone()

    total_fuel = result[0]

    if total_fuel is None:

        total_fuel = 0

    # ELIGIBILITY CHECK

    if total_fuel >= 100:

        reward_name = "Free Oil Change"

        insert_query = """

        INSERT INTO redeemed_offers
        (
            mobile_number,
            total_fuel,
            reward_name
        )

        VALUES (%s, %s, %s)

        """

        values = (
            mobile_number,
            total_fuel,
            reward_name
        )

        cursor.execute(
            insert_query,
            values
        )

        db.commit()

        return jsonify({

            "message":
            "Offer Redeemed Successfully!"

        })

    else:

        return jsonify({

            "message":
            "Customer Not Eligible Yet!"

        })
# REDEEM REPORT API

@app.route(
    "/redeem_reports",
    methods=["GET"]
)

def redeem_reports():

    query = """

    SELECT * FROM redeemed_offers

    ORDER BY redeemed_date DESC

    """

    cursor.execute(query)

    rows = cursor.fetchall()

    reports = []

    for row in rows:

        reports.append({

            "id": row[0],

            "mobile_number": row[1],

            "total_fuel": float(row[2]),

            "reward_name": row[3],

            "redeemed_date": str(row[4])

        })

    return jsonify(reports)
                  
if __name__ == "__main__":

    app.run(debug=True)
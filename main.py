import json
import logging
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import re  # for regular expression

# App Configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vishnu.db"
db = SQLAlchemy(app)
logging.basicConfig(level=logging.INFO)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    company_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip = db.Column(db.String(10))
    email = db.Column(db.String(120), unique=True, nullable=False)
    web = db.Column(db.String(120))
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company_name": self.company_name,
            "age": self.age,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "email": self.email,
            "web": self.web,
        }
    

db_initialized = False #initially the db is not there 
@app.before_request # decerator runs for every request
def setup():
    global db_initialized
    if db_initialized:
        return
    db.create_all() # create db table
    if not User.query.first(): #check table is empty
        logging.info("Loading users from JSON file")
        with open("users.json", "r") as f:
            users = json.load(f)
            for u in users:
                db.session.add(User(**u))#**u tahkes the values from dictionary and convert. into named arguments   
            db.session.commit()
    db_initialized = True


# GET /api/users
@app.route("/api/users", methods=["GET"])
def get_users():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))
    # Debug Purpose
    #print(page , limit)
    search = request.args.get("search")
    sort = request.args.get("sort")
    query = User.query
    if search:
        query = query.filter(
            (User.first_name.ilike(f"%{search}%")) | # same as like in MySQL
            (User.last_name.ilike(f"%{search}%"))
        )

    if sort:
        desc = sort.startswith("-")
        field = sort.lstrip("-")
        if not hasattr(User, field):
            return "",400
        query = query.order_by(
            getattr(User, field).desc() if desc else getattr(User, field)
        )
    users = query.offset((page - 1) * limit).limit(limit).all()# the offset is to specify the starting place
    return jsonify([u.to_dict() for u in users])


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if "email" not in data: # Check if email exists
        return jsonify({"error": "Email is required"}), 400
    email = data["email"]
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return jsonify({"error": "Invalid email format"}), 400
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    logging.info("New user is added")
    return jsonify(user.to_dict()), 201


# GET /api/users/{id}
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    logging.info("The user %s is displayed", user_id)
    return jsonify(user.to_dict())


# PUT /api/users/{id}
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    req = {
    "first_name", "last_name", "company_name",
    "age", "city", "state", "zip", "email", "web"
    }
    if not req.issubset(data.keys()):
        logging.info("include all fields")
        abort(400, "PUT request must contain all fields") #cancel if not all fields are present
    for key, value in data.items():
        setattr(user, key, value)
    logging.info("user data updated is added")
    db.session.commit()
    return jsonify(user.to_dict())


# PATCH /api/users/{id}
@app.route("/api/users/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    logging.info("user data patched is added")
    return jsonify(user.to_dict())


# DELETE /api/users/{id}
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    logging.info("The data is deleted")
    db.session.commit()
    return "", 201


# GET /api/users/summary
@app.route("/api/users/summary", methods=["GET"])
def user_summary():
    city_cnt = db.session.query(
        User.city, func.count(User.id)
    ).group_by(User.city).all()
    company_cnt = db.session.query(
    User.company_name, func.count(User.id)
    ).group_by(User.company_name).all()
    avg_age = db.session.query(func.avg(User.age)).scalar()

    return jsonify({
        "cnt_by_city": dict(city_cnt),
        "cnt_by_company": dict(company_cnt), 
        "avg_age": round(avg_age, 2) if avg_age else None
    })


if __name__ == "__main__":
    app.run(debug=True)

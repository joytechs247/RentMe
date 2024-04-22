
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scooter_rental.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Car model
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    year = db.Column(db.Integer)
    price = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    cars = Car.query.all()
    return render_template('index.html', cars=cars)

@app.route('/get_cars')
def get_cars():
    cars = Car.query.all()
    car_data = [{'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year, 'price': car.price, 'image_url': car.image_url} for car in cars]
    return jsonify(car_data)

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        image_url = request.form['image_url']
        description = request.form['description']

        new_car = Car(make=make, model=model, year=year, price=price, image_url=image_url, description=description)
        db.session.add(new_car)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('add_car.html')

@app.route('/car/<int:car_id>')
def car_details(car_id):
    car = Car.query.get(car_id)
    return render_template('car_details.html', car=car)

if __name__ == '__main__':
    app.run(debug=True)

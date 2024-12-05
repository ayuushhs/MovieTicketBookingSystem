from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model to store booking data
class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    theatre = db.Column(db.String(100), nullable=False)
    movie = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    screen = db.Column(db.String(50), nullable=False)
    popcorn_count = db.Column(db.Integer, nullable=False, default=0)
    coke_count = db.Column(db.Integer, nullable=False, default=0)
    total = db.Column(db.Float, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/book', methods=['POST'])
def book_ticket():
    data = request.json
    # Generating a random booking ID
    booking_id = random.randint(10000, 99999)
    
    # Extracting data from the request
    theatre = data['theatre']
    movie = data['movie']
    date = data['date']
    time = data['time']
    screen = data['screen']
    popcorn_count = data['popcorn_count']
    coke_count = data['coke_count']
    total = data['total']
    
    # Create new booking record
    new_booking = Booking(
        booking_id=booking_id,
        theatre=theatre,
        movie=movie,
        date=date,
        time=time,
        screen=screen,
        popcorn_count=popcorn_count,
        coke_count=coke_count,
        total=total
    )
    
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({
        'message': 'Booking confirmed!',
        'booking_id': booking_id
    })

@app.route('/cancel/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    # Find the booking by ID and delete it
    booking = Booking.query.filter_by(booking_id=booking_id).first()
    
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Booking canceled successfully!'})
    else:
        return jsonify({'message': 'Booking not found!'}), 404

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from uuid import uuid4

app = Flask(__name__)

# Models
class Screen:
    def __init__(self, screen_type, price, capacity):
        self.screen_type = screen_type
        self.price = price
        self.capacity = capacity
        self.booked_seats = []  # List of bookings
        self.waiting_list = []  # List of users in waiting list

class Theater:
    def __init__(self, theater_id, name, screens):
        self.theater_id = theater_id
        self.name = name
        self.screens = screens

class Booking:
    def __init__(self, user_id, screen_type, food_items, movie_time):
        self.booking_id = str(uuid4())
        self.user_id = user_id
        self.screen_type = screen_type
        self.food_items = food_items
        self.movie_time = movie_time
        self.created_at = datetime.now()
        self.total_price = 0

# Hardcoded theaters and screens
screens = {
    "Gold": Screen("Gold", 400, 2),
    "Max": Screen("Max", 300, 5),
    "General": Screen("General", 200, 10),
}

theaters = [
    Theater("1", "Theater A", screens),
    Theater("2", "Theater B", screens),
]

# Food pricing
FOOD_PRICES = {
    "Popcorn": 100,
    "Sandwich": 150
}

@app.route("/")
def home():
    return "Welcome to the Movie Theater Booking System!"


@app.route("/book", methods=["POST"])
def book_ticket():
    data = request.json
    theater_id = data.get("theater_id")
    screen_type = data.get("screen_type")
    food_items = data.get("food_items", [])
    movie_time = datetime.strptime(data.get("movie_time"), "%Y-%m-%d %H:%M:%S")
    user_id = data.get("user_id")

    theater = next((t for t in theaters if t.theater_id == theater_id), None)
    if not theater:
        return jsonify({"error": "Theater not found."}), 404

    screen = theater.screens.get(screen_type)
    if not screen:
        return jsonify({"error": "Screen type not found."}), 404

    # Check availability
    if len(screen.booked_seats) >= screen.capacity:
        if (movie_time - datetime.now()).total_seconds() < 1800:
            return jsonify({"error": "Bookings closed for this screen."}), 400
        screen.waiting_list.append(user_id)
        return jsonify({"message": "Added to waiting list."}), 200

    # Create booking
    booking = Booking(user_id, screen_type, food_items, movie_time)
    booking.total_price += screen.price

    # Calculate food cost
    food_cost = sum(FOOD_PRICES[item] for item in food_items)
    if screen_type == "Gold":
        food_cost *= 0.9  # 10% discount
    elif screen_type == "Max":
        food_cost *= 0.95  # 5% discount

    booking.total_price += food_cost
    screen.booked_seats.append(booking)

    return jsonify({"message": "Booking successful.", "booking_id": booking.booking_id, "total_price": booking.total_price}), 201

@app.route("/cancel", methods=["POST"])
def cancel_ticket():
    data = request.json
    theater_id = data.get("theater_id")
    booking_id = data.get("booking_id")

    theater = next((t for t in theaters if t.theater_id == theater_id), None)
    if not theater:
        return jsonify({"error": "Theater not found."}), 404

    # Find booking
    for screen in theater.screens.values():
        booking = next((b for b in screen.booked_seats if b.booking_id == booking_id), None)
        if booking:
            if (booking.movie_time - datetime.now()).total_seconds() < 1800:
                return jsonify({"error": "Cannot cancel within 30 minutes of movie time."}), 400

            # Remove booking and handle waiting list
            screen.booked_seats.remove(booking)
            if screen.waiting_list:
                next_user_id = screen.waiting_list.pop(0)
                new_booking = Booking(next_user_id, screen.screen_type, [], booking.movie_time)
                screen.booked_seats.append(new_booking)
                return jsonify({"message": "Booking cancelled and reassigned to waiting list user."}), 200

            return jsonify({"message": "Booking cancelled."}), 200

    return jsonify({"error": "Booking not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)

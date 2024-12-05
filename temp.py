# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABSE_URI'] = "sqlite:///movie.db"
# db = SQLAlchemy(app)

# class Todo(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     theatre = db.Column(db.string(200), nullable=False)
#     movie = db.Column(db.string(200), nullable=False)
#     date = db.Column(db.Date, default=datetime.utcnow().date)
#     time = db.Column(db.Time, default=datetime.utcnow().time)

# @app.route('/booking', method=['POST'])
# def booking():
#     theatre = request.form['theatre']
#     movie = request.form['movie']

#     new_booking = Booking(theatre=theatre, movie=movie, date=datetime.utcnow())
    
#     return render_template('booking.html')




# @app.route('/Home')
# def Home():
#     return render_template('index.html')

# @app.route('/About')
# def About():
#     return render_template('about.html')


# @app.route('/Packages')
# def Packages():
#     return render_template('packages.html')

# if __name__ == "__main__":
#     app.run(debug=True, port=8000)

# --------------------------------------------------------------

# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)


# @app.route('/Home')
# def Home():
#     return render_template('index.html')

# @app.route('/About')
# def About():
#     return render_template('about.html')


# @app.route('/Packages')
# def Packages():
#     return render_template('packages.html')

# @app.route('/booking')
# def booking():
#     return render_template('booking.html')


# if __name__ == "__main__":
#     app.run(debug=True, port=8000)




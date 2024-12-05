from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form.get('name')
    time = request.form.get('time')
    return f"Hello, {name}! You entered the time as {time}."

if __name__ == '__main__':
    app.run(debug=True)

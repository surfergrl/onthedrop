from flask import Flask

app = Flask(__name__)

print(dir(app))

@app.before_first_request
def test_decorator():
    print("This runs before the first request")

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
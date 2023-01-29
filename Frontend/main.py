from flask import Flask, render_template
from nlpModel import classify
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    print("Going Form")
    return render_template('form.html')

@app.route('/test')
def test():
    return "test"
if __name__ == "__main__":
    # print(classify("I love this product", "product"))
    app.run(host="0.0.0.0", port=5100, debug=True)
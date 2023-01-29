from flask import Flask, render_template, request
# from nlpModel import classify
from elkDataIngest import ingestData
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=('GET', 'POST'))
def form():
    print("Going Form")
    if request.method == 'POST':
        print("POST")

        error = ""
        name = request.form['name']
        aspect = request.form['aspect']
        feedback = request.form['feedback']
        print("from stuff -- " + name, aspect, feedback)
        if not aspect:
            error += "Aspect, "
        if not feedback:
            error += "Feedback, "
        if error:
            print("form incomplete")
            return render_template('form.html', error="Please fill all the fields: " + error[:-2])

        return "success"
    else:
        return render_template('form.html')

@app.route('/test')
def test():
    return "test"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
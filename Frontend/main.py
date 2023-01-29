from flask import Flask, render_template, request
# from nlpModel import classify
from elkDataIngest import ingestData
from firestore import db
import json
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
        else:
            print("form complete")
            ingestData(name, aspect, feedback)
            return render_template('thankyou.html')

    else:
        return render_template('form.html')

@app.route('/test')
def test():
    return "test"

@app.route('/getdata')
def getdata():
    coll_ref = db.collection('customer_review_data')
    # Using coll_ref.stream() is more efficient than coll_ref.get()
    docs = coll_ref.stream()
    res = [] 
    for doc in docs:
        res.append(doc.to_dict())
        # print(f'{doc.id} => {doc.to_dict()}')
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
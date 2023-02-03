from flask import Flask, render_template, request
# from nlpModel import classify
from elkDataIngest import ingestData
from firestore import db
import json
from yolo_demo.detect_function import run
import os

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
        image = request.files['image']
        name = request.form['name']
        aspect = request.form['aspect']
        feedback = request.form['feedback']
        print("from stuff -- " + name, aspect, feedback)
        if not aspect:
            error += "Aspect, "
        if not feedback:
            error += "Feedback, "
        if not image:
            error += "Image, "
        if error:
            print("form incomplete")
            return render_template('form.html', error="Please fill all the fields: " + error[:-2])
        else:
            image.save(image.filename)
            # print("image saved")
            # print("image name: " + image.filename)
            result = run(detect_object="laptop", source=image.filename)
            print(result)
            print("form complete")
            ingestData(name, aspect, feedback, result)
            os.remove(image.filename)
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

@app.route('/results')
def results():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
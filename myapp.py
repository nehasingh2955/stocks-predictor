from flask import Flask, render_template
import nlp_test
import graph
import os

app = Flask(__name__)

classifier = None
runOnce = True
accuracy = ""

@app.route("/")
def home():
    global runOnce
    global classifier
    global accuracy
    if runOnce:
        tup = nlp_test.train_model()
        classifier = tup[0]
        accuracy = tup[1]
        runOnce = False
    return render_template('index.html')

@app.route("/aapl")
def appl():
    global classifier
    output = nlp_test.main("apple", classifier)
    output = output.replace("\n", "<br>")
    graph.graph("AAPL")
    return render_template('page.html', name="Apple Prediction", output=output, accuracy=accuracy)

@app.route("/uber", methods=["GET"])
def uber():
    global classifier
    output = nlp_test.main("uber", classifier)
    output = output.replace("\n", "<br>")
    graph.graph("UBER")
    return render_template('page.html', name="Uber Prediction", output=output, accuracy=accuracy)

@app.route("/lyft")
def lyft():
    global classifier
    output = nlp_test.main("lyft", classifier)
    output = output.replace("\n", "<br>")
    graph.graph("LYFT")
    return render_template('page.html', name="Lyft", output=output, accuracy=accuracy)


if __name__ == '__main__':
    app.run(debug=True)
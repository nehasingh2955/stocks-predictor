from flask import Flask, render_template
import nlp_test
import graph
import os
import datetime

app = Flask(__name__)

def predict_value(calculated_val, positive, negative):
    return "{:.2f}".format(calculated_val + (positive/calculated_val) - (negative/calculated_val))

def calculate(coef, x):
    l = len(coef) - 1
    s = 0
    for i in range(len(coef)):
        s += (x**i) * coef[l-i]
    return s

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
    tmrw = datetime.date.today() + datetime.timedelta(days=1)
    d = tmrw.strftime("%B %d, %Y")
    return render_template('index.html', date=d)

@app.route("/aapl")
def appl():
    global classifier
    nlp_results = nlp_test.main("apple", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("AAPL")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Apple Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/uber", methods=["GET"])
def uber():
    global classifier
    nlp_results = nlp_test.main("uber", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("UBER")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Uber Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/lyft")
def lyft():
    global classifier
    nlp_results = nlp_test.main("lyft", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("LYFT")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Lyft Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/facebook")
def facebook():
    global classifier
    nlp_results = nlp_test.main("facebook", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("FB")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Facebook Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/tesla")
def tesla():
    global classifier
    nlp_results = nlp_test.main("tesla", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("TSLA")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Tesla Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/google")
def google():
    global classifier
    nlp_results = nlp_test.main("google", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("GOOGL")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Google Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/amazon")
def amazon():
    global classifier
    nlp_results = nlp_test.main("amazon", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("AMZN")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Amazon Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/microsoft")
def microsoft():
    global classifier
    nlp_results = nlp_test.main("microsoft", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("MSFT")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Microsoft Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/nvidia")
def nvidia():
    global classifier
    nlp_results = nlp_test.main("nvidia", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("NVDA")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Nvidia Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/netflix")
def netflix():
    global classifier
    nlp_results = nlp_test.main("netflix", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("NFLX")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Netflix Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/twitter")
def twitter():
    global classifier
    nlp_results = nlp_test.main("twitter", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("TWTR")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Twitter Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)

@app.route("/snap")
def snap():
    global classifier
    nlp_results = nlp_test.main("snap inc", classifier)
    output = nlp_results[0]
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = output.replace("\n", "<br>")
    tup = graph.graph("SNAP")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)
    return render_template('generic.html', name="Snap Inc. Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template
import nlp_test
import graph
import os
import datetime

app = Flask(__name__)

def predict_value(calculated_val, positive, negative):
    return calculated_val + (positive/calculated_val) - (negative/calculated_val)

def calculate(coef, x):
    l = len(coef) - 1
    s = 0
    for i in range(len(coef)):
        s += (x**i) * coef[l-i]
    return s


def convert_output(output, positive, negative):
    to_return = "Positive: <span style=\"color:#00ff00;\">" + str(positive) + "</span>" + " Negative: <span style=\"color:#FF0000;\">" + str(negative) + "</span><br>"
    
    for tup in output:
        title = tup[0]
        url = tup[1]
        sentiment = tup[2]

        if sentiment == "Positive":
            color = "#00ff00";
        else:
            color = "#FF0000"

        to_return += "<a href=\"" + url + "\">" + title + "</a> " + "<span style=\"float:right; color:" + color + ";\">" + sentiment + "</span>" + "<br>"
    
    return to_return



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
    today = datetime.date.today()

    day_of_week = today.weekday()
    if day_of_week >= 4:
        delta = 7 - day_of_week
    else:
        delta = 1

    tmrw = today + datetime.timedelta(days=delta)
    d = tmrw.strftime("%B %d, %Y")
    return render_template('index.html', date=d)

@app.route("/aapl")
def appl():
    global classifier
    nlp_results = nlp_test.main("apple", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("AAPL")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)


    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Apple Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/uber", methods=["GET"])
def uber():
    global classifier
    nlp_results = nlp_test.main("uber", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("UBER")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Uber Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/lyft")
def lyft():
    global classifier
    nlp_results = nlp_test.main("lyft", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("LYFT")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Lyft Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/facebook")
def facebook():
    global classifier
    nlp_results = nlp_test.main("facebook", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("FB")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Facebook Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/tesla")
def tesla():
    global classifier
    nlp_results = nlp_test.main("tesla", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("TSLA")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Tesla Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/google")
def google():
    global classifier
    nlp_results = nlp_test.main("google", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("GOOGL")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Google Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/amazon")
def amazon():
    global classifier
    nlp_results = nlp_test.main("amazon", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("AMZN")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Amazon Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/microsoft")
def microsoft():
    global classifier
    nlp_results = nlp_test.main("microsoft", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("MSFT")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Microsoft Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/nvidia")
def nvidia():
    global classifier
    nlp_results = nlp_test.main("nvidia", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("NVDA")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Nvidia Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/netflix")
def netflix():
    global classifier
    nlp_results = nlp_test.main("netflix", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("NFLX")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Netflix Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/twitter")
def twitter():
    global classifier
    nlp_results = nlp_test.main("twitter", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("TWTR")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Twitter Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/snap")
def snap():
    global classifier
    nlp_results = nlp_test.main("snap inc", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("SNAP")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Snap Inc. Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/salesforce")
def salesforce():
    global classifier
    nlp_results = nlp_test.main("salesforce", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("CRM")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Salesforce Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

@app.route("/splunk")
def splunk():
    global classifier
    nlp_results = nlp_test.main("Splunk", classifier)
    positive = nlp_results[1]
    negative = nlp_results[2]
    output = convert_output(nlp_results[0], positive, negative)
    tup = graph.graph("SPLK")
    plot_url = tup[0]
    coef = tup[1]
    x = tup[2] + 1
    calculated_val = calculate(coef, x)
    predicted_value = predict_value(calculated_val, positive, negative)

    prev_value = tup[3]
    if predicted_value > prev_value:
        img_src = "../static/images/trending-up.svg"
    elif predicted_value < prev_value:
        img_src = "../static/images/trending-down.svg"

    predicted_value = "{:.2f}".format(predicted_value)

    return render_template('generic.html', name="Splunk Prediction", output=output, 
        accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)


if __name__ == '__main__':
    app.run(debug=True)
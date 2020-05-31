from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import nlp_test
import graph
import os
import datetime
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import yfinance as yf

app = Flask(__name__)

#database start--------------------------------------------------------

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class User(db.Model):
    username = db.Column(db.String, primary_key=True, unique=True)
    password = db.Column(db.String)
    companies = db.Column(db.String)

    def __init__(self, username, password, companies):
        self.username = username
        self.password = password
        self.companies = companies


class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password', 'companies')
 
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    password = request.json['password']
    companies = request.json['companies']

    new_user = User(username, password, companies)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = User.query.get(username)
    return user_schema.jsonify(user)

@app.route('/user/<username>', methods=['PUT'])
def update_user(username):
    user = User.query.get(username)
    username = request.json['username']
    password = request.json['password']
    companies = request.json['companies']

    user.username = username
    user.password = password
    user.companies = companies

    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/user/<username>/add', methods=['PUT'])
def update_user_companies(username):
    user = User.query.get(username)
    company = request.json['company']

    user_list = json.loads(user.companies)
    user_list.append(company)
    user.companies = json.dumps(user_list)

    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/user/<username>/delete', methods=['PUT'])
def delete_user_companies(username):
    user = User.query.get(username)
    company = request.json['company']

    user_list = json.loads(user.companies)
    if company in user_list:
        user_list.remove(company)
    user.companies = json.dumps(user_list)

    db.session.commit()

    return user_schema.jsonify(user)



@app.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


#user should not have this power
@app.route('/user', methods=['DELETE'])
def delete_all():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

#-----------------------------------------------------------------------------

#helper analysis methods------------------------------------------------------

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

#-----------------------------------------------------------------------------------

classifier = None
runOnce = True
accuracy = ""

username = None
user_list = None


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global username
        global user_list
        entered_username = request.form['username']
        entered_password = request.form['password']

        temp_user = User.query.get(entered_username)

        if temp_user is not None:
            print("Entered password: ", entered_password)
            print("Correct password: ", temp_user.password)
            if entered_password == temp_user.password:
                username = temp_user.username
                print(temp_user.companies)
                user_list = json.loads(temp_user.companies)
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route("/logout")
def logout():
    global username
    global user_list

    username = None
    user_list = None
    return redirect(url_for('home'))



@app.route("/")
def home():
    global runOnce
    global classifier
    global accuracy
    global username
    global user_list

    if username == None and user_list == None:
        user = User.query.get("guest")
        username = user.username
        user_list = json.loads(user.companies)

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
    return render_template('index.html', date=d, list=user_list, username=username)

# @app.route("/<company>")
# def showinfo(company):
#     url = ('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' + company + '&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback')
#     response = requests.get(url)

#     json_file = response.json()

#     ticker = json_file['ResultSet']["Result"][0]["Symbol"]
#     print(ticker)
@app.route("/<company>")
def getinfo(company):
    is_in = False
    ticker = ""
    for item in user_list:
        if item[0] == company:
            is_in = True
            ticker = item[1]
            break
    if is_in:
        global classifier
        print(company)
        nlp_results = nlp_test.main(company, classifier)
        positive = nlp_results[1]
        negative = nlp_results[2]
        output = convert_output(nlp_results[0], positive, negative)
        print(output)

        tup = graph.graph(ticker)
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

        return render_template('generic.html', name=company + " Prediction", output=output, 
            accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src, list=user_list, username=username)
    else:
        return redirect(url_for('home'))




# @app.route("/aapl")
# def appl():
#     global classifier
#     nlp_results = nlp_test.main("apple", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)

#     tup = graph.graph("AAPL")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)


#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Apple Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/uber", methods=["GET"])
# def uber():
#     global classifier
#     nlp_results = nlp_test.main("uber", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("UBER")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Uber Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/lyft")
# def lyft():
#     global classifier
#     nlp_results = nlp_test.main("lyft", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("LYFT")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Lyft Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/facebook")
# def facebook():
#     global classifier
#     nlp_results = nlp_test.main("facebook", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("FB")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Facebook Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/tesla")
# def tesla():
#     global classifier
#     nlp_results = nlp_test.main("tesla", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("TSLA")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Tesla Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/google")
# def google():
#     global classifier
#     nlp_results = nlp_test.main("google", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("GOOGL")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Google Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/amazon")
# def amazon():
#     global classifier
#     nlp_results = nlp_test.main("amazon", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("AMZN")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Amazon Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/microsoft")
# def microsoft():
#     global classifier
#     nlp_results = nlp_test.main("microsoft", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("MSFT")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Microsoft Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/nvidia")
# def nvidia():
#     global classifier
#     nlp_results = nlp_test.main("nvidia", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("NVDA")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Nvidia Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/netflix")
# def netflix():
#     global classifier
#     nlp_results = nlp_test.main("netflix", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("NFLX")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Netflix Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/twitter")
# def twitter():
#     global classifier
#     nlp_results = nlp_test.main("twitter", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("TWTR")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Twitter Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/snap")
# def snap():
#     global classifier
#     nlp_results = nlp_test.main("snap inc", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("SNAP")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Snap Inc. Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/salesforce")
# def salesforce():
#     global classifier
#     nlp_results = nlp_test.main("salesforce", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("CRM")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Salesforce Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)

# @app.route("/splunk")
# def splunk():
#     global classifier
#     nlp_results = nlp_test.main("Splunk", classifier)
#     positive = nlp_results[1]
#     negative = nlp_results[2]
#     output = convert_output(nlp_results[0], positive, negative)
#     tup = graph.graph("SPLK")
#     plot_url = tup[0]
#     coef = tup[1]
#     x = tup[2] + 1
#     calculated_val = calculate(coef, x)
#     predicted_value = predict_value(calculated_val, positive, negative)

#     prev_value = tup[3]
#     if predicted_value > prev_value:
#         img_src = "../static/images/trending-up.svg"
#     elif predicted_value < prev_value:
#         img_src = "../static/images/trending-down.svg"

#     predicted_value = "{:.2f}".format(predicted_value)

#     return render_template('generic.html', name="Splunk Prediction", output=output, 
#         accuracy=accuracy, plot_url=plot_url, predicted_value=predicted_value, img_src=img_src)


if __name__ == '__main__':
    app.run(debug=True)
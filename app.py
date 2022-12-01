from flask import Flask, render_template, request, redirect, url_for, session
import warnings
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = 'raga'

class_labels = {0: "Apple_scab", 1: "Black_rot", 2: "Cedar_apple_rust", 3: "healthy"}

model = load_model("model/DenseNet201_model.h5")


def predict_label(img_path):
    filepath = img_path
    image = load_img(filepath, grayscale=False, color_mode='rgb', target_size=(256, 256))
    image = img_to_array(image)
    image = image / 255.0
    expanded_image = np.expand_dims(image, axis=0)
    model_prediction = model.predict(expanded_image, verbose=1)
    x = np.argmax(model_prediction[0])
    print(f"model predicted class is -> {x}")
    res = class_labels[x]
    print(f"model predicted label is -> {res}")
    return res


@app.route("/submit", methods=['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
        img = request.files['image']
        file = "static/" + img.filename
        img.save(file)
        p = predict_label(file)
        return render_template("home.html", prediction=p, img_path=file)


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["password"]
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["email"] == str(email) and row["password"] == str(pwd):

                return redirect(url_for('home'))
        else:
            mesg = 'Invalid Login Try Again'
            return render_template('login.html', msg=mesg)
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        password = request.form['Password']
        col_list = ["name", "email", "password"]
        r1 = pd.read_excel('user.xlsx', usecols=col_list)
        new_row = {'name': name, 'email': email, 'password': password}
        r1 = r1.append(new_row, ignore_index=True)
        r1.to_excel('user.xlsx', index=False)
        print("Records created successfully")
        # msg = 'Entered Mail ID Already Existed'
        msg = 'Registration Successfull !! U Can login Here !!!'
        return render_template('login.html', msg=msg)
    return render_template('register.html')


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/password', methods=['POST', 'GET'])
def password():
    if request.method == 'POST':
        current_pass = request.form['current']
        new_pass = request.form['new']
        verify_pass = request.form['verify']
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["password"] == str(current_pass):
                if new_pass == verify_pass:
                    r1.replace(to_replace=current_pass, value=verify_pass, inplace=True)
                    r1.to_excel("user.xlsx", index=False)
                    msg1 = 'Password changed successfully'
                    return render_template('password_change.html', msg1=msg1)
                else:
                    msg2 = 'Re-entered password is not matched'
                    return render_template('password.html', msg2=msg2)
        else:
            msg3 = 'Incorrect password'
            return render_template('password.html', msg3=msg3)
    return render_template('password.html')



@app.route('/logout')
def logout():
    session.clear()
    msg='You are now logged out', 'success'
    return redirect(url_for('login', msg=msg))


if __name__ == '__main__':
    app.run(debug=True)

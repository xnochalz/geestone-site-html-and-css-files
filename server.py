from flask import Flask, render_template
import random
import datetime
import requests



app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sample')
def sample():
    random_number = random.randint(1, 20)
    answer = random_number * 2
    current_year = datetime.datetime.now().year
    return render_template('web.html', response=random_number, num=answer, year=current_year)

@app.route('/guess/<name>')
def guess(name):
    gender_url = f'https://api.genderize.io?name={name}'
    gender_response = requests.get(gender_url)
    gender_data = gender_response.json()
    gender = gender_data['gender']
    age_url = f'https://api.agify.io?name={name}'
    age_response = requests.get(age_url)
    age_data = age_response.json()
    age = age_data['age']
    current_year = datetime.datetime.now().year
    return render_template('guess.html', person_name=name, gender=gender, age=age, year=current_year)


@app.route('/blog')
def blog():

    return render_template('blog.html')


@app.route('/wounds', methods=["GET"])
def woundcare():

    return render_template('woundcare.html')

@app.route('/', methods=['GET'])
def dropdown():
    extent_of_tissue = ['cough', 'Enviromental_Factors', 'Dysponia', 'Catarrh'
                        ' Cyanosis', ' Psychological_Factors', ' Smoking',
                        'Nose Pains', 'Chest X-ray', 'Chest Pain']
    return render_template('woundcare.html', colours=extent_of_tissue)



if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired, NumberRange
import pickle

#Create Flask instance
app = Flask(__name__)
#create a secret key
app.config["SECRET_KEY"] = "much_secret"

#create form for iris
class IrisData(FlaskForm):
    sepal_length = FloatField("Sepal length", validators=[InputRequired(), NumberRange(min=4, max=8, message="insert number from 4 to 8")])
    sepal_width = FloatField("Sepal width", validators=[InputRequired(), NumberRange(min=2, max=5, message="insert number from 2 to 5")])
    petal_length = FloatField("Petal length", validators=[InputRequired(), NumberRange(min=1, max=7, message="insert number from 1 to 7")])
    petal_width = FloatField("Petal width", validators=[InputRequired(), NumberRange(min=0.1, max=3, message="insert number from 0.1 to 3")])
    submit = SubmitField("submit")

#Create route decorator for index
@app.route('/')
def index():

    return render_template("index.html")


# Machine learning assignemnt
@app.route("/iris", methods=["GET"])
def iris():
    form = IrisData()
    return render_template("iris2.html", form=form)


@app.route("/iris", methods=["POST"])
def iris_post():
    form = IrisData()


    sepal_length = form.sepal_length.data
    sepal_width = form.sepal_width.data
    petal_length = form.petal_length.data
    petal_width = form.petal_width.data

    prediction = iris_prediction([sepal_length, sepal_width, petal_length, petal_width])
    prediction = str(prediction[0])


    if prediction == "setosa":
        image = "https://en.wikipedia.org/wiki/Iris_setosa#/media/File:Irissetosa1.jpg"
    elif prediction == "virginica":
        image = "https://upload.wikimedia.org/wikipedia/commons/f/f8/Iris_virginica_2.jpg"
    else:
        image = "https://en.wikipedia.org/wiki/Iris_versicolor#/media/File:Blue_Flag,_Ottawa.jpg"

    if form.validate_on_submit():
        return render_template("iris_result.html", form=form, prediction=prediction, image=image)
    else:
        return render_template("iris2.html", form=form)


def iris_prediction(iris_data: list):
    pickled_model = open('iris_predictor.pickle', 'rb')
    model = pickle.load(pickled_model)
    prediction = model.predict([iris_data])

    return prediction


if __name__ == '__main__':
    app.run(debug=True)
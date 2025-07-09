from flask import Flask,render_template,request
from src.pipelines.prediction_pipeline import PredictionPipeline,CustomData


application = Flask(__name__)
app = application


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict",methods = ["GET","POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")
    else:
        data = CustomData(
            gender=request.form["gender"],
            reading_score=float(request.form["reading_score"]),
            parental_level_of_education=request.form["parental_level_of_education"],
            lunch=request.form["lunch"],
            test_preparation_course=request.form["test_preparation_course"],
            race_ethnicity=request.form["ethnicity"],
            writing_score=float(request.form["writing_score"]),

        )

        param = data.get_data_as_dataframe()
        predict_pipeline = PredictionPipeline()
        prediction = predict_pipeline.predict(param)

        return render_template("predict.html",prediction=prediction[0])



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=4000,debug=True)
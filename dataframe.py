from flask import Flask, render_template, request
import google.generativeai as genai
import json
import pandas as pd

##initializing the flask app
app= Flask(__name__)

genai.configure(api_key="AIzaSyCrQKtsRFssldlEidyJahun7lpprmSBhDI")
model1 = genai.GenerativeModel(model_name='gemini-1.5-flash')
##method to grab the inputs from the index.html file colin made. reguest.form.get allows me to post the inputs into the api call as variables to generate workouts
@app.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
       Age=request.form.get("age")
       experience=request.form.get("experience")
       Frequency=request.form.get("Frequency")
       equipment=request.form.get("equipment")

       prompt = f'''create me a 7-day workout plan for a user who is {Age} years old. This user has {experience} years of experience. They want to lift only on these days: {Frequency}.Keep in mind that they only have this equipment: {equipment}. Each day should include workouts with fields: "Workout", "Sets", and "Reps".
       Return raw JSON with days of the week as keys: monday, tuesday, ..., sunday.'''

       response = model1.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
       ## just strips out white space from the response only extracting what we need
       output = response.text.strip()
       ##json.loads allows me to convert the json string that was given from gemini into a json format, followed by puting the json into a dataframee
       data = json.loads(output)
       df = pd.DataFrame(data)
    ##returns the dataframe into a html formatted version of the pd.dataframe.
       return df.to_html()
   
   return render_template('index.html')

if __name__ == "__main__":
   app.run(debug=True)

   ##next steps: format the dataframe so it is optimized for HTML and shows weekdays diagonally
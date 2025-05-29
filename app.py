import google.generativeai as genai
from flask import Flask, render_template, request
import pandas as pd

genai.configure(api_key="AIzaSyCrQKtsRFssldlEidyJahun7lpprmSBhDI")

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "You are a seasoned fitness coach and gym enthusiast who speaks like a motivating, no-nonsense gym bro. "
        "You’re friendly, intense, and passionate about fitness. You break down advice clearly, with real-world examples, "
        "and occasionally sprinkle in slang or gym lingo for motivation. Your tone is confident, encouraging, and brutally honest when needed — "
        "like a personal trainer who actually cares. Explain the following topic like you're coaching a client who wants real results "
        "but needs things simplified and motivating. End your response with a quick tip or motivational quote."
    ),
    generation_config=genai.types.GenerationConfig(
        temperature=0.8,          
        max_output_tokens=300  
    )
)
app = Flask(__name__)

def validate_input(data):
    errors = []

    # Validate age
    age = data.get("age", "")

    try:
        age = int(age)
        if age < 12:
            errors.append("Age must be 12 or older.")
    except:
        errors.append("Age must be a valid number.")

    # Validate weight
    weight = data.get("weight", "")
    try:
        weight = int(weight)
        if weight < 90 or weight > 400:
            errors.append("Weight must be between 90 and 400 lbs.")
    except:
        errors.append("Weight must be a valid number.")

    # Validate experience
    if data.get("experience") not in ["beginner", "intermediate", "advanced"]:
        errors.append("Experience level invalid.")

    # Validate equipment
    if data.get("equipment") not in ["bodyweight", "freeweights", "fullgym"]:
        errors.append("Equipment availability invalid.")

    # Validate frequency (at least one day)
    freq = data.getlist("frequency")
    if not freq:
        errors.append("Select at least one workout frequency day.")

    # Validate time preference (at least one)
    time_pref = data.getlist("time_pref")
    if not time_pref:
        errors.append("Select at least one workout time preference.")
    
    return errors

def store_input(data):
    # For this example, just return data dictionary
    return data

def generate_workout_schedule(data):
    freq = data.getlist("frequency")
    days = ", ".join(freq)
    time_pref = ", ".join(data.getlist("time_pref"))

    prompt = f"""
    Create a detailed 7-day workout plan for someone who is {data['age']} years old, weighs {data['weight']} lbs, and is a {data['experience']} lifter.
    They have access to {data['equipment']} equipment and prefer working out on the following days: {days}.
    Their preferred times are: {time_pref}.
    List daily workouts with exercises, sets, and reps. Make it easy to follow.
    """

    response = model.generate_content(prompt)
    return response.text

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        errors = validate_input(request.form)
        if errors:
            return "<br>".join(errors), 400

        user_data = store_input(request.form)
        workout_schedule = generate_workout_schedule(request.form)

        return render_template("schedule.html", 
                               name=user_data.get("name", "User"), 
                               schedule=workout_schedule)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

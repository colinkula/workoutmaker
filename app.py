from flask import Flask, render_template, request
import pandas as pd

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
    # Example: create a simple pandas DataFrame with dummy workouts per day selected
    freq = data.getlist("frequency")
    
    # Example reps and sets based on experience level (simplified)
    reps = {"beginner": "8-12", "intermediate": "10-15", "advanced": "12-20"}
    sets = {"beginner": 3, "intermediate": 4, "advanced": 5}

    workout_list = ["Squats", "Push-ups", "Pull-ups", "Lunges", "Plank"]
    schedule_data = []
    for day in freq:
        for w in workout_list:
            schedule_data.append({
                "Day": day,
                "Workout": w,
                "Reps": reps[data["experience"]],
                "Sets": sets[data["experience"]],
            })
    df = pd.DataFrame(schedule_data)
    return df.to_string(index=False)

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

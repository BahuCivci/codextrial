from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    diet_plan = None
    if request.method == 'POST':
        name = request.form.get('name', 'User')
        age = int(request.form.get('age', 0))
        gender = request.form.get('gender', 'other')
        weight = float(request.form.get('weight', 0))
        height = float(request.form.get('height', 0))
        goal = request.form.get('goal', 'maintain')

        # Simple Basal Metabolic Rate (BMR) calculation using Mifflin-St Jeor Equation
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        elif gender == 'female':
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age

        # Adjust calories based on goal
        if goal == 'lose':
            calories = bmr - 500
        elif goal == 'gain':
            calories = bmr + 500
        else:
            calories = bmr

        # Simple diet plan output
        diet_plan = {
            'name': name,
            'calories': round(calories),
            'meals': [
                {'meal': 'Breakfast', 'details': 'Protein + Complex Carbs + Fruit'},
                {'meal': 'Lunch', 'details': 'Lean Protein + Vegetables + Whole Grain'},
                {'meal': 'Snack', 'details': 'Nuts or Yogurt'},
                {'meal': 'Dinner', 'details': 'Protein + Vegetables + Healthy Fats'}
            ]
        }

    return render_template('index.html', diet_plan=diet_plan)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

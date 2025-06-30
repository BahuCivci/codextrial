from flask import Flask, render_template, request

app = Flask(__name__)


def calculate_plan(data):
    weight = float(data['weight'])
    height = float(data['height'])
    age = int(data['age'])
    gender = data['gender']
    activity = data['activity']
    goal = data['goal']
    diet = data['diet']

    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age

    factor = {'low': 1.2, 'moderate': 1.55, 'high': 1.725}.get(activity, 1.2)
    calories = bmr * factor

    if goal == 'lose':
        calories -= 500
    elif goal == 'gain':
        calories += 500

    carbs = calories * 0.4 / 4
    protein = calories * 0.3 / 4
    fat = calories * 0.3 / 9
    water_l = weight * 0.033

    meal_names = {
        'omnivore': {
            'Breakfast': 'Scrambled eggs with vegetables',
            'Snack1': 'Greek yogurt with berries',
            'Lunch': 'Grilled chicken salad',
            'Snack2': 'Mixed nuts',
            'Dinner': 'Baked fish with quinoa'
        },
        'vegetarian': {
            'Breakfast': 'Oatmeal with fruit',
            'Snack1': 'Cheese and crackers',
            'Lunch': 'Lentil soup with bread',
            'Snack2': 'Fruit smoothie',
            'Dinner': 'Vegetable stir fry with tofu'
        },
        'vegan': {
            'Breakfast': 'Tofu scramble with veggies',
            'Snack1': 'Hummus with carrots',
            'Lunch': 'Quinoa and bean salad',
            'Snack2': 'Trail mix',
            'Dinner': 'Chickpea curry with rice'
        }
    }[diet]

    ratios = {
        'Breakfast': 0.25,
        'Snack1': 0.1,
        'Lunch': 0.3,
        'Snack2': 0.1,
        'Dinner': 0.25
    }

    week = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        meals = []
        for name, recipe in meal_names.items():
            meals.append({'name': name, 'recipe': recipe, 'cal': round(calories * ratios[name])})
        week.append({'day': day, 'meals': meals})

    return {
        'calories': round(calories),
        'protein': round(protein),
        'carbs': round(carbs),
        'fat': round(fat),
        'water_l': round(water_l, 1),
        'week': week
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/plan', methods=['GET', 'POST'])
def plan():
    plan_data = None
    if request.method == 'POST':
        form_data = {
            'name': request.form.get('name', ''),
            'age': request.form.get('age', 0),
            'gender': request.form.get('gender', 'other'),
            'height': request.form.get('height', 0),
            'weight': request.form.get('weight', 0),
            'activity': request.form.get('activity', 'low'),
            'goal': request.form.get('goal', 'maintain'),
            'diet': request.form.get('diet', 'omnivore')
        }
        plan_data = calculate_plan(form_data)
    return render_template('plan.html', plan=plan_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

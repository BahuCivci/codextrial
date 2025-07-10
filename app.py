from flask import Flask, render_template, request

app = Flask(__name__)

temperaments = {
    "sanguine": "Sanguine: lively, sociable, and pleasure-seeking.",
    "choleric": "Choleric: ambitious, leader-like, and energetic.",
    "melancholic": "Melancholic: analytical, detail-oriented, and thoughtful.",
    "phlegmatic": "Phlegmatic: relaxed, peaceful, and quiet."
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        answers = [
            request.form.get('q1'),
            request.form.get('q2'),
            request.form.get('q3'),
            request.form.get('q4')
        ]
        score = {}
        for ans in answers:
            if ans:
                score[ans] = score.get(ans, 0) + 1
        if score:
            temperament = max(score, key=score.get)
            result = temperaments[temperament]
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

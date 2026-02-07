# app.py
# Stabilna wersja badania – walidacja, czas reakcji, kapitał, losowe wyniki dla niepewnych opcji

from flask import Flask, render_template_string, request, redirect, session
import csv, os, uuid, time, random, re

app = Flask(__name__)
app.secret_key = "VERY_SECRET_KEY"

RESULTS_FILE = "wyniki.csv"

# ================= PYTANIA =================
# correct = odpowiedź racjonalna wg teorii (TYLKO DO TWOJEJ WIEDZY)
QUESTIONS = [
    {
    "id": 0,
    "type": "risk_threshold",
    "text": "Reszka oznacza że tracisz 100zł, a orzeł że możesz wygrać. Jaką najniższą wartość musiałby wynosić orzeł żebyś zgodził/a się wziąć udział w zakładzie?",
    "options": [
        "Orzeł: +150 zł | Reszka: −100 zł",
        "Orzeł: +200 zł | Reszka: −100 zł",
        "Orzeł: +250 zł | Reszka: −100 zł",
        "Orzeł: +300 zł | Reszka: −100 zł",
        "Orzeł: +350 zł | Reszka: −100 zł",
        "Orzeł: +400 zł | Reszka: −100 zł",
        "Orzeł: +450 zł | Reszka: −100 zł",
        "Nie zgodził(a)bym się na żaden"
    ],
    "time": 40
    },  
    {
        "id": 1,
        "text": "Zainwestowałeś/aś 1 000 zł. Po 5 minutach Twoje saldo wynosi 1 200 zł (+200 zł zysku). Co robisz?",
        "A_label": "Zamykasz pozycję i wypłacasz pewne 1 200 zł.",
        "B_label": "Zostawiasz pieniądze na kolejne 5 minut, wiedząc, że masz: 50% szans, że zysk wzrośnie do 400 zł (saldo 1 400 zł) lub spadnie do 0 zł (saldo 1 000 zł).",
        "time": 25
    },
    {
        "id": 2,
        "text": "Wolisz na 80% stracić 250zł (istnieje 20% szans, że nie stracisz nic) czy na 100% stracić 200zł?",
        "A_label": "na 80% stracić 250 (20% szans na stratę 0zł)",
        "B_label": "na 100% stracić 200zł",  
        "time": 20
    },
   {
        "id": 3,
        "text": "Wolisz na 80% zyskać 250zł czy na 100% zyskać 200zł?",
        "A_label": "na 80% zyskać 250zł",
        "B_label": "na 100% zyskać 200zł",
        "time": 15
    },
    {
        "id": 4,
        "text": "Wolisz na 80% stracić 1 500zł (istnieje 20% szans, że nie stracisz nic) czy na 100% stracić 1 200zł?",
        "A_label": "na 80% stracić 1 500zł (20% szans na stratę 0zł)",
        "B_label": "na 100% stracić 1 200zł",
        "time": 20
    },
    {
        "id": 5,
        "text": "Wolisz na 80% zyskać 1 500zł czy na 100% zyskać 1 200zł?",
        "A_label": "na 80% zyskać 1 500zł",
        "B_label": "na 100% zyskać 1 200zł",
        "time": 15
    },
    {
        "id": 6,
        "text": "Wolisz na 80% stracić 5 000zł (istnieje 20% szans, że nie stracisz nic) czy na 100% stracić 4 000zł?",
        "A_label": "na 80% stracić 5 000zł (20% szans na stratę 0zł)",
        "B_label": "na 100% stracić 4 000zł",
        "time": 20
    },
    {
        "id": 7,
        "text": "Wolisz na 80% zyskać 5 000zł czy na 100% zyskać 4 000zł?",
        "A_label": "na 80% zyskać 5 000zł",
        "B_label": "na 100% zyskać 4 000zł",
        "time": 15
    },
    {
        "id": 8,
        "text": "Wolisz na 10% zyskać 10 000zł czy na 1% zyskać 100 000zł?",
        "A_label": "na 10% zyskać 10 000zł",
        "B_label": "na 1% zyskać 100 000zł",
        "time": 15
    },
    {
        "id": 9,
        "text": "Wolisz na 50% zyskać 2 000zł czy na 100% zyskać 500zł?",
        "A_label": "na 50% zyskać 2 000zł",
        "B_label": "na 100% zyskać 500zł",
        "time": 15
    },
    {
        "id": 10,
        "text": "Wolisz na 20% zyskać 10 000zł czy na 100% zyskać 2 000zł?",
        "A_label": "na 20% zyskać 10 000zł",
        "B_label": "na 100% zyskać 2 000zł",
        "time": 15
    },
    {
        "id": 11,
        "text": "Wolisz na 90% stracić 3 000zł (istnieje 10% szans, że nie stracisz nic) czy na 45% stracić 6 000zł (55% szans na stratę 0zł)?",
        "A_label": "na 90% stracić 3 000zł (10% szans na stratę 0zł)",
        "B_label": "na 45% stracić 6 000zł (55% szans na stratę 0zł)",
        "time": 20
    },
    {
        "id": 12,
        "text": "Wolisz na 90% zyskać 3 000zł czy na 45% zyskać 6 000zł?",
        "A_label": "na 90% zyskać 3 000zł",
        "B_label": "na 45% zyskać 6 000zł",
        "time": 15
    },
    {
        "id": 13,
        "text": "Wolisz szanse 50/50 na zyskanie lub stracenie 10 000zł czy szanse 50/50 na zyskanie lub stracenie 2 000zł?",
        "A_label": "50/50 zyskać lub stracić 10 000zł",
        "B_label": "50/50 zyskać lub stracić 2 000zł",
        "time": 15
    },

    {
        "id": 14,
        "text": "Czy chcesz skorzystać z opcji 50/50 pomnożenia obecnego kapitału razy 3 albo pomniejszenia go 3 razy (jeśli nie, twój kapitał się nie zmienia)?",
        "A_label": "Tak, chcę skorzystać z opcji",
        "B_label": "Nie chcę skorzystać z opcji",
        "time": 30,
    },
]


# ================= FUNKCJE =================

def save_result(row):
    exists = os.path.isfile(RESULTS_FILE)
    with open(RESULTS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(row)

# ================= FUNKCJE =================


def apply_capital_change(current_capital, q_id, selected_answer):
    preset = {
        1: {"A": 200, "B": 0},
        2: {"A": -250, "B": -200},
        3: {"A": 250, "B": 200},
        4: {"A": 0, "B": -1200},
        5: {"A": 1500, "B": 1200},
        6: {"A": -5000, "B": -4000},
        7: {"A": 5000, "B": 4000},
        8: {"A": 0, "B": 0},
        9: {"A": 2000, "B": 500},
        10: {"A": 0, "B": 2000},
        11: {"A": -3000, "B": -6000},
        12: {"A": 3000, "B": 6000},
        13: {"A": 10000, "B": 2000},
        14: {
            "A": lambda c: c * 3,
            "B": lambda c: c
        },
    }

    effect = preset[q_id][selected_answer]

    if callable(effect):
        return effect(current_capital)
    else:
        return current_capital + effect



# ================= ROUTES =================

@app.route('/', methods=['GET', 'POST'])
def intro():
    if request.method == 'POST':
        # WALIDACJA
        if not all(request.form.get(k) for k in ['age', 'field', 'stress', 'gender', 'savings_2000']):
            return "Wszystkie pola są wymagane", 400

        session.clear()
        session['id'] = str(uuid.uuid4())
        session['age'] = int(request.form['age'])
        session['field'] = request.form['field']
        session['stress'] = int(request.form['stress'])
        session['gender'] = request.form['gender']
        session['savings_2000'] = int(request.form['savings_2000'])
        session['capital'] = 1000
        session['q'] = 0
        session['answers'] = {}
        session['times'] = {}
        session['start_time'] = None

        return redirect('/instructions')

    return render_template_string(INTRO_HTML)

@app.route('/instructions')
def instructions():
    return render_template_string(INSTRUCTIONS_HTML)

@app.route('/question', methods=['GET', 'POST'])
def question():
    q_index = session.get('q', 0)
    if q_index >= len(QUESTIONS):
        return redirect('/end')

    q = QUESTIONS[q_index]

    if request.method == 'POST':
        start = session.get('start_time')
        rt = round(time.time() - start, 3) if start else None

        answer = request.form.get('answer')
        capital = session.get('capital', 1000)

        # brak odpowiedzi / timeout
        if answer is None or answer == 'TIMEOUT':
            capital -= 200
            answer = 'NO_ANSWER'
        else:
          if q.get("type") == "risk_threshold":
        # pytanie deklaratywne → brak zmiany kapitału
            pass
          else:
             capital = apply_capital_change(
                capital,
                q['id'],
                answer
            )


        session['capital'] = round(capital, 2)

        # zapis odpowiedzi i czasu reakcji
        answers = session.get('answers', {})
        times = session.get('times', {})
        answers[f"Q{q['id']}"] = answer
        times[f"RT{q['id']}"] = rt
        session['answers'] = answers
        session['times'] = times
        session['q'] = q_index + 1

        return redirect('/break')

    # GET → ustaw start_time
    session['start_time'] = time.time()
    return render_template_string(QUESTION_HTML, q=q, capital=session['capital'])

@app.route('/break')
def break_screen():
    return render_template_string(
        BREAK_HTML,
        capital=session.get('capital', 0)
    )


@app.route('/end')
def end():
    row = {
        'UUID': session['id'],
        'age': session['age'],
        'field': session['field'],
        'stress': session['stress'],
        'gender': session['gender'],
        'savings_2000': session['savings_2000'],
        'capital_end': session['capital'],
    }

    row.update(session.get('answers', {}))
    row.update(session.get('times', {}))

    final_capital = session['capital']

    save_result(row)
    session.clear()

    return render_template_string(
        END_HTML,
        capital_end=final_capital
)


# ================= HTML =================

INTRO_HTML = """
<h2>Dane wstępne</h2>
<form method='post'>
Wiek: <input type='number' name='age' required><br>
Kierunek: <input name='field' required><br>
Jak w skali 1-6 radzisz sobie ze stresem? (1 = nie radzę, 6 = doskonale):
<select name='stress' required>
<option value=''>--</option>
<option>1</option><option>2</option><option>3</option>
<option>4</option><option>5</option><option>6</option>
</select><br>
Czy jestes obecnie zdolny do samodzielnego pokrycia nagłej straty 1 500zł:<br>
<select name="savings_2000" required>
    <option value="">--</option>
    <option value="1">1 – Zdecydowanie nie</option>
    <option value="2">2 – Raczej nie</option>
    <option value="3">3 – Raczej tak</option>
    <option value="4">4 – Zdecydowanie tak</option>
</select><br><br>

Płeć:
<select name='gender' required>
<option value=''>--</option>
<option>K</option><option>M</option><option>Inna</option>
</select><br><br>
<button type='submit'>Dalej</button>
</form>
"""

INSTRUCTIONS_HTML = """
<p><b>Będziesz odpowiadać na pytania z dwoma wyborami (poza pierwszym pytaniem - ono nie wpływa na twój wynik).</b><br>
<p>Zaczynasz z kapitałem 1000. Brak odpowiedzi = -200.<br>
<p>Masz ograniczony czas na pytanie (wyświetla się licznik). Pomiedzy pytaniami masz 10 sekund przerwy.<p>
<p>Jesli masz opcję 80% stracić ileś, to w domyśle 20% = kapitał się nie zmienia(bedzie doprecyzowane)</p>
<p>cały czas twój kapital jest wyświetlany w prawym dolnym rogu ekranu.</p>
<p>Prowadzony jest ranking a dla osoby z najlepszym kapitałem końcowym przygotowana jest nagroda.</p>
<p>Powodzenia!<br>

<a href='/question'>Start</a>
"""

QUESTION_HTML = """
<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<title>Pytanie {{ q.id }}</title>

<style>
body { font-family: Arial, sans-serif; text-align: center; margin-top: 60px; }
.question { font-size: 34px; font-weight: bold; margin-bottom: 40px; }
.option {
    width: 80%; max-width: 700px; font-size: 32px; padding: 20px;
    margin: 15px auto; display: block; border-radius: 10px; border: 2px solid #333;
    background-color: #f0f0f0; cursor: pointer;
}
.option:hover { background-color: #ddd; }
.capital { position: fixed; bottom: 20px; right: 30px; font-size: 48px; font-weight: bold; }
.timer { position: fixed; top: 20px; right: 30px; font-size: 26px; font-weight: bold; }
</style>

<script>
let timeLeft = {{ q.time }};
function countdown() {
    if (timeLeft <= 0) { document.getElementById("timeout").submit(); }
    document.getElementById("timer").innerText = "Czas: " + timeLeft + " s";
    timeLeft--;
}
setInterval(countdown, 1000);
</script>

</head>
<body>

<div class="timer" id="timer"></div>

<div class="question">{{ q.text }}</div>

<form method="post">
{% if q.options %}
    {% for opt in q.options %}
        <button class="option" name="answer" value="{{ loop.index0 }}">
            {{ opt }}
        </button>
    {% endfor %}
{% else %}
    <button class="option" name="answer" value="A">A) {{ q.A_label }}</button>
    <button class="option" name="answer" value="B">B) {{ q.B_label }}</button>
{% endif %}
</form>


<form id="timeout" method="post">
    <input type="hidden" name="answer" value="TIMEOUT">
</form>

<div class="capital">Kapitał: {{ capital }} zł</div>

</body>
</html>
"""

BREAK_HTML = """
<!doctype html>
<html>
<head>
<style>
.capital {
    position: fixed;
    bottom: 20px;
    right: 30px;
    font-size: 26px;
    font-weight: bold;
}
</style>
</head>

<body>

<h2>Krótka przerwa</h2>
<p>Za chwilę kolejne pytanie…</p>

<div class="capital">Kapitał: {{ capital }} zł</div>

<script>
setTimeout(() => {
    window.location = '/question';
}, 8000);
</script>

</body>
</html>

"""

END_HTML = """
<h2>Dziękujemy za udział w badaniu</h2>
<h3>Twój końcowy kapitał: {{ capital_end }} zł</h3>

"""

# ================= RUN =================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

from flask import Flask, render_template, request, json

from syntax import clause


app = Flask(__name__)


@app.route("/")
def index():
    number = int(request.args.get('number', '20'))
    break_line = (request.args.get('break_line') == "true") or False
    checked = "checked='checked'" if break_line else ''

    clauses = phrases(number)

    return render_template(
        "index.html",
        clauses=clauses,
        number=number,
        break_line=break_line,
        checked=checked,
    )


@app.route("/json")
def index_json():
    number = int(request.args.get('number', '20'))
    return json.dumps(list(phrases(number)))


def phrases(number):
    return (
        (repr(clause()).capitalize() + '.').decode('utf-8')
        for i in xrange(number)
    )


if __name__ == "__main__":
    app.run(debug=True)

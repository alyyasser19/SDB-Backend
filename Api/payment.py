from .routes import app
from flask import request, jsonify


def verify_card(card):
    card_numbers = list(card.strip())

    check_digits = card_numbers.pop()

    card_numbers.reverse()

    processed_digits = []

    for index, digit in enumerate(card_numbers):
        if index % 2 == 0:
            doubled_digit = int(digit) * 2

            if doubled_digit > 9:
                doubled_digit = doubled_digit - 9

            processed_digits.append(doubled_digit)
        else:
            processed_digits.append(int(digit))

    total = int(check_digits) + sum(processed_digits)

    if total % 10 == 0:
        return True
    else:
        return False


def verify_ccv(ccv):
    ccv_string = str(ccv)
    return len(ccv_string) == 3


@app.route('/payment', methods=['POST'])
def payment():
    card = request.form['credit_card']
    ccv = request.form['ccv']
    if verify_card(card) & verify_ccv(ccv):
        return jsonify(
            message="success",
            status=200,
            mimetype='application/json'
        )
    else:
        return jsonify(
            message="incorrect credit card info",
            status=400,
            mimetype='application/json'
        )

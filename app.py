from flask import Flask, request, jsonify
import json
import ast

app = Flask(__name__)

# Load conversions dynamically from JSON
with open('conversions.json') as f:
    conversions = json.load(f)

def dynamic_conversion(value, unit_from, unit_to, conversion_type):
    try:
        # Handle special cases like temperature formulas
        if conversion_type == "temperature":
            formula = conversions[conversion_type].get(f"{unit_from}_to_{unit_to}")
            if formula:
                x = value
                return eval(formula)
            else:
                raise ValueError("Invalid temperature conversion")
        
        # Regular ratio-based conversion
        factor_from = conversions[conversion_type].get(unit_from)
        factor_to = conversions[conversion_type].get(unit_to)
        if factor_from is None or factor_to is None:
            raise ValueError("Invalid unit")
        
        # Perform the conversion
        return value * factor_to / factor_from
    except Exception as e:
        return str(e)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    conversion_type = data['type']
    unit_from = data['unit_from']
    unit_to = data['unit_to']
    value = float(data['value'])

    result = dynamic_conversion(value, unit_from, unit_to, conversion_type)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)

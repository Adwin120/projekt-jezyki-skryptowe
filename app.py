import json
from flask import Flask, redirect, render_template, request, make_response, url_for
from model.arithmetic_parser import evaluate_arithmetic
from model.molecules_parser import evaluate_molecule

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculator')
def calculator():
    return render_template('/calculator/index.html')

@app.route('/calculator/parse', methods=['POST'])
def calculator_parse():
    data = request.data.decode('utf-8')
    try:
        res = make_response(str(evaluate_arithmetic(data)), 200)
    except:
        res = make_response("niewlasciwa skladnia", 400)
    res.mimetype = 'text/plain'
    return res

@app.route('/atomcounter')
def atom_counter():
    
    if 'atoms' in request.args:
        atoms = json.loads(request.args['atoms'].replace("'", '"'))
    else:
        atoms = {}
    if type(atoms) != dict:
        atoms = {"Blad parsera": "zla skladnia"}
    return render_template('/atomcounter/index.html', atoms=atoms)

@app.route('/atomcounter/parse', methods=['POST'])
def atom_parse():
    try:
        atoms = evaluate_molecule(request.form['formula'])
    except:
        atoms = None
    return redirect(url_for('atom_counter', atoms=atoms))

if __name__ == '__main__':
    app.run(debug=True)
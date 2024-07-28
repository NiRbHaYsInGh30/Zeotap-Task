from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from helper import Node, create_ast, evaluate_ast 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
db = SQLAlchemy(app)

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_string = db.Column(db.String, nullable=False)
    ast_json = db.Column(db.String, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json['rule_string']
    ast = create_ast(rule_string)
    ast_json = json.dumps(ast, default=lambda o: o.__dict__)
    new_rule = Rule(rule_string=rule_string, ast_json=ast_json)
    db.session.add(new_rule)
    db.session.commit()
    return jsonify({"id": new_rule.id, "rule_string": rule_string, "ast_json": ast_json})

@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    rule_ids = request.json['rule_ids']
    rules = Rule.query.filter(Rule.id.in_(rule_ids)).all()
    combined_ast = None
    for rule in rules:
        ast = json.loads(rule.ast_json, object_hook=lambda d: Node(**d))
        if combined_ast is None:
            combined_ast = ast
        else:
            combined_ast = Node(type='operator', left=combined_ast, right=ast, value='and')
    combined_ast_json = json.dumps(combined_ast, default=lambda o: o.__dict__)
    return jsonify({"combined_ast_json": combined_ast_json})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    ast_json = request.json['ast_json']
    data = request.json['data']
    ast = json.loads(ast_json, object_hook=lambda d: Node(**d))
    result = evaluate_ast(ast, data)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)

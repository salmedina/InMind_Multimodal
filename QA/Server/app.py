import argparse
import json
import solr
from flask import Flask, render_template
from flask import request
from simplejson import loads


# ===================================================================
# QA nlp / processing
# ===================================================================
def get_question_type(question_str):
    if question_str is None:
        return ''
    if len(question_str) < 1:
        return ''

    return question_str.split(' ')[0]  # return first word


# ===================================================================
# Service auxiliaries
# ===================================================================
def validate_ask_request(req):
    '''
    @in_request: it is the request in JSON format
    '''
    # Normalize request keys to lowercase


    for key in req.keys():
        req[key.lower()] = req.pop(key)
    keys = req.keys()
    print keys

    return ('question' in keys and 'user' in keys)


def build_error_answer(message):
    res = {}
    res['type'] = 'error'
    res['message'] = message

    return json.dumps(res)


def build_answer(question_str, question_type, answer_str, answers):
    '''
    @question_str: 
    @question_type: 
    @answer_str: answer string with highest probability
    @answers: top list of answers
    '''
    res = {}
    res['answer_summary'] = answer_str
    res['answers'] = answers
    res['question_type'] = question_type
    res['user_question'] = question_str

    return json.dumps(res)


# ===================================================================
# FLASK APP
# ===================================================================
app = Flask(__name__)


@app.route("/ask", methods=['POST', 'GET'])
def answer():
    req = request.get_json(force=True)['data']

    if not validate_ask_request(req):
        return build_error_answer('Invalid request')

    # Extract the question and its type
    q = req['question']
    user = req['user']

    q_type = get_question_type(q)
    # Get the answer

    # Return the answer
    return build_answer(q, q_type, 'who knows', [])


if __name__ == '__main__':
    # Load the arguments of the program
    # Host and port where the service will be running
    parser = argparse.ArgumentParser(description='Text summarizer server')
    parser.add_argument('-ip', '--ip', help='Host where the service will be running', required=False, default='0.0.0.0')
    parser.add_argument('-p', '--port', help='Port where the service will be running', required=False, default=15000)
    args = vars(parser.parse_args())

    app.debug = True
    app.run(host=args['ip'], port=int(args['port']))

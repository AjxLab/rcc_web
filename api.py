# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request
from engine import BotEngine
from nltk.tokenize import sent_tokenize

ai = BotEngine('./model/English.model')
api = Flask(__name__)


@api.route('/', methods=['POST'])
def get_query():
    ## -----*----- 推論結果を返す -----*----- ##
    text = request.form['text']
    question = request.form['question']
    choices = request.form.getlist('choices')
    scores = []

    # 最大類似文を抽出
    for sentence in sent_tokenize(text):
        scores.append({'sentence': '', 'score': 0})
        scores[-1]['sentence'] = sentence
        scores[-1]['score'] = ai.sentence_similarity(sentence, question)

    # 類似度の高い順にソート
    for i in range(len(scores)):
        for j in range(len(scores) - 1, i, -1):
            if scores[j]['score'] > scores[j - 1]['score']:
                tmp = scores[j]
                scores[j] = scores[j - 1]
                scores[j - 1] = tmp
    scores = scores[0:100]

    with open('./tmp/result.txt', mode='w') as f:
        for i in range(len(scores)):
            f.write('{0}_similar\n'.format(i + 1))
            f.write('  - Sentence：' + scores[i]['sentence'] + '\n')
            f.write('  - Similar ：' + str(scores[i]['score']) + '\n')
            max_choice = {'choice': '', 'score': 0}
            for choice in choices:
                score = ai.sentence_similarity(choice, scores[i]['sentence'])
                if max_choice['score'] <= score:
                    max_choice['choice'] = choice
                    max_choice['score'] = score
            f.write('  - Choice  ：' + max_choice['choice'] + '\n')

    # 最も適当な選択肢を返す
    max_choice = {'choice': '', 'score': 0.0}
    for choice in choices:
        score = ai.sentence_similarity(choice, scores[0]['sentence'])
        if max_choice['score'] < score:
            max_choice['choice'] = choice
            max_choice['score'] = score

    result = {'sentence': scores[0], 'result': max_choice['choice']}
    return make_response(jsonify(result))


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3000)

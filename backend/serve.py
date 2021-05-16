from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
import string
import collections
import re
from nltk.corpus import stopwords
import nltk

import os
from typing import Tuple, List
from functools import partial

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils.rnn import pad_sequence

from transformers import ( 
    AutoModelWithLMHead, 
    AutoTokenizer,
    BertTokenizer, 
    BertModel, 
    AdamW, 
    get_linear_schedule_with_warmup, 
    BertPreTrainedModel, 
    BertForMaskedLM
)

from model import BertClassifier
from gensim.models.word2vec import Word2Vec
import gensim.downloader as api
from utils import *

vectors = api.load("glove-twitter-25")
bert_model_name = 'bert-base-cased'
device = torch.device('cpu')
if torch.cuda.is_available(): device = torch.device('cuda:0')

tokenizer = BertTokenizer.from_pretrained(bert_model_name)
model = BertClassifier(BertModel.from_pretrained(
    bert_model_name, output_attentions=True), 6).to(device)
model.load_state_dict(torch.load("finetuned_pytorch_model.bin"))

tokenizer_LM = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model_LM = AutoModelWithLMHead.from_pretrained("distilbert-base-uncased")
model_LM.to('cuda')
model_LM.eval()

app = Flask(__name__)
CORS(app)

history = {}
token_types = {}
overall_memo = {}
text_memo = {}
final_submissions = {}

@app.route("/set_token_type", methods=['POST'])
def set_token_type():
    token_types[request.json["uuid"]] = request.json["type"]
    return jsonify({"saved": True})

@app.route("/token_type", methods=['GET'])
def get_token_type():
    return jsonify(token_types)

@app.route("/submit", methods=['POST'])
def add_user_submission():
    if request.json["uuid"] not in final_submissions:
        final_submissions[request.json["uuid"]] = []

    final_submissions[request.json["uuid"]].append(request.json["submission"])
    
    return jsonify({"saved": True})

@app.route("/submit", methods=['GET'])
def get_user_submission():
    return jsonify(final_submissions)

@app.route("/toxicity", methods=['POST'])
def selected_toxicity():

    if "uuid" not in request.json:
        return None

    # store request
    if request.json["uuid"] not in history:
        history[request.json["uuid"]] = {
            "requests": [],
            "responses": []
        }

    history[request.json["uuid"]]["requests"].append(request.json)

    selected_alts = collections.OrderedDict(sorted(request.json["alternatives"].items()))
    swap_idxs = list(selected_alts.keys())

    if len(swap_idxs) > 0:
        # trim the alternatives
        all_alts = [selected_alts[key][:3] for key in selected_alts]
        possible_complete_alts = cartesian_product_simple_transpose(np.array(all_alts))
        split_words = request.json['text'].split(" ")
        options = []
        raw_options = []
        tokens = torch.LongTensor(tokenizer.encode(" ".join(split_words), add_special_tokens=True)).to(device)
        options.append(tokens)

        for candidate in possible_complete_alts:
            for idx, word in enumerate(candidate):
                split_words[int(swap_idxs[idx])] = word

            raw_options.append(" ".join(split_words))
            tokens = torch.LongTensor(tokenizer.encode(" ".join(split_words), add_special_tokens=True)).to(device)
            options.append(tokens)

        x = pad_sequence(options, batch_first=True,
                         padding_value=tokenizer.pad_token_id).to(device)
        mask = (x != tokenizer.pad_token_id).float().to(device)
        with torch.no_grad():
            _, outputs, attns, last_layer = model(x, attention_mask=mask)

        model_outs = outputs[:, 0].squeeze().tolist()
        original_toxicity = model_outs[:1]
        candidate_replacements = model_outs[1:]
        sorted_candidates = np.argsort(candidate_replacements)

        updated_toxicity_replacements = []
        original_toxicity = model_outs[:1]
        for i in sorted_candidates[:5]:
            updated_toxicity_replacements.append(
                [candidate_replacements[i], list(possible_complete_alts[i])])

        return_obj = {
            "originalToxicity": original_toxicity,
            "alternatives": updated_toxicity_replacements
        }

        history[request.json["uuid"]]["responses"].append(return_obj)
        return jsonify(return_obj)

    sigmoid_outputs, orig_attentions, orig_tokens = get_probs_and_attention(request.json['text'], model, tokenizer)
    return jsonify({
        "originalToxicity": [sigmoid_outputs[0]["value"]],
        "alternatives": []
    })


@app.route("/history", methods=['GET'])
def get_history():
    return jsonify(history)

@app.route("/", methods=['POST'])
def get_toxic_labels():

    if "uuid" not in request.json:
        return None

    # store request
    if request.json["uuid"] not in history:
        history[request.json["uuid"]] = {
            "requests": [],
            "responses": []
        }

    history[request.json["uuid"]]["requests"].append(request.json)

    if request.json['text'] in overall_memo:
        history[request.json["uuid"]]["responses"].append(
            overall_memo[request.json['text']])
        return jsonify(overall_memo[request.json['text']])

    sigmoid_outputs, orig_attentions, orig_tokens = get_probs_and_attention(
        request.json['text'], model, tokenizer)

    def generate_alternatives(index, tokens, original_score, orig_attentions):
        selection_regexed = re.findall(r"[\w']+|[.,!?;]", tokens[index])
        selection = [selection_regexed[0].lower()] + ["".join(selection_regexed[1:])]
        if (selection[0] not in vectors.vocab):
            return None
        
        similar_vectors = get_synonyms(selection[0].lower())
        similar_lm_words = predict_masked_tokens(tokens.copy(), index, tokenizer_LM, model_LM)

        if similar_vectors == None:
            similar_vectors = {elem[0]: elem[1] for elem in vectors.most_similar(selection[0].lower(), topn=10)}

        potential_options = {}
        for k in similar_vectors:
            potential_options[k] = similar_vectors[k]

        for k in similar_lm_words:
            stripped = re.sub(r'\W+', '', k)
            if '#' in stripped or len(stripped) == 0 or stripped.lower() in set(stopwords.words('english')): 
                continue
            
            if k in potential_options:
                potential_options[k] += potential_options[k] + similar_lm_words[k]
            else: potential_options[k] = similar_lm_words[k]
            
        sorted_options = {k: v for k, v in sorted(potential_options.items(), key=lambda item: item[1])}
        
        local_options = []
        for word in list(sorted_options.keys())[:20] + [""]:
            if '#' in word: continue
            old = tokens[index]            
            tokens[index] = word
            
            alt_sigmoid_outputs, alt_attentions, alt_tokens = get_probs_and_attention(" ".join(tokens), model, tokenizer)

            old_word_sigmoid_out, _, _ = get_probs_and_attention(old, model, tokenizer)
            old_word_score = old_word_sigmoid_out[0]["value"]
            word_sigmoid_out, _, _ = get_probs_and_attention(word, model, tokenizer)
            word_score = word_sigmoid_out[0]["value"]
            if word_score < .4 and old_word_score >= .4:
                local_options.append(
                    [word + selection[1], word_score, alt_attentions])

            tokens[index] = old

        if len(local_options) == 0:
            return None
        return sorted(local_options, key=lambda x: x[1], reverse=False)

    options = {}
    orig_tokens_copy = orig_tokens.copy()

    if sigmoid_outputs[0]["value"] > .25:
        for idx, attention in enumerate(orig_attentions):
            if orig_tokens[idx].lower() in set(stopwords.words('english')):
                continue
            if attention > .25:
                alternatives = generate_alternatives(
                    idx, orig_tokens_copy, sigmoid_outputs[0]["value"], orig_attentions)
                if alternatives is not None:
                    options[idx] = alternatives

    response = {
        "mainInputResults": {
            "attentionOutput": orig_attentions,
            "sigmoidOutput": sigmoid_outputs
        },
        "alternatives": options,
    }

    overall_memo[request.json['text']] = response
    history[request.json["uuid"]]["responses"].append(response)

    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000')

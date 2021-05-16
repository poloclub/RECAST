from torch.nn.utils.rnn import pad_sequence
import torch
import itertools
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet

device = torch.device('cpu')
if torch.cuda.is_available(): device = torch.device('cuda:0')

text_memo = {}
mask_cache = {}
synonym_cache = {}

label_list = ['toxic', 'severe_toxic', 'obscene',
              'threat', 'insult', 'identity_hate']

# gets a list of synonyms from WordNet
def get_synonyms(word):
    if word in synonym_cache:
        return synonym_cache[word]

    synonyms = []
    for syn in wordnet.synsets(word)[:2]: # only look at first two sysnets.
        for l in syn.lemma_names():
            if '_' not in l: synonyms.append(l)
     
    if len(synonyms) == 0:
        return None
    
    similar_vectors = {}
    for k in synonyms:
        if k.lower() == word:
            continue
        similar_vectors[k] = 0
        
    synonym_cache[word] = similar_vectors
    return similar_vectors

# predicts a missing word using [mask] token
# masks out selected toxic work (where selected word = select_idx)
def predict_masked_tokens(masked_text, select_idx, tokenizer_LM, model_LM, topn=20):
    masked_text[select_idx] = tokenizer_LM.mask_token
    sequence = " ".join(masked_text) + "."
    if sequence in mask_cache:
        return mask_cache[sequence]

    input = tokenizer_LM.encode(sequence, return_tensors="pt").cuda()
    mask_token_index = torch.where(input == tokenizer_LM.mask_token_id)[1]
    token_logits = model_LM(input)[0]
    mask_token_logits = token_logits[0, mask_token_index, :]

    top_k_token_sets = torch.topk(mask_token_logits, topn, dim=1).indices.squeeze().tolist()
    top_k_token_values = torch.softmax(torch.topk(mask_token_logits, topn, dim=1).values.squeeze(), dim=0).tolist()
    sample_tokens = {}
    for idx, token in enumerate(top_k_token_sets):
        sample_tokens[(tokenizer_LM.decode([token]))] = top_k_token_values[idx]
    mask_cache[sequence] = sample_tokens
    return sample_tokens

def cartesian_product_simple_transpose(arrays):
    return [elem for elem in itertools.product(*arrays)]

def doc_tokenizer(paragraph_text):
    return paragraph_text.split()

# maps tokenized to original text.
def get_tok_to_orig_index(doc_tokens, tokenizer):
    tok_to_orig_index = []
    for (i, token) in enumerate(doc_tokens):
        sub_tokens = tokenizer.tokenize(token)
        for sub_token in sub_tokens:
            tok_to_orig_index.append(i)

    return tok_to_orig_index

# selects attention scores from heads in last layer    
def attention_reducer(attn, orig_len, input_text, tokenizer):
    r = torch.sum(attn[-1][0], axis=0)[0][1:-1]
    reduced_attn = []
    if len(r) > 0:
        reduced_attn = (r-min(r))/(max(r)-min(r))
        reduced_attn = reduced_attn.tolist()

    original_tokens = doc_tokenizer(input_text)
    original_attentions = [0] * len(original_tokens)

    tok_to_orig_index = get_tok_to_orig_index(
        doc_tokenizer(input_text), tokenizer)

    for index, attn_score in enumerate(reduced_attn):
        if original_attentions[tok_to_orig_index[index]] < attn_score:
            original_attentions[tok_to_orig_index[index]] = attn_score

    return original_attentions, original_tokens

def get_probs_and_attention(text, model, tokenizer):
    if text in text_memo:
        return text_memo[text]
    tokens = tokenizer.encode(text, add_special_tokens=True)
    if len(tokens) > 120:
        tokens = tokens[:119] + [tokenizer.sep_token_id]
    texts = torch.LongTensor(tokens).unsqueeze(0).to(device)
    x = pad_sequence(texts, batch_first=True,
                     padding_value=tokenizer.pad_token_id).to(device)
    mask = (x != tokenizer.pad_token_id).float().to(device)
    with torch.no_grad():
        _, outputs, attns, last_layer = model(x, attention_mask=mask)
    probs = outputs[0].tolist()
    sigmoid_outputs = []
    for label_idx, label in enumerate(label_list):
        sigmoid_outputs.append({
            "label": label,
            "value": probs[label_idx]
        })

    orig_attentions, orig_tokens = attention_reducer(attns, len(tokens), text, tokenizer)
    text_memo[text] = sigmoid_outputs, orig_attentions, orig_tokens
    return text_memo[text]


from tqdm import tqdm
import requests
import zipfile
import torch
import torch.nn as nn
import numpy as np
from .doc import *
from .tbinfo import *

SPACE_RE = re.compile(r'\s')


def unzip(dir, filename):
    with zipfile.ZipFile(os.path.join(dir, filename)) as f:
        f.extractall(dir)
    os.remove(os.path.join(dir, filename))


def download(cache_dir, language):
    lang_dir = os.path.join(cache_dir, language)
    save_fpath = os.path.join(cache_dir, language, '{}.zip'.format(language))

    if not os.path.exists(os.path.join(lang_dir, '{}.downloaded'.format(language))):
        # print('Downloading saved models for {} ...'.format(language))
        url = "http://nlp.uoregon.edu:8000/download/merino/{}.zip".format(language)

        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc='Downloading: ')

        ensure_dir(lang_dir)
        with open(save_fpath, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        unzip(lang_dir, '{}.zip'.format(language))
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("Failed to download saved models for {}!".format(language))
        else:
            with open(os.path.join(lang_dir, '{}.downloaded'.format(language)), 'w') as f:
                f.write('')


def parse_report(report_fpath):
    with open(report_fpath) as f:
        lines = [line.strip() for line in f if line.strip()][2:]
    score = {
        'tokens': 0,
        'sentences': 0,
        'words': 0,
        'upos': 0,
        'xpos': 0,
        'ufeats': 0,
        'alltags': 0,
        'lemmas': 0,
        'uas': 0,
        'las': 0,
        'clas': 0,
        'mlas': 0,
        'blex': 0
    }
    if not lines[0].startswith('Tokens'):
        score['average'] = 0
        return score
    else:
        score['tokens'] = float(lines[0].split('|')[-2].strip())
        score['sentences'] = float(lines[1].split('|')[-2].strip())
        score['words'] = float(lines[2].split('|')[-2].strip())
        score['upos'] = float(lines[3].split('|')[-2].strip())
        score['xpos'] = float(lines[4].split('|')[-2].strip())
        score['ufeats'] = float(lines[5].split('|')[-2].strip())
        score['alltags'] = float(lines[6].split('|')[-2].strip())
        score['lemmas'] = float(lines[7].split('|')[-2].strip())
        score['uas'] = float(lines[8].split('|')[-2].strip())
        score['las'] = float(lines[9].split('|')[-2].strip())
        score['clas'] = float(lines[10].split('|')[-2].strip())
        score['mlas'] = float(lines[11].split('|')[-2].strip())
        score['blex'] = float(lines[12].split('|')[-2].strip())

        score['average'] = np.mean(list(score.values()))
        return score


def process_doc(conllu_doc):
    out_doc = []
    num_sents = len(conllu_doc)
    for sent_id in range(num_sents):
        sent = conllu_doc[sent_id]
        out_sent = []

        start2mwt = {}
        for mwt in sent['mwts']:
            start2mwt[mwt['start']] = mwt

        num_words = len(sent.keys()) - 1
        for word_id in range(1, num_words + 1):
            word = sent[word_id]
            assert word['id'] == word_id
            if word_id in start2mwt:
                mwt = start2mwt[word_id]
                out_sent.append({ID: '{}-{}'.format(mwt['start'], mwt['end']), TEXT: mwt['text']})

            out_sent.append({ID: f'{word_id}', TEXT: word[TEXT],
                             UPOS: word.get(UPOS, '_'), XPOS: word.get(XPOS, '_'), FEATS: word.get(FEATS, '_'),
                             HEAD: word.get(HEAD, f'{word_id - 1}'), DEPREL: word.get(DEPREL, '_')})
        out_doc.append(out_sent)
    return out_doc


def process_sentence(sentence):
    sent = []
    i = 0
    for tok, wp_p, additional_info in sentence:
        if len(tok) <= 0:
            continue
        if wp_p == 3 or wp_p == 4:
            additional_info['MWT'] = 'Yes'
        infostr = None if len(additional_info) == 0 else '|'.join(
            [f"{k}={additional_info[k]}" for k in additional_info])
        sent.append({ID: f'{i + 1}', TEXT: tok})
        if infostr is not None: sent[-1][MISC] = infostr
        i += 1
    return sent


def ensure_dir(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def printlog(logger, message, printout=True):
    logger.info(message)
    if printout:
        print(message)


def word_lens_to_idxs_fast(token_lens):
    max_token_num = max([len(x) for x in token_lens])
    max_token_len = max([max(x) for x in token_lens])
    idxs, masks = [], []
    for seq_token_lens in token_lens:
        seq_idxs, seq_masks = [], []
        offset = 0
        for token_len in seq_token_lens:
            seq_idxs.extend([i + offset for i in range(token_len)]
                            + [-1] * (max_token_len - token_len))
            seq_masks.extend([1.0 / token_len] * token_len
                             + [0.0] * (max_token_len - token_len))
            offset += token_len
        seq_idxs.extend([-1] * max_token_len * (max_token_num - len(seq_token_lens)))
        seq_masks.extend([0.0] * max_token_len * (max_token_num - len(seq_token_lens)))
        idxs.append(seq_idxs)
        masks.append(seq_masks)
    return idxs, masks, max_token_num, max_token_len


def compute_word_reps_avg(piece_reprs, component_idxs):
    batch_word_reprs = []
    batch_size, _, _ = piece_reprs.shape
    _, num_words, _ = component_idxs.shape
    for bid in range(batch_size):
        word_reprs = []
        for wid in range(num_words):
            wrep = torch.mean(piece_reprs[bid][component_idxs[bid][wid][0]: component_idxs[bid][wid][1]], dim=0)
            word_reprs.append(wrep)
        word_reprs = torch.stack(word_reprs, dim=0)  # [num words, rep dim]
        batch_word_reprs.append(word_reprs)
    batch_word_reprs = torch.stack(batch_word_reprs, dim=0)  # [batch size, num words, rep dim]
    return batch_word_reprs


def normalize_token(treebank_name, token):  # adapted from stanza
    token = SPACE_RE.sub(' ', token.lstrip())

    if 'chinese' in treebank_name.lower() or 'korean' in treebank_name.lower() or 'japanese' in treebank_name.lower():
        token = token.replace(' ', '')

    return token


def word_lens_to_idxs(word_lens):
    max_token_num = max([len(x) for x in word_lens])
    max_token_len = max([max(x) for x in word_lens])
    idxs = []
    for seq_token_lens in word_lens:
        seq_idxs = []
        offset = 0
        for token_len in seq_token_lens:
            seq_idxs.append([offset, offset + token_len])
            offset += token_len
        seq_idxs.extend([[-1, 0]] * (max_token_num - len(seq_token_lens)))
        idxs.append(seq_idxs)
    return idxs, max_token_num, max_token_len


class Linears(nn.Module):
    def __init__(self, dimensions, activation='relu', dropout_prob=0.0, bias=True):
        super().__init__()
        assert len(dimensions) > 1
        self.layers = nn.ModuleList([nn.Linear(dimensions[i], dimensions[i + 1], bias=bias)
                                     for i in range(len(dimensions) - 1)])
        self.activation = getattr(torch, activation)
        self.dropout = nn.Dropout(dropout_prob)

    def forward(self, inputs):
        for i, layer in enumerate(self.layers):
            if i > 0:
                inputs = self.activation(inputs)
                inputs = self.dropout(inputs)
            inputs = layer(inputs)
        return inputs

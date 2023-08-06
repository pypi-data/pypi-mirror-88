import os
import re
import json
import sys
from torch.utils.data import DataLoader
import tqdm
from .base_utils import *
from copy import deepcopy

NEWLINE_WHITESPACE_RE = re.compile(r'\n\s*\n')
NUMERIC_RE = re.compile(r'^([\d]+[,\.]*)+$')
WHITESPACE_RE = re.compile(r'\s')
PARAGRAPH_BREAK = re.compile(r'\n\s*\n')
MWT_SPLIT = '<mwt-split>'

PUNCTUATION = re.compile(
    r'''["’'\(\)\[\]\{\}<>:\,‒–—―…!\.«»\-‐\?‘’“”;/⁄␠·&@\*\\•\^¤¢\$€£¥₩₪†‡°¡¿¬\#№%‰‱¶′§~¨_\|¦⁂☞∴‽※"]''')


def pseudo_tokenize(sent_text):
    tokens_by_space = sent_text.split()
    pseudo_tokens = []
    for token in tokens_by_space:
        if len(PUNCTUATION.findall(token)) > 0:
            tmp = ''
            for char in token:
                if PUNCTUATION.match(char):
                    if tmp != '':
                        pseudo_tokens.append(tmp)
                        tmp = ''
                    pseudo_tokens.append(char)
                else:
                    tmp += char
            if tmp != '':
                pseudo_tokens.append(tmp)
        else:
            pseudo_tokens.append(token)

    assert len(''.join(sent_text.split())) == len(''.join(pseudo_tokens))
    return pseudo_tokens


def get_startchar_idx(word, text):
    start_char_idx = 0
    for k in range(len(text)):
        if len(text[k].strip()) > 0:
            start_char_idx = k
            break
    text = text[start_char_idx + len(word):]
    return text, start_char_idx


def get_character_locations(string_units, text):
    tmp_text = deepcopy(text)
    offset = 0
    end_positions = []
    for str_unit in string_units:
        tmp_text, start_position = get_startchar_idx(str_unit, tmp_text)
        start_position += offset
        end_position = start_position + len(str_unit) - 1
        end_positions.append(end_position)
        offset = start_position + len(str_unit)
    return end_positions


def get_mapping_wp_character_to_or_character(wordpiece_splitter, wp_single_string, or_single_string):
    wp_char_to_or_char = {}
    converted_text = ''
    for char_id, char in enumerate(or_single_string):
        converted_chars = ''.join(
            [c if not c.startswith('▁') else c[1:] for c in wordpiece_splitter.tokenize(char) if c != '▁'])

        for converted_c in converted_chars:
            c_id = len(converted_text)
            wp_char_to_or_char[c_id] = char_id
            converted_text += converted_c
    assert wp_single_string == converted_text
    return wp_char_to_or_char


def wordpiece_tokenize_from_raw_text(wordpiece_splitter, sent_text, sent_labels, sent_position_in_paragraph,
                                     treebank_name):
    if 'Chinese' in treebank_name or 'Japanese' in treebank_name:
        pseudo_tokens = [c for c in sent_text]  # characters as pseudo tokens
    else:
        if treebank_name == 'UD_Urdu-UDTB':
            sent_text = sent_text.replace('۔', '.')
        elif treebank_name == 'UD_Uyghur-UDT':
            sent_text = sent_text.replace('-', '،')
        pseudo_tokens = pseudo_tokenize(sent_text)
    end_pids = set()
    group_pieces = [wordpiece_splitter.tokenize(t) for t in
                    pseudo_tokens]  # texts could be considered as a list of pseudo tokens
    flat_wordpieces = []
    for group in group_pieces:
        if len(group) > 0:
            for p in group:
                if p != '▁':
                    pid = len(flat_wordpieces)
                    flat_wordpieces.append((p, pid))
            end_pids.add(len(flat_wordpieces) - 1)

    single_original_string = ''.join([c.strip() for c in sent_text])

    original_characters = [c for c in single_original_string]
    character_locations = get_character_locations(original_characters, sent_text)

    single_wordpiece_string = ''.join([p if not p.startswith('▁') else p.lstrip('▁') for p, pid in flat_wordpieces])

    wp_character_2_or_character = get_mapping_wp_character_to_or_character(wordpiece_splitter, single_wordpiece_string,
                                                                           single_original_string)

    flat_wordpiece_labels = []
    flat_wordpiece_ends = []
    offset = 0
    for wordpiece, _ in flat_wordpieces:
        if wordpiece.startswith('▁'):
            str_form = wordpiece[1:]
        else:
            str_form = wordpiece
        end_char = offset + len(str_form) - 1
        ori_char = wp_character_2_or_character[end_char]
        location_in_sentence = character_locations[ori_char]
        wp_label = int(sent_labels[location_in_sentence])
        wp_end = sent_position_in_paragraph + location_in_sentence
        flat_wordpiece_labels.append(wp_label)
        flat_wordpiece_ends.append(wp_end)

        offset = end_char + 1

    return flat_wordpieces, flat_wordpiece_labels, flat_wordpiece_ends, end_pids


def split_to_sentences(paragraph_text, charlabels, mwtlabels, treebank_name):
    sent_text = ''
    sent_labels = ''
    sent_mwt_labels = []
    sentences = []
    start = 0
    mwt_id = 0
    for k in range(len(charlabels)):
        sent_text += paragraph_text[k]
        sent_labels += charlabels[k]
        if charlabels[k] == '3' or charlabels[k] == '4':
            sent_mwt_labels.append(mwtlabels[mwt_id])
            mwt_id += 1
        if charlabels[k] == '2' or charlabels[k] == '4':
            end = k  # (start, end) local position in REFURBISHED paragraph (REFURBISHED means the \newline characters are removed from a paragraph text
            sentences.append((deepcopy(sent_text), deepcopy(sent_labels), deepcopy(sent_mwt_labels), start, end))
            start = end + 1
            sent_text = ''
            sent_labels = ''
            sent_mwt_labels = []

    if len(sentences) > 0:  # case: train data
        # a paragraph not always ends with a 2 or 4 label
        if not (len(sent_text) == 0 and len(sent_labels) == 0 and len(
                sent_mwt_labels) == 0):
            sentences.append(
                (deepcopy(sent_text), deepcopy(sent_labels), deepcopy(sent_mwt_labels), start, len(paragraph_text) - 1))
    else:
        sentences = [(paragraph_text, charlabels, mwtlabels, 0, len(paragraph_text) - 1)]
    return sentences


def split_to_subsequences(wordpieces, wordpiece_labels, sent_mwt_labels, wordpiece_ends, end_piece_ids,
                          max_input_length):
    subsequences = []
    subseq = [[], [], [], []]
    sub_mwt_labels = []
    mwt_id = 0
    for wp_wpid, wl, we in zip(wordpieces, wordpiece_labels, wordpiece_ends):
        wp, wpid = wp_wpid
        subseq[0].append((wp, wpid))
        subseq[1].append(wl)
        if wl == 3 or wl == 4:
            sub_mwt_labels.append(sent_mwt_labels[mwt_id])
            mwt_id += 1
        subseq[3].append(we)
        if wpid in end_piece_ids and len(subseq[0]) >= max_input_length - 10:
            subsequences.append((subseq[0], subseq[1], sub_mwt_labels, subseq[3], end_piece_ids))

            subseq = [[], [], [], []]
            sub_mwt_labels = []

    if len(subseq[0]) > 0:
        subsequences.append((subseq[0], subseq[1], sub_mwt_labels, subseq[3], end_piece_ids))
    return subsequences


def charlevel_format_to_wordpiece_format(wordpiece_splitter, max_input_length, plaintext, treebank_name):
    corpus_labels = '\n\n'.join(['0' * len(pt.rstrip()) for pt in NEWLINE_WHITESPACE_RE.split(plaintext)])
    corpus_mwt_labels = [[] for pt in NEWLINE_WHITESPACE_RE.split(plaintext)]

    data = [{'text': pt.rstrip(), 'charlabels': pc, 'mwtlabels': pmwt} for pt, pc, pmwt in
            zip(NEWLINE_WHITESPACE_RE.split(plaintext), NEWLINE_WHITESPACE_RE.split(corpus_labels),
                corpus_mwt_labels) if
            len(pt.rstrip()) > 0]

    wordpiece_examples = []
    kept_tokens = 0
    total_tokens = 0
    for paragraph_index, paragraph in enumerate(data):
        paragraph_text = paragraph['text']
        paragraph_labels = paragraph['charlabels']
        paragraph_mwt_labels = paragraph['mwtlabels']
        # split to sentences
        sentences = split_to_sentences(paragraph_text, paragraph_labels, paragraph_mwt_labels, treebank_name)
        tmp_examples = []
        for sent in sentences:
            sent_text, sent_labels, sent_mwt_labels, sent_start, sent_end = sent
            wordpieces, wordpiece_labels, wordpiece_ends, end_piece_ids = wordpiece_tokenize_from_raw_text(
                wordpiece_splitter, sent_text,
                sent_labels, sent_start,
                treebank_name)
            kept_tokens += len([x for x in wordpiece_labels if x != 0])
            total_tokens += len([x for x in sent_labels if x != '0'])
            if len(wordpieces) <= max_input_length - 2:  # minus 2: reserved for <s> and </s>
                tmp_examples.append((wordpieces, wordpiece_labels, sent_mwt_labels, wordpiece_ends, end_piece_ids))
            else:
                subsequences = split_to_subsequences(wordpieces, wordpiece_labels, sent_mwt_labels, wordpiece_ends,
                                                     end_piece_ids,
                                                     max_input_length)
                for subseq in subsequences:
                    tmp_examples.append(subseq)
        # merge consecutive sentences/subsequences
        new_example = [[], [], [], []]
        for example in tmp_examples:
            if len(new_example[0]) + len(example[0]) > max_input_length - 2:
                num_extra_wordpieces = min(max_input_length - 2 - len(new_example[0]), len(example[0]))
                end_piece_ids = example[-1]
                takeout_position = 0
                for tmp_id in range(num_extra_wordpieces):
                    wp, wpid = example[0][tmp_id]
                    if wpid in end_piece_ids:
                        takeout_position = tmp_id + 1
                num_extra_wordpieces = takeout_position
                new_example[0] += deepcopy(example[0][: num_extra_wordpieces])
                new_example[1] += deepcopy(example[1][: num_extra_wordpieces])

                extra_mwt_labels = []
                mwt_id = 0
                for pid in range(num_extra_wordpieces):
                    if example[1][pid] == 3 or example[1][pid] == 4:
                        extra_mwt_labels.append(deepcopy(example[2][mwt_id]))
                        mwt_id += 1
                new_example[2] += extra_mwt_labels

                new_example[3] += deepcopy(example[3][: num_extra_wordpieces])
                wordpiece_examples.append(
                    ([wp for wp, wpid in new_example[0]], new_example[1], new_example[2], new_example[3],
                     paragraph_index))
                # start new example
                new_example = [[], [], [], []]

            new_example[0] += deepcopy(example[0])
            new_example[1] += deepcopy(example[1])
            new_example[2] += deepcopy(example[2])
            new_example[3] += deepcopy(example[3])
        if len(new_example[0]) > 0:
            wordpiece_examples.append(
                ([wp for wp, wpid in new_example[0]], new_example[1], new_example[2], new_example[3], paragraph_index))

    final_examples = []
    for wp_example in wordpiece_examples:
        wordpieces, wordpiece_labels, seq_mwt_labels, wordpiece_ends, paragraph_index = wp_example
        final_examples.append({
            'wordpieces': wordpieces,
            'wordpiece_labels': wordpiece_labels,
            'mwt_labels': seq_mwt_labels,
            'wordpiece_ends': wordpiece_ends,
            'paragraph_index': paragraph_index
        })

    return final_examples


def charlevel_format_to_wordpiece_offline(tokenizer, max_input_length, plaintext_file,
                                          wordpiece_labels_output_fpath, treebank_name):
    with open(plaintext_file, 'r') as f:
        corpus_text = ''.join(f.readlines())

    corpus_labels = '\n\n'.join(['0' * len(pt.rstrip()) for pt in NEWLINE_WHITESPACE_RE.split(corpus_text)])
    corpus_mwt_labels = [[] for pt in NEWLINE_WHITESPACE_RE.split(corpus_text)]

    data = [{'text': pt.rstrip(), 'charlabels': pc, 'mwtlabels': pmwt} for pt, pc, pmwt in
            zip(NEWLINE_WHITESPACE_RE.split(corpus_text), NEWLINE_WHITESPACE_RE.split(corpus_labels),
                corpus_mwt_labels) if
            len(pt.rstrip()) > 0]

    wordpiece_examples = []
    kept_tokens = 0
    total_tokens = 0
    for paragraph_index, paragraph in enumerate(data):
        paragraph_text = paragraph['text']
        paragraph_labels = paragraph['charlabels']
        paragraph_mwt_labels = paragraph['mwtlabels']
        # split to sentences
        sentences = split_to_sentences(paragraph_text, paragraph_labels, paragraph_mwt_labels, treebank_name)
        tmp_examples = []
        for sent in sentences:
            sent_text, sent_labels, sent_mwt_labels, sent_start, sent_end = sent
            wordpieces, wordpiece_labels, wordpiece_ends, end_piece_ids = wordpiece_tokenize_from_raw_text(
                tokenizer, sent_text,
                sent_labels, sent_start,
                treebank_name)
            kept_tokens += len([x for x in wordpiece_labels if x != 0])
            total_tokens += len([x for x in sent_labels if x != '0'])
            if len(wordpieces) <= max_input_length - 2:  # minus 2: reserved for <s> and </s>
                tmp_examples.append((wordpieces, wordpiece_labels, sent_mwt_labels, wordpiece_ends, end_piece_ids))
            else:
                subsequences = split_to_subsequences(wordpieces, wordpiece_labels, sent_mwt_labels, wordpiece_ends,
                                                     end_piece_ids,
                                                     max_input_length)
                for subseq in subsequences:
                    tmp_examples.append(subseq)
        # merge consecutive sentences/subsequences
        new_example = [[], [], [], []]
        for example in tmp_examples:
            if len(new_example[0]) + len(example[0]) > max_input_length - 2:
                num_extra_wordpieces = min(max_input_length - 2 - len(new_example[0]), len(example[0]))
                end_piece_ids = example[-1]
                takeout_position = 0
                for tmp_id in range(num_extra_wordpieces):
                    wp, wpid = example[0][tmp_id]
                    if wpid in end_piece_ids:
                        takeout_position = tmp_id + 1
                num_extra_wordpieces = takeout_position
                new_example[0] += deepcopy(example[0][: num_extra_wordpieces])
                new_example[1] += deepcopy(example[1][: num_extra_wordpieces])

                extra_mwt_labels = []
                mwt_id = 0
                for pid in range(num_extra_wordpieces):
                    if example[1][pid] == 3 or example[1][pid] == 4:
                        extra_mwt_labels.append(deepcopy(example[2][mwt_id]))
                        mwt_id += 1
                new_example[2] += extra_mwt_labels

                new_example[3] += deepcopy(example[3][: num_extra_wordpieces])
                wordpiece_examples.append(
                    ([wp for wp, wpid in new_example[0]], new_example[1], new_example[2], new_example[3],
                     paragraph_index))
                # start new example
                new_example = [[], [], [], []]

            new_example[0] += deepcopy(example[0])
            new_example[1] += deepcopy(example[1])
            new_example[2] += deepcopy(example[2])
            new_example[3] += deepcopy(example[3])
        if len(new_example[0]) > 0:
            wordpiece_examples.append(
                ([wp for wp, wpid in new_example[0]], new_example[1], new_example[2], new_example[3], paragraph_index))

    final_examples = []
    for wp_example in wordpiece_examples:
        wordpieces, wordpiece_labels, seq_mwt_labels, wordpiece_ends, paragraph_index = wp_example
        final_examples.append({
            'wordpieces': wordpieces,
            'wordpiece_labels': wordpiece_labels,
            'mwt_labels': seq_mwt_labels,
            'wordpiece_ends': wordpiece_ends,
            'paragraph_index': paragraph_index
        })

    with open(wordpiece_labels_output_fpath, 'w') as f:
        json.dump(final_examples, f)
    return final_examples

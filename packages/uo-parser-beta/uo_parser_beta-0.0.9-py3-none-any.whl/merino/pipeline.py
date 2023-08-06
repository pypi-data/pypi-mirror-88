from .config import config as master_config
from .models.base_models import Multilingual_Embedding
from .models.classifiers import TokenizerClassifier, TaggerClassifier, NERClassifier
from .models.mwt_model import MWTWrapper
from .models.lemma_model import LemmaWrapper
from .iterators.tokenizer_iterators import TokenizeDatasetLive, TokenizeDataset
from .iterators.tagger_iterators import TaggerDatasetLive
from .iterators.ner_iterators import NERDatasetLive
from .utils.tokenizer_utils import *
from collections import defaultdict
from .utils.doc import *
from .utils.conll import CoNLL
from .utils.conll2 import CoNLL as CoNLL2
from .utils.tbinfo import tbname2training_id, lang2treebank
from .utils.chuliu_edmonds import *
from transformers import XLMRobertaTokenizer


class Pipeline:
    def __init__(self, language, cache_dir=None):
        super(Pipeline, self).__init__()

        if cache_dir is None:
            master_config.cache_dir = 'cache/merino'
        else:
            master_config.cache_dir = cache_dir

        if not os.path.exists(master_config.cache_dir):
            os.makedirs(master_config.cache_dir, exist_ok=True)

        master_config.wordpiece_splitter = XLMRobertaTokenizer.from_pretrained('xlm-roberta-base',
                                                                               cache_dir=os.path.join(
                                                                                   master_config.cache_dir,
                                                                                   'xlmr'))
        self.lang_list = [language]
        for lang in self.lang_list:
            assert lang in lang2treebank, '{} has not been supported. Currently supported languages: {}'.format(lang,
                                                                                                                list(
                                                                                                                    lang2treebank.keys()))
        self.config = master_config

        # download saved model for initial language
        download(
            cache_dir=self.config.cache_dir,
            language=language
        )

        # load ALL vocabs
        self.load_vocabs()

        # shared multilingual embeddings
        self.embedding_layers = Multilingual_Embedding(self.config)
        self.embedding_layers.to(self.config.device)
        self.embedding_layers.eval()
        # tokenizers
        self.tokenizer = {}
        for lang in self.lang_list:
            self.tokenizer[lang] = TokenizerClassifier(self.config, treebank_name=lang2treebank[lang])
            self.tokenizer[lang].to(self.config.device)
            self.tokenizer[lang].eval()
        # taggers
        self.tagger = {}
        for lang in self.lang_list:
            self.tagger[lang] = TaggerClassifier(self.config, treebank_name=lang2treebank[lang])
            self.tagger[lang].to(self.config.device)
            self.tagger[lang].eval()

        #     - mwt and lemma:
        self.mwt_model = {}
        for lang in self.lang_list:
            treebank_name = lang2treebank[lang]
            if tbname2training_id[treebank_name] % 2 == 1:
                self.mwt_model[lang] = MWTWrapper(self.config, treebank_name=treebank_name)
        self.lemma_model = {}
        for lang in self.lang_list:
            treebank_name = lang2treebank[lang]
            self.lemma_model[lang] = LemmaWrapper(self.config, treebank_name=treebank_name)
        # ner if possible
        self.ner_model = {}
        for lang in self.lang_list:
            if lang in lang2nercorpus:
                self.ner_model[lang] = NERClassifier(self.config, lang)
                self.ner_model[lang].to(self.config.device)
                self.ner_model[lang].eval()

        # load and hold the pretrained weights
        self.embedding_weights = self.embedding_layers.state_dict()
        self.set_default_language(language)

    def set_default_language(self, language):
        assert language in self.lang_list
        self.config.default_language = language
        self.default_language = language
        self.config.treebank_name = lang2treebank[language]
        print('Default language: {}'.format(self.config.default_language))

    def add_language(self, lang):
        if lang in self.lang_list:
            print('Language `{}` was already added'.format(lang))
        else:
            # download saved models
            download(
                cache_dir=self.config.cache_dir,
                language=lang
            )
            # update vocabs
            treebank_name = lang2treebank[lang]
            with open(os.path.join(self.config.cache_dir,
                                   '{}/{}.vocabs.json'.format(treebank2lang[treebank_name],
                                                              treebank2lang[treebank_name]))) as f:
                vocabs = json.load(f)
                self.config.vocabs[treebank_name] = vocabs
            if lang in lang2nercorpus:
                with open(os.path.join(self.config.cache_dir,
                                       '{}/{}.ner-vocab.json'.format(lang, lang))) as f:
                    self.config.ner_vocabs[lang] = json.load(f)
            self.config.itos[lang][UPOS] = {v: k for k, v in vocabs[UPOS].items()}
            self.config.itos[lang][XPOS] = {v: k for k, v in vocabs[XPOS].items()}
            self.config.itos[lang][FEATS] = {v: k for k, v in vocabs[FEATS].items()}
            self.config.itos[lang][DEPREL] = {v: k for k, v in vocabs[DEPREL].items()}
            # add tokenizer
            self.tokenizer[lang] = TokenizerClassifier(self.config, treebank_name=lang2treebank[lang])
            self.tokenizer[lang].to(self.config.device)
            self.tokenizer[lang].eval()
            # add tagger
            self.tagger[lang] = TaggerClassifier(self.config, treebank_name=lang2treebank[lang])
            self.tagger[lang].to(self.config.device)
            self.tagger[lang].eval()
            # mwt if needed
            treebank_name = lang2treebank[lang]
            if tbname2training_id[treebank_name] % 2 == 1:
                self.mwt_model[lang] = MWTWrapper(self.config, treebank_name=treebank_name)
            # lemma
            self.lemma_model[lang] = LemmaWrapper(self.config, treebank_name=treebank_name)
            # ner if possible
            if lang in lang2nercorpus:
                self.ner_model[lang] = NERClassifier(self.config, lang)
                self.ner_model[lang].to(self.config.device)
                self.ner_model[lang].eval()
            self.lang_list.append(lang)

    def load_vocabs(self):
        self.config.vocabs = {}
        self.config.ner_vocabs = {}
        self.config.itos = defaultdict(dict)
        for lang in self.lang_list:
            treebank_name = lang2treebank[lang]
            with open(os.path.join(self.config.cache_dir,
                                   '{}/{}.vocabs.json'.format(lang, lang))) as f:
                vocabs = json.load(f)
                self.config.vocabs[treebank_name] = vocabs
            self.config.itos[lang][UPOS] = {v: k for k, v in vocabs[UPOS].items()}
            self.config.itos[lang][XPOS] = {v: k for k, v in vocabs[XPOS].items()}
            self.config.itos[lang][FEATS] = {v: k for k, v in vocabs[FEATS].items()}
            self.config.itos[lang][DEPREL] = {v: k for k, v in vocabs[DEPREL].items()}
            # ner vocabs
            if lang in lang2nercorpus:
                with open(os.path.join(self.config.cache_dir,
                                       '{}/{}.ner-vocab.json'.format(lang, lang))) as f:
                    self.config.ner_vocabs[lang] = json.load(f)

    def load_adapter_weights(self, model_name):
        assert model_name in ['tokenizer', 'tagger', 'ner']
        if model_name == 'tokenizer':
            pretrained_weights = self.tokenizer[self.config.default_language].pretrained_tokenizer_weights
        elif model_name == 'tagger':
            pretrained_weights = self.tagger[self.config.default_language].pretrained_tagger_weights
        else:
            assert model_name == 'ner'
            pretrained_weights = self.ner_model[self.config.default_language].pretrained_ner_weights

        for name, value in pretrained_weights.items():
            if 'adapters.{}.adapter'.format(model_name) in name:
                target_name = name.replace('adapters.{}.adapter'.format(model_name), 'adapters.embedding.adapter')
                self.embedding_weights[target_name] = value
        self.embedding_layers.load_state_dict(self.embedding_weights)

    def tokenize(self, raw_text, eval_batch_size=1):
        # load input text
        config = self.config
        test_set = TokenizeDatasetLive(config, raw_text)
        test_set.numberize(config.wordpiece_splitter)

        # load weights of tokenizer into the combined model
        self.load_adapter_weights(model_name='tokenizer')

        # make predictions
        wordpiece_pred_labels, wordpiece_ends, paragraph_indexes = [], [], []
        for batch in DataLoader(test_set, batch_size=eval_batch_size,
                                shuffle=False, collate_fn=test_set.collate_fn):
            wordpiece_reprs = self.embedding_layers.get_tokenizer_inputs(batch)
            predictions = self.tokenizer[self.config.default_language].predict(batch, wordpiece_reprs)
            wp_pred_labels, wp_ends, para_ids = predictions[0], predictions[1], predictions[2]
            wp_pred_labels = wp_pred_labels.data.cpu().numpy().tolist()

            for i in range(len(wp_pred_labels)):
                wordpiece_pred_labels.append(wp_pred_labels[i][: len(wp_ends[i])])

            wordpiece_ends.extend(wp_ends)
            paragraph_indexes.extend(para_ids)
        # mapping
        para_id_to_wp_pred_labels = defaultdict(list)

        for wp_pred_ls, wp_es, p_index in zip(wordpiece_pred_labels, wordpiece_ends,
                                              paragraph_indexes):
            para_id_to_wp_pred_labels[p_index].extend([(pred, char_position) for pred, char_position in
                                                       zip(wp_pred_ls, wp_es)])
        # get predictions
        corpus_text = raw_text

        paragraphs = [pt.rstrip() for pt in
                      NEWLINE_WHITESPACE_RE.split(corpus_text) if
                      len(pt.rstrip()) > 0]
        all_wp_preds = []
        all_raw = []
        ##############
        for para_index, para_text in enumerate(paragraphs):
            para_wp_preds = [0 for _ in para_text]
            for wp_l, end_position in para_id_to_wp_pred_labels[para_index]:
                para_wp_preds[end_position] = wp_l

            all_wp_preds.append(para_wp_preds)
            all_raw.append(para_text)
        ###########################3
        offset = 0
        doc = []
        for j in range(len(paragraphs)):
            raw = all_raw[j]
            wp_pred = all_wp_preds[j]

            current_tok = ''
            current_sent = []

            for t, wp_p in zip(raw, wp_pred):
                offset += 1
                current_tok += t
                if wp_p >= 1:
                    tok = normalize_token(test_set.treebank_name, current_tok)
                    assert '\t' not in tok, tok
                    if len(tok) <= 0:
                        current_tok = ''
                        continue
                    additional_info = dict()
                    current_sent += [(tok, wp_p, additional_info)]
                    current_tok = ''
                    if (wp_p == 2 or wp_p == 4):
                        doc.append(process_sentence(current_sent))
                        current_sent = []

            if len(current_tok):
                tok = normalize_token(test_set.treebank_name, current_tok)
                assert '\t' not in tok, tok
                if len(tok) > 0:
                    additional_info = dict()
                    current_sent += [(tok, 2, additional_info)]

            if len(current_sent):
                doc.append(process_sentence(current_sent))

        return doc

    def tag_sentence(self, tokenized_sentence):
        temp = []
        for i, word in enumerate(tokenized_sentence):
            temp.append({ID: f'{i + 1}', TEXT: word})
        tokenized_doc = [temp]

        CoNLL.dict2conll(tokenized_doc,
                         os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language)))
        tokenized_doc = CoNLL2.conll2dict(
            os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language)))
        return self.tag(tokenized_doc)[0]

    def tag(self, tokenized_doc):
        # load outputs of tokenizer
        config = self.config
        # write to buffer
        CoNLL2.dict2conll(tokenized_doc,
                          os.path.join(self.config.cache_dir,
                                       'buff.tag.{}'.format(self.config.default_language)))
        test_set = TaggerDatasetLive(
            conllu_fpath=os.path.join(self.config.cache_dir, 'buff.tag.{}'.format(self.config.default_language)),
            wordpiece_splitter=config.wordpiece_splitter,
            config=config
        )
        test_set.numberize()

        # load weights of tagger into the combined model
        self.load_adapter_weights(model_name='tagger')

        # make predictions

        for batch in DataLoader(test_set, batch_size=self.config.eval_batch_size,
                                shuffle=False, collate_fn=test_set.collate_fn):
            batch_size = len(batch.word_num)

            word_reprs, cls_reprs = self.embedding_layers.get_tagger_inputs(batch)
            predictions = self.tagger[self.config.default_language].predict(batch, word_reprs, cls_reprs)
            predicted_upos = predictions[0]
            predicted_xpos = predictions[1]
            predicted_feats = predictions[2]

            predicted_upos = predicted_upos.data.cpu().numpy().tolist()
            predicted_xpos = predicted_xpos.data.cpu().numpy().tolist()
            predicted_feats = predicted_feats.data.cpu().numpy().tolist()

            # head, deprel
            predicted_dep = predictions[3]
            sentlens = [l + 1 for l in batch.word_num]
            head_seqs = [chuliu_edmonds_one_root(adj[:l, :l])[1:] for adj, l in
                         zip(predicted_dep[0], sentlens)]  # remove attachment for the root
            deprel_seqs = [
                [self.config.itos[self.config.default_language][DEPREL][predicted_dep[1][i][j + 1][h]] for j, h in
                 enumerate(hs)] for
                i, hs
                in
                enumerate(head_seqs)]

            pred_tokens = [[[str(head_seqs[i][j]), deprel_seqs[i][j]] for j in range(sentlens[i] - 1)] for i in
                           range(batch_size)]

            for bid in range(batch_size):
                for i in range(batch.word_num[bid]):
                    sentid = batch.sent_index[bid]
                    wordid = batch.word_ids[bid][i]

                    # upos
                    pred_upos_id = predicted_upos[bid][i]
                    upos_name = self.config.itos[self.config.default_language][UPOS][pred_upos_id]
                    test_set.conllu_doc[sentid][wordid][UPOS] = upos_name
                    # xpos
                    pred_xpos_id = predicted_xpos[bid][i]
                    xpos_name = self.config.itos[self.config.default_language][XPOS][pred_xpos_id]
                    test_set.conllu_doc[sentid][wordid][XPOS] = xpos_name
                    # feats
                    pred_feats_id = predicted_feats[bid][i]
                    feats_name = self.config.itos[self.config.default_language][FEATS][pred_feats_id]
                    test_set.conllu_doc[sentid][wordid][FEATS] = feats_name

                    # head
                    test_set.conllu_doc[sentid][wordid][HEAD] = pred_tokens[bid][i][0]
                    # deprel
                    test_set.conllu_doc[sentid][wordid][DEPREL] = pred_tokens[bid][i][1]
        tagged_doc = process_doc(conllu_doc=test_set.conllu_doc)
        return tagged_doc

    def lemmatize(self, tagged_doc):
        lemmatized_doc = self.lemma_model[self.config.default_language].predict(tagged_doc)
        return lemmatized_doc

    def mwt_expand(self, tokenized_doc):
        expanded_doc = self.mwt_model[self.config.default_language].predict(tokenized_doc)
        return expanded_doc

    def ner(self, final_doc):
        sentences = []
        start = -1
        end = -1
        for sent in final_doc:
            tokens = []
            for tok in sent:
                if type(tok['id']) == int and start <= tok['id'] <= end:
                    if tok['id'] == end:
                        start = -1
                        end = -1
                    continue
                else:
                    tokens.append(tok[TEXT])
                    if type(tok['id']) == tuple and len(tok['id']) == 2:
                        start = tok['id'][0]
                        end = tok['id'][1]
            sentences.append(tokens)
        test_set = NERDatasetLive(
            config=self.config,
            tokenized_sentences=sentences
        )
        test_set.numberize()
        # load ner adapter weights
        self.load_adapter_weights(model_name='ner')

        predictions = []
        for batch in DataLoader(test_set, batch_size=self.config.eval_batch_size,
                                shuffle=False, collate_fn=test_set.collate_fn):
            word_reprs, cls_reprs = self.embedding_layers.get_tagger_inputs(batch)
            pred_entity_labels = self.ner_model[self.config.default_language].predict(batch, word_reprs)
            predictions += pred_entity_labels

        start = -1
        end = -1
        for sid in range(len(final_doc)):
            tagged_id = 0
            for tid in range(len(final_doc[sid])):
                if type(final_doc[sid][tid]['id']) == int and start <= final_doc[sid][tid]['id'] <= end:
                    if final_doc[sid][tid]['id'] == end:
                        start = -1
                        end = -1
                    continue
                else:
                    final_doc[sid][tid][NER] = predictions[sid][tagged_id]
                    tagged_id += 1
                    if type(final_doc[sid][tid]['id']) == tuple and len(final_doc[sid][tid]['id']) == 2:
                        start = final_doc[sid][tid]['id'][0]
                        end = final_doc[sid][tid]['id'][1]
        return final_doc

    def analyze(self, raw_text):
        tokenized_doc = self.tokenize(raw_text)
        if tbname2training_id[self.config.treebank_name] % 2 == 1:
            tokenized_doc = self.mwt_expand(tokenized_doc)
        else:
            CoNLL.dict2conll(tokenized_doc,
                             os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language)))
            tokenized_doc = CoNLL2.conll2dict(
                os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language)))
        tagged_doc = self.tag(tokenized_doc)
        final_doc = self.lemmatize(tagged_doc)
        if self.config.default_language in lang2nercorpus:  # ner if possible
            final_doc = self.ner(final_doc)

        return final_doc

    ############################## CONLLU PREDICTION #############################
    def conllu_tokenize(self, raw_text_fpath, treebank_name, language, eval_batch_size=1):
        data_set = TokenizeDataset(self.config, text_fpath=raw_text_fpath, treebank_name=treebank_name,
                                   language=language)
        data_set.numberize(self.config.wordpiece_splitter)
        batch_num = len(data_set) // eval_batch_size + \
                    (len(data_set) % eval_batch_size != 0)

        # load weights of tokenizer into the combined model
        self.load_adapter_weights(model_name='tokenizer')

        # evaluate
        progress = tqdm(total=batch_num, ncols=75,
                        desc='Conllu Tokenize')
        wordpiece_pred_labels, wordpiece_ends, paragraph_indexes = [], [], []
        for batch in DataLoader(data_set, batch_size=eval_batch_size,
                                shuffle=False, collate_fn=data_set.collate_fn):
            progress.update(1)
            wordpiece_reprs = self.embedding_layers.get_tokenizer_inputs(batch)
            predictions = self.tokenizer[language].predict(batch, wordpiece_reprs)
            wp_pred_labels, wp_ends, para_ids = predictions[0], predictions[1], predictions[2]
            wp_pred_labels = wp_pred_labels.data.cpu().numpy().tolist()

            for i in range(len(wp_pred_labels)):
                wordpiece_pred_labels.append(wp_pred_labels[i][: len(wp_ends[i])])

            wordpiece_ends.extend(wp_ends)
            paragraph_indexes.extend(para_ids)
        progress.close()
        # mapping
        para_id_to_wp_pred_labels = defaultdict(list)

        for wp_pred_ls, wp_es, p_index in zip(wordpiece_pred_labels, wordpiece_ends,
                                              paragraph_indexes):
            para_id_to_wp_pred_labels[p_index].extend([(pred, char_position) for pred, char_position in
                                                       zip(wp_pred_ls, wp_es)])
        # compute scores
        with open(data_set.plaintext_file, 'r') as f:
            corpus_text = ''.join(f.readlines())

        paragraphs = [pt.rstrip() for pt in
                      NEWLINE_WHITESPACE_RE.split(corpus_text) if
                      len(pt.rstrip()) > 0]
        all_wp_preds = []
        all_raw = []
        ##############
        for para_index, para_text in enumerate(paragraphs):
            para_wp_preds = [0 for _ in para_text]
            for wp_l, end_position in para_id_to_wp_pred_labels[para_index]:
                para_wp_preds[end_position] = wp_l

            all_wp_preds.append(para_wp_preds)
            all_raw.append(para_text)
        ###########################3
        offset = 0
        doc = []
        for j in range(len(paragraphs)):
            raw = all_raw[j]
            wp_pred = all_wp_preds[j]

            current_tok = ''
            current_sent = []

            for t, wp_p in zip(raw, wp_pred):
                offset += 1
                current_tok += t
                if wp_p >= 1:
                    tok = normalize_token(data_set.treebank_name, current_tok)
                    assert '\t' not in tok, tok
                    if len(tok) <= 0:
                        current_tok = ''
                        continue
                    additional_info = dict()
                    current_sent += [(tok, wp_p, additional_info)]
                    current_tok = ''
                    if (wp_p == 2 or wp_p == 4):
                        doc.append(process_sentence(current_sent))
                        current_sent = []

            if len(current_tok):
                tok = normalize_token(data_set.treebank_name, current_tok)
                assert '\t' not in tok, tok
                if len(tok) > 0:
                    additional_info = dict()
                    current_sent += [(tok, 2, additional_info)]

            if len(current_sent):
                doc.append(process_sentence(current_sent))

        pred_conllu_fpath = os.path.join(data_set.output_dir, os.path.basename(raw_text_fpath) + '.tokenized.conllu')
        CoNLL.dict2conll(doc, pred_conllu_fpath)
        return pred_conllu_fpath

    def conllu_tag(self, pred_tokenize_fpath):
        # load outputs of tokenizer
        config = self.config
        # write to buffer
        test_set = TaggerDatasetLive(
            conllu_fpath=pred_tokenize_fpath,
            wordpiece_splitter=config.wordpiece_splitter,
            config=config
        )
        test_set.numberize()

        # load weights of tagger into the combined model
        self.load_adapter_weights(model_name='tagger')

        # make predictions
        batch_num = len(test_set) // self.config.eval_batch_size + \
                    (len(test_set) % self.config.eval_batch_size != 0)
        progress = tqdm(total=batch_num, ncols=75,
                        desc='Conllu tag')

        for batch in DataLoader(test_set, batch_size=self.config.eval_batch_size,
                                shuffle=False, collate_fn=test_set.collate_fn):
            progress.update(1)
            batch_size = len(batch.word_num)

            word_reprs, cls_reprs = self.embedding_layers.get_tagger_inputs(batch)
            predictions = self.tagger[self.config.default_language].predict(batch, word_reprs, cls_reprs)
            predicted_upos = predictions[0]
            predicted_xpos = predictions[1]
            predicted_feats = predictions[2]

            predicted_upos = predicted_upos.data.cpu().numpy().tolist()
            predicted_xpos = predicted_xpos.data.cpu().numpy().tolist()
            predicted_feats = predicted_feats.data.cpu().numpy().tolist()

            # head, deprel
            predicted_dep = predictions[3]
            sentlens = [l + 1 for l in batch.word_num]
            head_seqs = [chuliu_edmonds_one_root(adj[:l, :l])[1:] for adj, l in
                         zip(predicted_dep[0], sentlens)]  # remove attachment for the root
            deprel_seqs = [
                [self.config.itos[self.config.default_language][DEPREL][predicted_dep[1][i][j + 1][h]] for j, h in
                 enumerate(hs)] for
                i, hs
                in
                enumerate(head_seqs)]

            pred_tokens = [[[str(head_seqs[i][j]), deprel_seqs[i][j]] for j in range(sentlens[i] - 1)] for i in
                           range(batch_size)]

            for bid in range(batch_size):
                for i in range(batch.word_num[bid]):
                    sentid = batch.sent_index[bid]
                    wordid = batch.word_ids[bid][i]

                    # upos
                    pred_upos_id = predicted_upos[bid][i]
                    upos_name = self.config.itos[self.config.default_language][UPOS][pred_upos_id]
                    test_set.conllu_doc[sentid][wordid][UPOS] = upos_name
                    # xpos
                    pred_xpos_id = predicted_xpos[bid][i]
                    xpos_name = self.config.itos[self.config.default_language][XPOS][pred_xpos_id]
                    test_set.conllu_doc[sentid][wordid][XPOS] = xpos_name
                    # feats
                    pred_feats_id = predicted_feats[bid][i]
                    feats_name = self.config.itos[self.config.default_language][FEATS][pred_feats_id]
                    test_set.conllu_doc[sentid][wordid][FEATS] = feats_name

                    # head
                    test_set.conllu_doc[sentid][wordid][HEAD] = pred_tokens[bid][i][0]
                    # deprel
                    test_set.conllu_doc[sentid][wordid][DEPREL] = pred_tokens[bid][i][1]
        progress.close()
        tagged_doc = process_doc(conllu_doc=test_set.conllu_doc)
        pred_conllu_fpath = pred_tokenize_fpath + '.tagged'
        CoNLL.dict2conll(tagged_doc, pred_conllu_fpath)
        return pred_conllu_fpath

    def conllu_predict(self, raw_text_fpath, treebank_name, language):
        # tokenize
        pred_tokenize_fpath = self.conllu_tokenize(raw_text_fpath, treebank_name, language)
        if tbname2training_id[treebank_name] % 2 == 1:
            # mwt
            pred_tokenize_fpath = self.mwt_model[language].conllu_predict(pred_tokenize_fpath)
        # tag
        pred_tag_fpath = self.conllu_tag(pred_tokenize_fpath)
        # lemma
        pred_lemma_fpath = self.lemma_model[language].conllu_predict(pred_tag_fpath)
        return pred_lemma_fpath

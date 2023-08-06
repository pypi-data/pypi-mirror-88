# This is adapted from stanza
from copy import deepcopy
from .seq2seq_model import Seq2SeqModel
from ..utils.conll import CoNLL
from ..utils.conll2 import CoNLL as CoNLL2
from merino.utils.tbinfo import tbname2shorthand, treebank2lang
from ..utils.doc import *
from ..utils.seq2seq_utils import *
from ..utils.seq2seq_vocabs import *
from ..iterators.mwt_iterators import MWTDataLoader


class Trainer(object):
    """ A trainer for training models. """

    def __init__(self, args=None, vocab=None, emb_matrix=None, model_file=None, use_cuda=False):
        self.use_cuda = use_cuda
        if model_file is not None:
            # load from file
            self.load(model_file, use_cuda)
        else:
            self.args = args
            self.model = None if args['dict_only'] else Seq2SeqModel(args, emb_matrix=emb_matrix)
            self.vocab = vocab
            self.expansion_dict = dict()
        if not self.args['dict_only']:
            self.crit = SequenceLoss(self.vocab.size)
            self.parameters = [p for p in self.model.parameters() if p.requires_grad]
            if use_cuda:
                self.model.cuda()
                self.crit.cuda()
            else:
                self.model.cpu()
                self.crit.cpu()
            self.optimizer = get_optimizer(self.args['optim'], self.parameters, self.args['lr'])

    def update(self, batch, eval=False):
        inputs, orig_idx = unpack_mwt_batch(batch, self.use_cuda)
        src, src_mask, tgt_in, tgt_out = inputs

        if eval:
            self.model.eval()
        else:
            self.model.train()
            self.optimizer.zero_grad()
        log_probs, _ = self.model(src, src_mask, tgt_in)
        loss = self.crit(log_probs.view(-1, self.vocab.size), tgt_out.view(-1))
        loss_val = loss.data.item()
        if eval:
            return loss_val

        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.args['max_grad_norm'])
        self.optimizer.step()
        return loss_val

    def predict(self, batch):
        inputs, orig_idx = unpack_mwt_batch(batch, self.use_cuda)
        src, src_mask, tgt, tgt_mask = inputs

        self.model.eval()
        batch_size = src.size(0)
        preds, _ = self.model.predict(src, src_mask, self.args['beam_size'])
        pred_seqs = [self.vocab.unmap(ids) for ids in preds]  # unmap to tokens
        pred_seqs = prune_decoded_seqs(pred_seqs)
        pred_tokens = ["".join(seq) for seq in pred_seqs]  # join chars to be tokens
        pred_tokens = unsort(pred_tokens, orig_idx)
        return pred_tokens

    def train_dict(self, pairs):
        """ Train a MWT expander given training word-expansion pairs. """
        # accumulate counter
        ctr = Counter()
        ctr.update(
            [(p[0], p[1]) for p in pairs])  # p[0]: source token, p[1]: expanded form that consists of multiple words
        seen = set()
        # find the most frequent mappings
        for p, _ in ctr.most_common():
            w, l = p  # w: src token, l: expanded form that consists of multiple words
            if w not in seen and w != l:
                self.expansion_dict[w] = l
            seen.add(w)
        return

    def predict_dict(self, words):
        """ Predict a list of expansions given words. """
        expansions = []
        for w in words:
            if w in self.expansion_dict:
                expansions += [self.expansion_dict[w]]
            elif w.lower() in self.expansion_dict:
                expansions += [self.expansion_dict[w.lower()]]
            else:
                expansions += [w]
        return expansions

    def ensemble(self, cands, other_preds):
        """ Ensemble the dict with statistical model predictions. """
        expansions = []
        assert len(cands) == len(other_preds)
        for c, pred in zip(cands, other_preds):
            if c in self.expansion_dict:
                expansions += [self.expansion_dict[c]]
            elif c.lower() in self.expansion_dict:
                expansions += [self.expansion_dict[c.lower()]]
            else:
                expansions += [pred]
        return expansions

    def save(self, filename):
        params = {
            'model': self.model.state_dict() if self.model is not None else None,
            'dict': self.expansion_dict,
            'vocab': self.vocab.state_dict(),
            'config': self.args
        }
        try:
            torch.save(params, filename)
        except BaseException:
            raise

    def load(self, filename, use_cuda=False):
        try:
            checkpoint = torch.load(filename, lambda storage, loc: storage)
        except BaseException:
            raise
        self.args = checkpoint['config']
        self.expansion_dict = checkpoint['dict']
        if not self.args['dict_only']:
            self.model = Seq2SeqModel(self.args, use_cuda=use_cuda)
            self.model.load_state_dict(checkpoint['model'])
        else:
            self.model = None
        self.vocab = Vocab.load_state_dict(checkpoint['vocab'])


def get_mwt_model(cache_dir, language):
    args = {
        'train_file': '',
        'eval_file': '',
        'output_file': '',
        'gold_file': '',
        'mode': 'predict',
        'lang': '',
        'shorthand': '',
        'ensemble_dict': True,
        'ensemble_early_stop': False,
        'dict_only': False,
        'hidden_dim': 100,
        'emb_dim': 50,
        'num_layers': 1,
        'emb_dropout': 0.5,
        'dropout': 0.5,
        'max_dec_len': 50,
        'beam_size': 1,
        'attn_type': 'soft',
        'sample_train': 1.0,
        'optim': 'adam',
        'lr': 1e-3,
        'lr_decay': 0.9,
        'decay_epoch': 30,
        'num_epoch': 50,
        'batch_size': 50,
        'max_grad_norm': 5.0,
        'log_step': 20,
        'save_name': '',
        'seed': 1234
    }
    args['shorthand'] = language
    # ############## load model #############
    # file paths
    model_file = os.path.join(cache_dir, '{}/{}_mwt_expander.pt'.format(language, language))
    args['data_dir'] = os.path.join(cache_dir, language)
    args['save_dir'] = os.path.join(cache_dir, language)
    # load model
    use_cuda = True if torch.cuda.is_available() else False
    trainer = Trainer(model_file=model_file, use_cuda=use_cuda)
    loaded_args, vocab = trainer.args, trainer.vocab

    for k in args:
        if k.endswith('_dir') or k.endswith('_file') or k in ['shorthand']:
            loaded_args[k] = args[k]

    return trainer, args, loaded_args, vocab


class MWTWrapper:
    # adapted from stanza
    def __init__(self, config, treebank_name):
        self.config = config
        self.shorthand = tbname2shorthand[treebank_name]
        self.model, self.args, self.loaded_args, self.vocab = get_mwt_model(config.cache_dir,
                                                                            language=treebank2lang[treebank_name])
        print('Loaded multi-word expander for {}'.format(treebank2lang[treebank_name]))

    def conllu_predict(self, tokenized_conllu):
        args = self.args
        loaded_args = self.loaded_args
        vocab = self.vocab
        # load data
        doc = Document(
            CoNLL2.conll2dict(tokenized_conllu))
        batch = MWTDataLoader(doc, args['batch_size'], loaded_args, vocab=vocab, evaluation=True)

        if len(batch) > 0:
            dict_preds = self.model.predict_dict(batch.doc.get_mwt_expansions(evaluation=True))
            # decide trainer type and run eval
            if loaded_args['dict_only']:
                preds = dict_preds
            else:
                preds = []
                for i, b in enumerate(batch):
                    preds += self.model.predict(b)

                if loaded_args.get('ensemble_dict', False):
                    preds = self.model.ensemble(batch.doc.get_mwt_expansions(evaluation=True), preds)
        else:
            # skip eval if dev data does not exist
            preds = []

        # write to file and score
        doc = deepcopy(batch.doc)
        doc.set_mwt_expansions(preds)
        pred_conllu_fpath = tokenized_conllu.replace('.tokenized.conllu', '.mwt.conllu')
        CoNLL2.dict2conll(doc.to_dict(), pred_conllu_fpath)
        return pred_conllu_fpath

    def predict(self, tokenized_doc):
        args = self.args
        loaded_args = self.loaded_args
        vocab = self.vocab
        # load data
        # write to buffer
        CoNLL.dict2conll(tokenized_doc,
                         os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language)))
        # load from buffer
        doc = Document(
            CoNLL2.conll2dict(
                os.path.join(self.config.cache_dir, 'buff.tok.{}'.format(self.config.default_language))))
        batch = MWTDataLoader(doc, args['batch_size'], loaded_args, vocab=vocab, evaluation=True)

        if len(batch) > 0:
            dict_preds = self.model.predict_dict(batch.doc.get_mwt_expansions(evaluation=True))
            # decide trainer type and run eval
            if loaded_args['dict_only']:
                preds = dict_preds
            else:
                preds = []
                for i, b in enumerate(batch):
                    preds += self.model.predict(b)

                if loaded_args.get('ensemble_dict', False):
                    preds = self.model.ensemble(batch.doc.get_mwt_expansions(evaluation=True), preds)
        else:
            # skip eval if dev data does not exist
            preds = []

        # write to file and score
        doc = deepcopy(batch.doc)
        doc.set_mwt_expansions(preds)
        expanded_doc = doc.to_dict()
        return expanded_doc

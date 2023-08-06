from .base_models import *
from .crf_model import CRFLoss, viterbi_decode
from ..utils.base_utils import *


class NERClassifier(nn.Module):
    def __init__(self, config, language):
        super().__init__()
        self.config = config
        self.xlmr_dim = 768
        self.entity_label_stoi = config.ner_vocabs[language]  # BIOES tags
        self.entity_label_itos = {i: s for s, i in self.entity_label_stoi.items()}
        self.entity_label_num = len(self.entity_label_stoi)

        self.entity_label_ffn = Linears([self.xlmr_dim, config.hidden_num,
                                         self.entity_label_num],
                                        dropout_prob=config.linear_dropout,
                                        bias=config.linear_bias,
                                        activation=config.linear_activation)

        self.crit = CRFLoss(self.entity_label_num)

        # load pretrained weights
        self.initialized_weights = self.state_dict()
        self.pretrained_ner_weights = torch.load(os.path.join(self.config.cache_dir, language,
                                                              '{}.ner.mdl'.format(
                                                                  language)), map_location=self.config.device)['adapters']

        for name, value in self.pretrained_ner_weights.items():
            if name in self.initialized_weights:
                self.initialized_weights[name] = value
        self.load_state_dict(self.initialized_weights)
        print('Loaded NER for {}'.format(language))

    def predict(self, batch, word_reprs):
        batch_size, _, _ = word_reprs.size()

        logits = self.entity_label_ffn(word_reprs)
        _, trans = self.crit(logits, batch.word_mask, batch.entity_label_idxs)
        # decode
        trans = trans.data.cpu().numpy()
        scores = logits.data.cpu().numpy()
        bs = logits.size(0)
        tag_seqs = []
        for i in range(bs):
            tags, _ = viterbi_decode(scores[i, :batch.word_num[i]], trans)
            tags = [self.entity_label_itos[t] for t in tags]
            tag_seqs += [tags]
        return tag_seqs


class TaggerClassifier(nn.Module):
    def __init__(self, config, treebank_name):
        super().__init__()
        self.config = config

        self.xlmr_dim = 768
        self.upos_embedding = nn.Embedding(
            num_embeddings=len(config.vocabs[treebank_name][UPOS]),
            embedding_dim=50
        )
        # pos tagging
        self.upos_ffn = nn.Linear(self.xlmr_dim, len(config.vocabs[treebank_name][UPOS]))
        self.xpos_ffn = nn.Linear(self.xlmr_dim + 50, len(config.vocabs[treebank_name][XPOS]))
        self.feats_ffn = nn.Linear(self.xlmr_dim, len(config.vocabs[treebank_name][FEATS]))

        self.down_dim = self.xlmr_dim // 4
        self.down_project = nn.Linear(self.xlmr_dim, self.down_dim)
        # dependency parsing
        self.unlabeled = Deep_Biaffine(self.down_dim, self.down_dim,
                                       self.down_dim, 1)
        self.deprel = Deep_Biaffine(self.down_dim, self.down_dim,
                                    self.down_dim, len(config.vocabs[treebank_name][DEPREL]))
        # load pretrained weights
        self.initialized_weights = self.state_dict()
        language = treebank2lang[treebank_name]
        self.pretrained_tagger_weights = torch.load(os.path.join(self.config.cache_dir, language,
                                                                 '{}.tagger.mdl'.format(
                                                                     language)), map_location=self.config.device)['adapters']

        for name, value in self.pretrained_tagger_weights.items():
            if name in self.initialized_weights:
                self.initialized_weights[name] = value
        self.load_state_dict(self.initialized_weights)
        print('Loaded tagger for {}'.format(language))

    def predict(self, batch, word_reprs, cls_reprs):
        # upos
        upos_scores = self.upos_ffn(word_reprs)
        predicted_upos = torch.argmax(upos_scores, dim=2)
        # edits
        xpos_reprs = torch.cat(
            [word_reprs, self.upos_embedding(predicted_upos)], dim=2
        )  # [batch size, num words, xlmr dim + 50]
        # xpos
        xpos_scores = self.xpos_ffn(xpos_reprs)
        predicted_xpos = torch.argmax(xpos_scores, dim=2)
        # feats
        feats_scores = self.feats_ffn(word_reprs)
        predicted_feats = torch.argmax(feats_scores, dim=2)

        # head
        dep_reprs = torch.cat(
            [cls_reprs, word_reprs], dim=1
        )  # [batch size, 1 + max num words, xlmr dim] # cls serves as ROOT node
        dep_reprs = self.down_project(dep_reprs)
        unlabeled_scores = self.unlabeled(dep_reprs, dep_reprs).squeeze(3)

        diag = torch.eye(batch.head_idxs.size(-1) + 1, dtype=torch.bool).unsqueeze(0).to(self.config.device)
        unlabeled_scores.masked_fill_(diag, -float('inf'))

        # deprel
        deprel_scores = self.deprel(dep_reprs, dep_reprs)
        dep_preds = []
        dep_preds.append(F.log_softmax(unlabeled_scores, 2).detach().cpu().numpy())
        dep_preds.append(deprel_scores.max(3)[1].detach().cpu().numpy())
        return predicted_upos, predicted_xpos, predicted_feats, dep_preds


class TokenizerClassifier(nn.Module):
    def __init__(self, config, treebank_name):
        super().__init__()
        self.config = config
        self.xlmr_dim = 768
        self.tokenizer_ffn = nn.Linear(self.xlmr_dim, 5)

        language = treebank2lang[treebank_name]
        # load pretrained weights
        self.pretrained_tokenizer_weights = torch.load(os.path.join(self.config.cache_dir, language,
                                                                    '{}.tokenizer.mdl'.format(
                                                                        language)), map_location=self.config.device)['adapters']
        self.initialized_weights = self.state_dict()

        for name, value in self.pretrained_tokenizer_weights.items():
            if name in self.initialized_weights:
                self.initialized_weights[name] = value

        self.load_state_dict(self.initialized_weights)
        print('Loaded tokenizer for {}'.format(language))

    def predict(self, batch, wordpiece_reprs):
        wordpiece_scores = self.tokenizer_ffn(wordpiece_reprs)
        predicted_wordpiece_labels = torch.argmax(wordpiece_scores, dim=2)  # [batch size, num wordpieces]

        return predicted_wordpiece_labels, batch.wordpiece_ends, batch.paragraph_index

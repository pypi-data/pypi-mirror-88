from torch.utils.data import Dataset
from collections import namedtuple
from ..utils.base_utils import *
from ..utils.tbinfo import lang2nercorpus

# for sents
instance_fields = [
    'words', 'word_num',
    'piece_idxs', 'attention_masks', 'word_lens',
    'entity_label_idxs'
]

batch_fields = [
    'words', 'word_num', 'word_mask',
    'piece_idxs', 'attention_masks', 'word_lens',
    'entity_label_idxs'
]

Instance = namedtuple('Instance', field_names=instance_fields)

Batch = namedtuple('Batch', field_names=batch_fields)


class NERDatasetLive(Dataset):
    def __init__(self, config, tokenized_sentences):
        self.config = config
        self.tokenizer = config.wordpiece_splitter
        # load data
        self.data = [{'words': sentence} for sentence in tokenized_sentences]

        # load vocab
        self.vocabs = self.config.ner_vocabs[self.config.default_language]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def numberize(self):
        tokenizer = self.tokenizer
        data = []
        for inst in self.data:
            words = inst['words']
            # lowercase
            if self.config.lowercase:
                words = [w.lower() for w in words]
            # ---------------------
            pieces = [[p for p in tokenizer.tokenize(w) if p != '▁'] for w in words]
            for ps in pieces:
                if len(ps) == 0:
                    ps += ['-']
            word_lens = [len(x) for x in pieces]
            flat_pieces = [p for ps in pieces for p in ps]
            # Pad word pieces with special tokens
            piece_idxs = tokenizer.encode(
                flat_pieces,
                add_special_tokens=True,
                max_length=self.config.max_input_length,
                truncation=True
            )

            pad_num = self.config.max_input_length - len(piece_idxs)
            attn_masks = [1] * len(piece_idxs) + [0] * pad_num
            piece_idxs = piece_idxs + [0] * pad_num

            instance = Instance(
                words=inst['words'],
                word_num=len(inst['words']),
                piece_idxs=piece_idxs,
                attention_masks=attn_masks,
                word_lens=word_lens,
                entity_label_idxs=[0 for _ in inst['words']]
            )
            data.append(instance)
        self.data = data

    def collate_fn(self, batch):
        batch_words = [inst.words for inst in batch]
        batch_word_num = [inst.word_num for inst in batch]

        batch_piece_idxs = []
        batch_attention_masks = []
        batch_word_lens = []

        max_word_num = max(batch_word_num)
        batch_word_mask = []
        batch_entity_label_idxs = []

        for inst in batch:
            batch_piece_idxs.append(inst.piece_idxs)
            batch_attention_masks.append(inst.attention_masks)
            batch_word_lens.append(inst.word_lens)
            batch_word_mask.append([1] * inst.word_num + [0] * (max_word_num - inst.word_num))
            batch_entity_label_idxs.append(inst.entity_label_idxs +
                                           [0] * (max_word_num - inst.word_num))

        batch_piece_idxs = torch.cuda.LongTensor(batch_piece_idxs)
        batch_attention_masks = torch.cuda.FloatTensor(
            batch_attention_masks)
        batch_word_num = torch.cuda.LongTensor(batch_word_num)
        batch_word_mask = torch.cuda.LongTensor(batch_word_mask).eq(0)
        batch_entity_label_idxs = torch.cuda.LongTensor(batch_entity_label_idxs)

        return Batch(
            words=batch_words,
            word_num=batch_word_num,
            word_mask=batch_word_mask,
            piece_idxs=batch_piece_idxs,
            attention_masks=batch_attention_masks,
            word_lens=batch_word_lens,
            entity_label_idxs=batch_entity_label_idxs
        )

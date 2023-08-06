import os, sys
import torch

no_train_treebanks = ['UD_Estonian-EWT', 'UD_Galician-TreeGal',
                      'UD_Kazakh-KTB', 'UD_Kurmanji-MG',
                      'UD_Slovenian-SST',
                      'UD_Latin-Perseus']
os.system('mkdir -p saved_models')
trained_treebanks = os.listdir('../../ud-training/datasets/tagger/')

if len(sys.argv) == 2:
    trained_treebanks = [sys.argv[1]]
from utils.tbinfo import tbname2shorthand, tbname2training_id, treebank2lang, lang2nercorpus

nercorpus2path = {
    'CoNLL03-English': {
        'model': '../../ud-training/datasets/NER-datasets/CoNLL03/CoNLL03-English.model.mdl',
        'vocab': '../../ud-training/datasets/NER-datasets/CoNLL03/CoNLL03-English-tag-vocab.json'
    },
    'OntoNotes-Chinese': {
        'model': '../../ud-training/datasets/NER-datasets/OntoNotes-5.0/v4/chinese/OntoNotes-Chinese.model.mdl',
        'vocab': '../../ud-training/datasets/NER-datasets/OntoNotes-5.0/v4/chinese/OntoNotes-Chinese-tag-vocab.json',
    },
    'CoNLL02-Dutch': {
        'model': '../../ud-training/datasets/NER-datasets/CoNLL02/CoNLL02-Dutch.model.mdl',
        'vocab': '../../ud-training/datasets/NER-datasets/CoNLL02/CoNLL02-Dutch-tag-vocab.json'
    },
    'AQMAR': {
        'model': '../../ud-training/datasets/NER-datasets/AQMAR/AQMAR.model.mdl',
        'vocab': '../../ud-training/datasets/NER-datasets/AQMAR/AQMAR-tag-vocab.json',
    }
}


def copy_tagger_weights(input_ckpt, output_ckpt):
    name_mapping = {
        'unlabeled.scorer.W_bilin.weight': 'unlabeled.pairwise_weight',
        'unlabeled.W1.weight': 'unlabeled.ffn1.0.weight',
        'unlabeled.W1.bias': 'unlabeled.ffn1.0.bias',
        'unlabeled.W2.weight': 'unlabeled.ffn2.0.weight',
        'unlabeled.W2.bias': 'unlabeled.ffn2.0.bias',
        'deprel.scorer.W_bilin.weight': 'deprel.pairwise_weight',
        'deprel.W1.weight': 'deprel.ffn1.0.weight',
        'deprel.W1.bias': 'deprel.ffn1.0.bias',
        'deprel.W2.weight': 'deprel.ffn2.0.weight',
        'deprel.W2.bias': 'deprel.ffn2.0.bias'
    }
    pretrained_tagger_weights = torch.load(input_ckpt)
    new_weights = {
        'epoch': pretrained_tagger_weights['epoch'],
        'adapters': {}
    }
    for name, value in pretrained_tagger_weights['adapters'].items():
        if name.startswith('unlabeled') or name.startswith('deprel'):
            new_name = name_mapping.get(name, name)
            new_weights['adapters'][new_name] = value
        else:
            new_weights['adapters'][name] = value
    torch.save(new_weights, output_ckpt)


for tbname in trained_treebanks:
    tbname = tbname.rstrip('2')

    language = treebank2lang[tbname]
    os.system('mkdir -p saved_models/{}'.format(language))

    if tbname not in no_train_treebanks:

        os.system(
            'cp -a ../../ud-training/datasets/tokenize/{}/{}.best-tokenizer.mdl saved_models/{}/{}.tokenizer.mdl'.format(
                tbname,
                tbname,
                language, language))
        os.system(
            'cp -a ../../ud-training/datasets/tagger/{}/train.vocabs.json saved_models/{}/{}.vocabs.json'.format(
                tbname,
                language, language))

        copy_tagger_weights(
            input_ckpt='../../ud-training/datasets/tagger/{}/{}.best-tagger.mdl'.format(
                tbname,
                tbname),
            output_ckpt='saved_models/{}/{}.tagger.mdl'.format(
                language, language)
        )
        if tbname2training_id[tbname] % 2 == 1:
            os.system(
                'cp -a ../../ud-training/stanza_src/saved_models/mwt/{}_mwt_expander.pt saved_models/{}/{}_mwt_expander.pt'.format(
                    tbname2shorthand[tbname], language, language
                ))
        os.system(
            'cp -a ../../ud-training/stanza_src/saved_models/lemma/{}_lemmatizer.pt saved_models/{}/{}_lemmatizer.pt'.format(
                tbname2shorthand[tbname], language, language
            )
        )
        if language in lang2nercorpus:
            nercorpus = lang2nercorpus[language]
            # copy ner model
            os.system(
                'cp -a {} saved_models/{}/{}.ner.mdl'.format(nercorpus2path[nercorpus]['model'], language, language)
            )
            # copy vocab
            os.system(
                'cp -a {} saved_models/{}/{}.ner-vocab.json'.format(nercorpus2path[nercorpus]['vocab'], language,
                                                                    language)
            )
    else:
        os.system(
            'cp -a ../../ud-training/datasets/tokenize/{}2/{}2.best-tokenizer.mdl saved_models/{}/{}.tokenizer.mdl'.format(
                tbname,
                tbname,
                language, language))
        os.system(
            'cp -a ../../ud-training/datasets/tagger/{}2/train.vocabs.json saved_models/{}/{}.vocabs.json'.format(
                tbname,
                language, language))
        copy_tagger_weights(
            input_ckpt='../../ud-training/datasets/tagger/{}2/{}2.best-tagger.mdl'.format(
                tbname, tbname),
            output_ckpt='saved_models/{}/{}.tagger.mdl'.format(
                language, language)
        )
        if tbname2training_id[tbname] % 2 == 1:
            os.system(
                'cp -a ../../ud-training/stanza_src/saved_models/mwt/{}2_mwt_expander.pt saved_models/{}/{}_mwt_expander.pt'.format(
                    tbname2shorthand[tbname], language, language
                ))
        os.system(
            'cp -a ../../ud-training/stanza_src/saved_models/lemma/{}2_lemmatizer.pt saved_models/{}/{}_lemmatizer.pt'.format(
                tbname2shorthand[tbname], language, language
            )
        )

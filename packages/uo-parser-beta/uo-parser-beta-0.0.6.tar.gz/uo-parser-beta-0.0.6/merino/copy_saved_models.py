import os, sys
import torch

no_train_treebanks = ['UD_Estonian-EWT', 'UD_Galician-TreeGal',
                      'UD_Kazakh-KTB', 'UD_Kurmanji-MG',
                      'UD_Slovenian-SST',
                      'UD_Latin-Perseus']
os.system('mkdir -p resources/merino')
trained_treebanks = os.listdir('../../ud-training/datasets/tagger/')

if len(sys.argv) == 2:
    trained_treebanks = [sys.argv[1]]
from resources.tbinfo import tbname2shorthand, tbname2training_id, treebank2lang


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
    os.system('mkdir -p resources/merino/{}'.format(language))

    if tbname not in no_train_treebanks:

        os.system(
            'cp -a ../../ud-training/datasets/tokenize/{}/{}.best-tokenizer.mdl resources/merino/{}/{}.tokenizer.mdl'.format(
                tbname,
                tbname,
                language, language))
        os.system(
            'cp -a ../../ud-training/datasets/tagger/{}/train.vocabs.json resources/merino/{}/{}.vocabs.json'.format(
                tbname,
                language, language))

        copy_tagger_weights(
            input_ckpt='../../ud-training/datasets/tagger/{}/{}.best-tagger.mdl'.format(
                tbname,
                tbname),
            output_ckpt='resources/merino/{}/{}.tagger.mdl'.format(
                language, language)
        )
        if tbname2training_id[tbname] % 2 == 1:
            os.system(
                'cp -a ../../ud-training/stanza_src/saved_models/mwt/{}_mwt_expander.pt resources/merino/{}/{}_mwt_expander.pt'.format(
                    tbname2shorthand[tbname], language, language
                ))
        os.system(
            'cp -a ../../ud-training/stanza_src/saved_models/lemma/{}_lemmatizer.pt resources/merino/{}/{}_lemmatizer.pt'.format(
                tbname2shorthand[tbname], language, language
            )
        )
    else:
        os.system(
            'cp -a ../../ud-training/datasets/tokenize/{}2/{}2.best-tokenizer.mdl resources/merino/{}/{}.tokenizer.mdl'.format(
                tbname,
                tbname,
                language, language))
        os.system(
            'cp -a ../../ud-training/datasets/tagger/{}2/train.vocabs.json resources/merino/{}/{}.vocabs.json'.format(
                tbname,
                language, language))
        os.system(
            'cp -a ../../ud-training/datasets/tagger/{}2/{}2.best-tagger.mdl resources/merino/{}/{}.tagger.mdl'.format(
                tbname, tbname,
                language, language))
        copy_tagger_weights(
            input_ckpt='cp -a ../../ud-training/datasets/tagger/{}2/{}2.best-tagger.mdl'.format(
                tbname, tbname),
            output_ckpt='resources/merino/{}/{}.tagger.mdl'.format(
                language, language)
        )
        if tbname2training_id[tbname] % 2 == 1:
            os.system(
                'cp -a ../../ud-training/stanza_src/saved_models/mwt/{}2_mwt_expander.pt resources/merino/{}/{}_mwt_expander.pt'.format(
                    tbname2shorthand[tbname], language, language
                ))
        os.system(
            'cp -a ../../ud-training/stanza_src/saved_models/lemma/{}2_lemmatizer.pt resources/merino/{}/{}_lemmatizer.pt'.format(
                tbname2shorthand[tbname], language, language
            )
        )

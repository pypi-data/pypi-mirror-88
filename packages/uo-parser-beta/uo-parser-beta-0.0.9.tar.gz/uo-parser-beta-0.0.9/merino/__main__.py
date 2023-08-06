from .pipeline import Pipeline
from .pipeline import lang2treebank, tbname2training_id, treebank2lang
import sys, os

# evaluate pretrained pipelines
if len(sys.argv) < 4:
    print(
        'Not enough specified arguments! Please use the command, for example: python -m merino UD_English-EWT test.input-text.txt test.gold.conllu')

tbname = sys.argv[1]
input_fpath = sys.argv[2]
gold_conllu = sys.argv[3]
tblang = treebank2lang[tbname]

pretrained_pipeline = Pipeline(tblang)
pred_conllu = pretrained_pipeline.conllu_predict(input_fpath, tbname, tblang)
os.system("python merino/utils/conll18_ud_eval.py -v {} {}".format(gold_conllu, pred_conllu))

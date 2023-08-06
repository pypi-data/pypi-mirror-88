from .pipeline import Pipeline
from .pipeline import lang2treebank, tbname2training_id, treebank2lang
import sys, os
from time import time
from datetime import datetime

# evaluate pretrained pipelines
if len(sys.argv) < 4:
    print(
        'Not enough specified arguments! Please use the command, for example: python -m merino UD_English-EWT test.input-text.txt test.gold.conllu $device\nwhere $device=gpu or $device=cpu')

tbname = sys.argv[1]
input_fpath = sys.argv[2]
gold_conllu = sys.argv[3]
tblang = treebank2lang[tbname]

pretrained_pipeline = Pipeline(tblang)
start_time = time()
pred_conllu = pretrained_pipeline.conllu_predict(input_fpath)
print('{}: Done. Writing predictions to {}\nProcessing time: {} seconds'.format(datetime.now(), pred_conllu,
                                                                                time() - start_time))
os.system("python merino/utils/conll18_ud_eval.py -v {} {}".format(gold_conllu, pred_conllu))

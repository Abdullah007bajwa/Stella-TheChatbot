from .ML.logistic_regression import lr
from .ML.naive_bayes import nb
from .ML.svm import svc
from .ML.dnn import dnn
from .ML.rnn import rnn


def predict_gender(name):
    lr_p = lr(name)
    nb_p = nb(name)
    svm_p = svc(name)
    rnn_p = rnn(name)
    dnn_p = dnn(name)
    result = (lr_p + nb_p + svm_p + rnn_p + dnn_p)/5
    print(result)
    return 'male' if result <= 0.5 else 'female'

# print(predict_gender('ali'))
# print(predict_gender('maria'))

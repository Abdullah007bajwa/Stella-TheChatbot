from .logistic_regression import lr
from .naive_bayes import nb
from .svm import svc
from .dnn import dnn
from .rnn import rnn


def predict_gender(name):
    lr_p = lr(name)
    nb_p = nb(name)
    svm_p = svc(name)
    rnn_p = rnn(name)
    dnn_p = dnn(name)
    result = (lr_p + nb_p + svm_p + rnn_p + dnn_p)/5
    print(result)
    return 'male' if result <= 0.5 else 'female'

# print(predict_gender('maria'))
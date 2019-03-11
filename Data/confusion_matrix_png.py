# -*- coding: utf-8 -*-
from pylab import *

# 其中cm是计算好的混淆矩阵
# cm = confusion_matrix(test_label, predict_label)
# 比如上述这样产生cm
def ConfusionMatrixPng(cm,classlist):

    norm_conf = []
    for i in cm:
        a = 0
        tmp_arr = []
        a = sum(i, 0)
        for j in i:
            tmp_arr.append(float(j) / float(a))
        norm_conf.append(tmp_arr)
    fig = plt.figure()
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    res = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet,
                    interpolation='nearest')
    width = len(cm)
    height = len(cm[0])
    cb = fig.colorbar(res)
    alphabet = classlist
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    locs, labels = plt.xticks(range(width), alphabet[:width])
    for t in labels:
        t.set_rotation(90)
    # plt.xticks('orientation', 'vertical')
    # locs, labels = xticks([1,2,3,4], ['Frogs', 'Hogs', 'Bogs', 'Slogs'])
    # setp(alphabet, 'rotation', 'vertical')
    plt.yticks(range(height), alphabet[:height])
    plt.savefig('confusion_matrix.png', format='png')
    plt.show()

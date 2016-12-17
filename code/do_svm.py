from sklearn.svm import SVC
from process_data import get_data
import numpy as np
import decimal

if __name__=='__main__':
    train_set = get_data()
    tset_size = len(train_set)
    print(tset_size)
    #print(train_set[0])
    #print(train_set[1])
    #5折交叉验证
    for epoch in range(0,5):
        perm = np.random.permutation(tset_size)
        nb_train_set=[]
        nb_train_label=[]
        nb_test_set=[]
        nb_test_label=[]
        for i in range(0, int(4*tset_size/5)):
            tmp_vec = train_set[perm[i]-1]
            nb_train_set.append(tmp_vec[0:len(tmp_vec)-1])
            nb_train_label.append(tmp_vec[len(tmp_vec)-1])
        svclf = SVC(kernel = 'linear',decision_function_shape='ovo')#default with 'rbf'  
        svclf.fit(nb_train_set,nb_train_label)  

        
        for i in range(int(4*tset_size/5), int(tset_size)):
            tmp_vec = train_set[perm[i]]#train_set[1]
            nb_test_set.append(tmp_vec[0:len(tmp_vec)-1])
            nb_test_label.append(tmp_vec[len(tmp_vec)-1])
        ans_label = svclf.predict(nb_test_set)
        pred = list(map(lambda x,y : x==y, ans_label, nb_test_label))
        efficiency = sum(pred)/len(nb_test_set)
        print("epoch = ", epoch, ", efficiency = ", efficiency)


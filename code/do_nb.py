from process_data import get_data
import numpy as np
import decimal
from decimal import Decimal


def trainNB(train_set, train_label, y_type):
    train_size = len(train_set)
    x_type = len(train_set[0])
    #计算p(y=ci)
    Py = [0]*y_type
    sum_y = [1]*y_type#平滑,是否需要改成0.5或更小？
    #每一种y的各个x项(x为1)的和
    sum_y_x_1=[[1]*x_type for i in range(y_type)]
    #每一种y的各个x项(x为0)的和
    sum_y_x_0=[[1]*x_type for i in range(y_type)]
    Py_x_1 = [[0]*x_type for i in range(y_type)]
    Py_x_0 = [[0]*x_type for i in range(y_type)]#[[0]*x_type]*y_type
    for k in range(0, train_size):
        i = train_label[k]
        sum_y[i] += 1
        tmp_vec = train_set[k]
        for j in range(0,len(tmp_vec)):
            if tmp_vec[j]==1:
                sum_y_x_1[i][j]+=1
            else:
                sum_y_x_0[i][j]+=1
        #break
    #print("sum_y[0]=",sum_y[0])  
    #print("sum_y_x_0[0]:",sum_y_x_0[0])
    for i in range(0, y_type):
        Py[i] = sum_y[i]/train_size
        for j in range(0, x_type):
            Py_x_1[i][j] = sum_y_x_1[i][j]/(sum_y[i]+1)#这里对应平滑项，sum_y[i]+2？看书里是怎么平滑的
            Py_x_0[i][j] = sum_y_x_0[i][j]/(sum_y[i]+1)
    print("py: ", Py)
    
    #Py_x[i][j]表示P(x=j|y=i)
    #Py[i]表示P(y=i)
    return Py_x_1, Py_x_0, Py

def testNB(Py_x_1, Py_x_0, Py, nb_test_set, nb_test_label, y_type):
    test_size = len(nb_test_set)
    x_type = len(nb_test_set[0])
    ans_label = []
    decimal.getcontext().prec = 30000
    print("test_set size: ", len(nb_test_set))
    print("nb_test_label: ", nb_test_label)
    for test_vec in nb_test_set:
        max_prob = Decimal('0')
        for y_label in range(0, y_type):
            prob = Decimal(Py[y_label])
            for i in range(0, x_type):
                if test_vec[i]==1:
                    prob = prob*Decimal(Py_x_1[y_label][i])
                else:
                    prob = prob*Decimal(Py_x_0[y_label][i])
            #print("prob=",prob)
            if prob > max_prob:
                max_prob = prob
                max_label = y_label
            #break
        ans_label.append(max_label)
    print("ans_label: ", ans_label)
    pred = list(map(lambda x,y : x==y, ans_label, nb_test_label))
    efficiency = sum(pred)/len(nb_test_set)
    
    return efficiency;

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
        Py_x_1, Py_x_0, Py = trainNB(nb_train_set, nb_train_label, 4)
        #print(Py_x_1[1]) 
        #print(Py_x_0[1])
        
        for i in range(int(4*tset_size/5), int(tset_size)):
            tmp_vec = train_set[perm[i]]#train_set[1]
            nb_test_set.append(tmp_vec[0:len(tmp_vec)-1])
            nb_test_label.append(tmp_vec[len(tmp_vec)-1])
        efficiency =  testNB(Py_x_1, Py_x_0, Py, nb_test_set, nb_test_label, 4)
        print("epoch = ", epoch, ", efficiency = ", efficiency)






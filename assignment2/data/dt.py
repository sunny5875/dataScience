
import sys
import numpy as np
import random


class Feature:
    def __init__(self, feature, i):
        self.featureName = feature
        self.featureValueList = []
        self.tag = i
    
    
    def __str__(self):
        return f"featureName: ({self.featureName})\t featureValueList: ({self.featureValueList})"
    
    def __iter__(self):
        return iter(self.featureValueList)

class Node:
    def __init__(self):
        self.feature = None #feature 종류, nonleaf이면 값이 있고 아니면 None임
        self.children = [] #child 노드
        self.class_label = None #leaf node일 때 class_label
        self.feature_value = None # 부모노드 feature에 의해 나눠질 때의 해당 feature value

    def append(self, newNode):
        self.next.append(newNode)

    
    def __repr__(self):
        return f"Node(feature: {self.feature}, class_label: {self.class_label}),childern: {self.children}), feature_value: {self.feature_value})"

    def dfs(self):
        print(self)
        for child in self.children :
            child.dfs()
    
    
    # evaluate entropy of dataset
    def calculate_before_entropy(self, class_labels, data_set):
        entropy = 0
        data_labels = np.array([])
        for item in data_set:
            data_labels = np.append(data_labels, item[-1])


        for label in class_labels:
            p_i = np.sum(data_labels==label)/data_labels.size
            if p_i==0:
                continue
            entropy += p_i*np.log2(p_i)
        return -entropy

    # evaluate entropy of splited dataset
    def calculate_after_entropy(self, class_labels, data_set, feature):
        entropy = 0
        attr_values = feature.featureValueList

        for attr in attr_values:
            data_subset = data_set[data_set.T[feature.tag]==attr]
            p_i = data_subset.shape[0]/data_set.shape[0]
            
            entropy += p_i*self.calculate_before_entropy(class_labels, data_subset)

        print("using feature ",feature.featureName," after entropy: ", entropy)
        return entropy
    
    def calculate_splitInfo(self, data_set, feature):
        entropy = 0
        attr_values = feature.featureValueList

        for attr in attr_values:
            data_subset = data_set[data_set.T[feature.tag]==attr]
            p_i = data_subset.shape[0]/data_set.shape[0]
            if p_i==0:
                continue
            entropy += p_i*np.log2(p_i)

        print("using feature ",feature.featureName," splitInfo: ", -entropy)
        return -entropy
    
    def majority_voting(self, class_labels, data_set):
        major_label = None
        max_cnt = 0
        data_labels = data_set.T[-1]
        for label in class_labels:
            cnt = np.sum(data_labels==label)
            if cnt > max_cnt:
                max_cnt = cnt
                major_label = label
        # return major_label, max_cnt/data_labels.size
        return major_label

    def fit(self, data_set, remainfeatureList, class_label):
        #split할지 말지 결정
        print("===== start", self, "=====")
        before_entropy = self.calculate_before_entropy(class_label, data_set)
        print("before entropy: ", before_entropy)
        
       
        if before_entropy == 0 or remainfeatureList.size == 0 :
            self.class_label = self.majority_voting(class_label, data_set)
            print("done")
            return


        max_feature = remainfeatureList[0]
        max_gain_ratio = sys.float_info.min
        
        for feature in remainfeatureList:
                info_gain = before_entropy - self.calculate_after_entropy(class_label, data_set, feature)
                split_info = self.calculate_splitInfo(data_set, feature)
                gain_ratio = info_gain / split_info
                if gain_ratio > max_gain_ratio:
                    max_gain_ratio = gain_ratio
                    max_feature = feature
        
        print("select the feature!: ", max_feature)
        self.feature = max_feature
        
        for feature_value in max_feature.featureValueList:
            data_subset = data_set[data_set.T[max_feature.tag]==feature_value]
            
            subset_ratio = data_subset.shape[0]/data_set.shape[0]

            new_remain_feature_list = np.delete(remainfeatureList, np.where(remainfeatureList == max_feature))
            new_leaf = Node()
            new_leaf.feature_value = feature_value

            if data_subset.size != 0:
                new_leaf.fit( data_subset, new_remain_feature_list ,class_label)
            else:
                new_leaf.class_label = random.choice(class_label.featureValueList)
            self.children.append(new_leaf)
            


    def predict(self, data):
        if self.feature == None:
            return self.class_label
        
        for i, item in enumerate(self.feature.featureValueList):
            if item == data[self.feature.tag]:
                return self.children[i].predict(data)

        
    
def read_train_file(file_name):
    f = open("./" + file_name,'r')


    read_feature_list = f.readline().split()
    feature_list = np.array([])
    for i, feature in enumerate(read_feature_list):
        feature_list = np.append(feature_list, np.array([Feature(feature, i )]))
    
    input_list = f.readlines()
    transaction_list = np.empty((0,feature_list.size))


    for input in input_list:
        item_set = np.array(input.strip().split('\t'))
        transaction_list = np.append(transaction_list,  np.array([item_set]), axis = 0)
    
        for i, item in enumerate(item_set):
            if item not in feature_list[i].featureValueList:
                feature_list[i].featureValueList.append(item)
    
    f.close()
    class_label = feature_list[-1]
    feature_list = feature_list[:-1]
    

    return feature_list, class_label, transaction_list


def create_output_file(output_file_name, test_file_name, feature_list, class_label):
    output_file = open(output_file_name, 'w')
    _, _, test_data = read_train_file(test_file_name)
    result = ""
    for item in feature_list:
        result += item.featureName+"\t"
    
    output_file.write(result + class_label.featureName + "\n")

    for data in test_data:
        result = ""
        for item in data:
            result += item+"\t"
        result += model.predict(data) +"\n"
        output_file.write(result)

    output_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("argv is not correct! please check argv one more time")
        quit()

    train_file_name = sys.argv[1]
    test_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    feature_list, class_label, transaction_list = read_train_file(train_file_name)

    print("===== initial feature list =====")
    for item in feature_list:
        print(item)
    print(class_label)
    print("===== initial transaction list =====")
    print(transaction_list)

    model = Node()
    model.fit( transaction_list, feature_list, class_label)
    # model.dfs()

    create_output_file(output_file_name, test_file_name, feature_list, class_label)
    
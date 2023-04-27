
import sys
import numpy as np



class Feature:
    def __init__(self, feature):
        self.featureName = feature
        self.featureValueList = []
        self.isValid = True
    
    def getFeatureValueList(self) :
        return self.featureValueList
    
    def setFeatureValueList(self, value) :
        self.featureValueList.append(value)
    
    def __str__(self):
        return f"featureName: ({self.featureName})\t featureValueList: ({self.featureValueList})"

class Node:
    def __init__(self, feat):
        self.feature = feat
        self.children = []
        self.class_label = None

    def append(self, newNode):
        self.next.append(newNode)

    def setFeature(self, feat):
        self.feature = feat

    def setClassLabel(self, result):
        self.class_label = result

    def getFeature(self):
        return self.feature

    def getNext(self, index):
        return self.children[index]

    def getClassLabel(self):
        return self.class_label
    
    
    # evaluate entropy of dataset
    def calculate_before_entropy(self, class_labels, data_set):
        entropy = 0
        data_labels = np.array([])
        for item in class_labels:
            data_labels.append(item[-1])

        for label in class_labels:
            p_i = np.sum(data_labels==label)/data_labels.size
            if p_i==0:
                continue
            entropy += p_i*np.log2(p_i)

        return -entropy

    # evaluate entropy of splited dataset
    def calculate_after_entropy(self, class_labels, data_set, attr_idx):
        entropy = 0
        attr_values = np.unique(data_set.T[attr_idx])

        for attr in attr_values:
            data_subset = data_set[data_set.T[attr_idx]==attr]
            p_i = data_subset.shape[0]/data_set.shape[0]
            entropy += p_i*self.calculate_before_entropy(class_labels, data_subset)

        return entropy
    
    def majority_voting(self, class_labels, data_set):
        major_label = None
        max_cnt = 0
        data_labels = data_set.T[-1]
        for label in class_labels:
            cnt = np.sum(data_labels==label)
            if cnt > max_cnt:
                max_cnt = cnt
                major_label = label

        return major_label, max_cnt/data_labels.size

    def fit(self, data_set, remainfeatureList, class_labels):
        before_entropy = self.calculate_before_entropy(class_labels, data_set)
        if before_entropy == 0:
            self.class_label = data_set[0][-1]
            return

        self.class_label, ratio = self.majority_voting(class_labels, data_set)
        if len(self.mask) == attributes.size - 1 or ratio > self.majority_threshold:
            return

        test_attr_idx = None
        max_info_gain = 0

        for attr_idx in range(attributes.size - 1):
            if attr_idx in self.mask:
                continue
            
            info_gain = self.calculate_before_entropy(class_labels, data_set) - self.calculate_after_entropy(class_labels, data_set, attr_idx)
            if info_gain > max_info_gain:
                max_info_gain = info_gain
                test_attr_idx = attr_idx
        

        self.feature = remainfeatureList[test_attr_idx]
        attr_values = np.unique(data_set.T[test_attr_idx])
        
        for attr in attr_values:
            data_subset = data_set[data_set.T[test_attr_idx]==attr]
            subset_ratio = data_subset.shape[0]/data_set.shape[0]
            if subset_ratio < self.pruning_threshold:
                continue
            new_leaf = Node(new_mask)

            new_leaf.fit(class_labels, data_subset)
            self.children[attr] = new_leaf
            


    def majorityVoting(dataSet):
        return 'majority'
        
    def predict(model) -> str:
        return 'unknown'

 


        
    
def read_train_file(file_name):
    f = open("./" + file_name,'r')

    transaction_list = []

    read_feature_list = f.readline().split()
    feature_list = []

    for feature in read_feature_list:
        feature_list.append(Feature(feature))
    
    input_list = f.readlines()

    for input in input_list:
        item_set = np.array(input.strip().split('\t'))
        transaction_list.append(item_set)
    
        for i, item in enumerate(item_set):
            if item not in feature_list[i].getFeatureValueList():
                feature_list[i].setFeatureValueList(item)
    
    f.close()
    
    return feature_list, transaction_list





if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("argv is not correct! please check argv one more time")
        quit()

    train_file_name = sys.argv[1]
    test_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    feature_list, transaction_list = read_train_file(train_file_name)

    print("===== initial feature list =====")
    for item in feature_list:
        print(item)
    print("===== initial transaction list =====")
    print(transaction_list)

    model = Node(feature_list)
    model.fit(model, transaction_list, feature_list)

    predict(model)

    # output_file = open(output_file_name, 'w')
    # output_file.write()
    # output_file.close()
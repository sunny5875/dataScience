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
    
    def getFeatureName(self):
        return self.featureName


# Decision Tree Class
class Node:
    def __init__(self, feature):
        self.children = {}
        self.feature = feature
        # self.attr_idx = None
        # self.mask = set()
        # self.mask.update(mask)
        self.class_label = None
        # self.majority_threshold = 0.8
        # self.pruning_threshold = 0.05
    
    def __repr__(self):
        return f"Node(feature: {self.feature}, class_label: {self.class_label})"

    def dfs(self):
        print(self)
        for child in self.children:
            child.dfs()

    def calculate_before_entropy(self, class_labels, data_set):
        entropy = 0
        data_labels = data_set.T[-1]
        print(data_labels)
        for label in class_labels:
            p_i = np.sum(data_labels==label)/data_labels.size
            print(p_i)
            if p_i==0:
                continue
            entropy += p_i*np.log2(p_i)

        return -entropy

    def calculate_after_entropy(self, class_labels, data_set, attr_idx):
        entropy = 0
        attr_values = np.unique(data_set.T[attr_idx])
        print(attr_values)

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

    def fit(self, feature_list, data_set):
        print("start fit")
        if self.calculate_before_entropy(feature_list, data_set) == 0:
            print("done")
            self.class_label = data_set[0][-1]
            return
        print("not done")
        self.class_label, ratio = self.majority_voting(feature_list, data_set)
        # if len(self.mask) == attributes.size - 1 or ratio > self.majority_threshold:
        #     return

        test_attr_idx = None
        max_info_gain = 0

        for attr_idx in range(attributes.size - 1):
            if attr_idx in self.mask:
                continue
            
            info_gain = self.calculate_before_entropy(feature_list, data_set) - self.calculate_after_entropy(feature_list, data_set, attr_idx)
            if info_gain > max_info_gain:
                max_info_gain = info_gain
                test_attr_idx = attr_idx
        

        attr_idx = test_attr_idx
        attr_values = np.unique(data_set.T[test_attr_idx])
        
        for attr in attr_values:
            data_subset = data_set[data_set.T[test_attr_idx]==attr]
            subset_ratio = data_subset.shape[0]/data_set.shape[0]
            # if subset_ratio < self.pruning_threshold:
            #     continue
            new_leaf = Node(new_mask)
            new_feature_list = feature_list
            new_feature_list[attr_idx].isValid = False

            new_leaf.fit(feature_list, data_subset)
            self.children[attr] = new_leaf

    def predict(self, data):
        if self.feature == None:
            return self.class_label
        
        attr = data[self.attr_idx]

        if not (attr in self.children):
            return self.class_label

        return self.children[attr].predict(data)


def input_training_set(filename):
    file = open(filename)
    
    read_feature_list = file.readline().split()
    feature_list = []

    for feature in read_feature_list:
        feature_list.append(Feature(feature))
        
    training_set = []

    while True:
        line = file.readline()
        if not line:
            break
        item_set = np.array(line.strip().split('\t'))
        training_set.append(item_set)
        for i, item in enumerate(item_set):
            if item not in feature_list[i].getFeatureValueList():
                feature_list[i].setFeatureValueList(item)
    
    training_set = np.array(training_set)
    file.close()
    
    return feature_list, training_set

def build_decision_tree(class_labels, training_set):
    decision_tree = Node(None)
    decision_tree.fit(class_labels, training_set)
    
    return decision_tree

def array_to_str(arr):
    result = ''
    for s in arr:
        result += s.getFeatureName()
        result += '\t'
    result = result[:-1]
    result += '\n'

    return result

def test_and_output(feature_list, decision_tree, test_filename, output_filename): 
    test_file = open(test_filename)
    output_file = open(output_filename, mode='w')

    test_file.readline()
    output_file.write(array_to_str(feature_list))

    while True:
        line = test_file.readline()
        if not line:
            break
        data = np.array(line.strip().split('\t'))

        class_label = decision_tree.predict(data)
        data = np.append(data, class_label)
        output_file.write(array_to_str(data))
    
    test_file.close()
    output_file.close()

def main(argv):
    if len(argv)<4:
        print('PLEASE, give 3 arguments (training filename, test filename, output filename)')
        return
    feature_list, transaction_list = input_training_set(argv[1])

    print("===== initial feature list =====")
    for item in feature_list:
        print(item)
    print("===== initial transaction list =====")
    print(transaction_list)
    
    # sys.setrecursionlimit(max(attributes.size*10, 10000))
    decision_tree = build_decision_tree(feature_list, transaction_list)
    decision_tree.dfs()
    # test_and_output(class_labels, decision_tree, argv[2], argv[3])

if __name__ == '__main__':
    main(sys.argv)
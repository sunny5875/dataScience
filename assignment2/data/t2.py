import sys
import time
import numpy as np

# Decision Tree Class
class DT:
    # Constructor
    # mask is set of already used attribute index
    def __init__(self, mask):
        self.child = {}
        self.attr_idx = None
        self.mask = set()
        self.mask.update(mask)
        self.class_label = None
        self.majority_threshold = 0.8
        self.pruning_threshold = 0.05

    # evaluate entropy of dataset
    def entropy_of(self, class_labels, data_set):
        entropy = 0
        data_labels = data_set.T[-1]
        for label in class_labels:
            p_i = np.sum(data_labels==label)/data_labels.size
            if p_i==0:
                continue
            entropy += p_i*np.log2(p_i)

        return -entropy

    # evaluate entropy of splited dataset
    def entropy_with_attr_of(self, class_labels, data_set, attr_idx):
        entropy = 0
        attr_values = np.unique(data_set.T[attr_idx])

        for attr in attr_values:
            data_subset = data_set[data_set.T[attr_idx]==attr]
            p_i = data_subset.shape[0]/data_set.shape[0]
            entropy += p_i*self.entropy_of(class_labels, data_subset)

        return entropy
    
    # majority voting
    # return major class label and its ratio
    def major_label_of(self, class_labels, data_set):
        major_label = None
        max_cnt = 0
        data_labels = data_set.T[-1]
        for label in class_labels:
            cnt = np.sum(data_labels==label)
            if cnt > max_cnt:
                max_cnt = cnt
                major_label = label

        return major_label, max_cnt/data_labels.size

    # construct Decision Tree recursively
    # pruning with majority_threshold and pruning_threshold
    def construct(self, attributes, class_labels, data_set):
        if self.entropy_of(class_labels, data_set) == 0:
            self.class_label = data_set[0][-1]
            return
        
        self.class_label, ratio = self.major_label_of(class_labels, data_set)
        if len(self.mask) == attributes.size - 1 or ratio > self.majority_threshold:
            return

        test_attr_idx = None
        max_info_gain = 0

        for attr_idx in range(attributes.size - 1):
            if attr_idx in self.mask:
                continue
            
            info_gain = self.entropy_of(class_labels, data_set) - self.entropy_with_attr_of(class_labels, data_set, attr_idx)
            if info_gain > max_info_gain:
                max_info_gain = info_gain
                test_attr_idx = attr_idx
        
        new_mask = set()
        new_mask.update(self.mask)
        new_mask.add(test_attr_idx)

        self.attr_idx = test_attr_idx
        attr_values = np.unique(data_set.T[test_attr_idx])
        
        for attr in attr_values:
            data_subset = data_set[data_set.T[test_attr_idx]==attr]
            subset_ratio = data_subset.shape[0]/data_set.shape[0]
            if subset_ratio < self.pruning_threshold:
                continue
            new_leaf = DT(new_mask)

            new_leaf.construct(attributes, class_labels, data_subset)
            self.child[attr] = new_leaf

    # predict unknown class label of given data
    def classify(self, data):
        if self.attr_idx == None:
            return self.class_label
        
        attr = data[self.attr_idx]

        if not (attr in self.child):
            return self.class_label

        return self.child[attr].classify(data)

# read input file
# Since DT algorithm in this source code is using vector operation with numpy,
# Dataset is parsed to numpy array
# To eliminate randomness, class labels are sorted
def input_training_set(filename):
    file = open(filename)
    
    attributes = np.array(file.readline().strip().split('\t'))
    class_labels = []
    training_set = []

    while True:
        line = file.readline()
        if not line:
            break
        data = np.array(line.strip().split('\t'))
        class_labels.append(data[-1])
        training_set.append(data)
    
    training_set = np.array(training_set)
    class_labels = np.unique(class_labels)
    class_labels.sort()
    file.close()
    
    return attributes, class_labels, training_set

# master Decision Tree Building Process
# using DT class, it returns a Decision Tree instance
def build_decision_tree(attributes, class_labels, training_set):
    decision_tree = DT(set())

    decision_tree.construct(attributes, class_labels, training_set)
    
    return decision_tree

# formatting function for numpy array with string
def array_to_str(arr):
    result = ''
    for s in arr:
        result += s
        result += '\t'
    result = result[:-1]
    result += '\n'

    return result

# read test file and write test result to output file
def test_and_output(attributes, decision_tree, test_filename, output_filename): 
    test_file = open(test_filename)
    output_file = open(output_filename, mode='w')

    test_file.readline()
    output_file.write(array_to_str(attributes))

    while True:
        line = test_file.readline()
        if not line:
            break
        data = np.array(line.strip().split('\t'))

        class_label = decision_tree.classify(data)
        data = np.append(data, class_label)
        output_file.write(array_to_str(data))
    
    test_file.close()
    output_file.close()



def main(argv):
    if len(argv)<4:
        print('PLEASE, give 3 arguments (training filename, test filename, output filename)')
        return
    attributes, class_labels, training_set = input_training_set(argv[1])
    
    sys.setrecursionlimit(max(attributes.size*10, 10000))
    train_start = time.time()
    decision_tree = build_decision_tree(attributes, class_labels, training_set)
    train_end = time.time()
    print('Building Time : %f sec' % (train_end-train_start))
    test_start = time.time()
    test_and_output(attributes, decision_tree, argv[2], argv[3])
    test_end = time.time()
    print('Testing Time : %f sec' % (test_end-test_start))

if __name__ == '__main__':
    main(sys.argv)
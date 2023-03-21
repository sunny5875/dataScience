import sys
#python3 apriori.py 3 input.txt output.txt


def count_item_set(item_set,transaction_list):
    cnt = 0
    for t in transaction_list:
        if item_set == set.intersection(item_set, t):
            cnt += 1
    return cnt


def apriori(transaction_list, total, min_sup):
    print("=== start apriori ===")
    #scan and find c1
    c1 = list()
    for item in transaction_list:
        for i in item:
                if set([i]) not in c1:
                    c1.append(set([i]))
    print(c1)
    #scan db and find l1
    l1 = list()
    for item in c1:
        if count_item_set(item, transaction_list)/total >= min_sup:
            l1.append(item)
    print(l1)
    #lk가 공집합이 될 때까지 반복
    # ck = []
    # lk = []
    print("=== end apriori ===")

    return l1

def findAssociationRule(list):
    print("=== start associationRule ===")

def read_input_file(file_name):
    f = open("./" + input_file_name,'r')
    input_list = f.readlines()
    total = len(input_list)

    print("==== input ====")
    transaction_list = []
    for input in input_list:
        line = input.replace("\n","").split('\t')
        print(set(map(int, line)))
        transaction_list.append(set(map(int, line)))
    
    f.close()
    
    return transaction_list, total

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("argv is not correct! please check argv one more time")
        quit()
        
    min_sup = int(sys.argv[1])
    min_sup = min_sup/100

    print(min_sup)

    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    #read file and return transaction list and total transaction
    transaction_list, total = read_input_file(input_file_name)

    # find freqeunt pattern
    frequent_pattern_set = apriori(transaction_list, total, min_sup)

    output_file = open(output_file_name, 'w')
    output_file.write("")

    output_file.close()
    

    
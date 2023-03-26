import sys
import itertools
#python3 apriori.py 3 input.txt output.txt

def read_input_file_and_get_c1(file_name):
    f = open("./" + input_file_name,'r')
    input_list = f.readlines()
    total = len(input_list)

    transaction_list = []
    c1 = []
    support_list = dict()

    for input in input_list:
        line = input.replace("\n","").split('\t')
        item_set = set(map(int, line))
        transaction_list.append(item_set)
        
        for item in item_set:
            temp_item = frozenset([item])
            if temp_item not in c1:
                c1.append(set([item]))
            if temp_item in support_list:
                support_list[temp_item] +=1
            else:
                support_list[temp_item] = 1


    f.close()
    
    return transaction_list, total, support_list, c1


def self_joining(l,k): #이게 제일 오래걸림
    result = list()
    for item in itertools.combinations(l, k):
        temp = set.union(*item)
        if len(temp) == k:
            result.append(temp)
    return result

      
# ck와 lk의 차로 pk 구하는 함수: pk는 self joining 후 pruning할 때 pruning하기 위해 저장하는 추가적인 변수
def difference(c,l):
    return  [s for s in c if s not in l]

def pruning_before_testing(c, p):
    return  [s for s in c if not any(s.issuperset(t) for t in p)]


def apriori(transaction_list, total, min_sup, support_list, c1):
    #scan db and find l1
    l1 = list()
    for item_set in c1:
        if support_list[frozenset(item_set)] >= min_sup * total:
                l1.append(item_set)
    p = difference(c1,l1)
    lk_1 = l1
    l = lk_1 
    k = 2
    while(True):
        if len(lk_1) == 0:
            break
        ck = self_joining(lk_1,k)
        ck = pruning_before_testing(ck,p)
        #testing 
        for item_set in transaction_list:
            for item in ck:
                temp_item = frozenset(item)
                if set(temp_item) <= set(item_set): 
                    if temp_item in support_list:
                        support_list[temp_item] += 1
                    else:
                        support_list[temp_item] = 1
                else:
                    if temp_item not in support_list:
                        support_list[temp_item] = 0

                    
        # find lk
        lk = []
        for item_set in ck:
            if support_list[frozenset(item_set)]>= min_sup * total:
                lk.append(item_set)
        pk = difference(ck,lk)
        p.extend(pk)
        lk_1 = lk
        l.extend(lk)
        k+= 1
    return l, support_list


def findAssociationRule(frequent_list, support_list, total):
    output = ""
    candidate_list = [s for s in frequent_list if len(s) >= 2]
    for candidate in candidate_list:
        for i in range(1,len(candidate)):
            for item_set_tuple in itertools.combinations(candidate, i):
                item_set = set(map(int, item_set_tuple)) #tuple이기에 set으로 변경
                associate_item_set = candidate.difference(item_set)
                # if len(associate_item_set) == 0:
                #     break
                support = support_list[frozenset(candidate)]/total * 100
                item_set_count = support_list[frozenset(item_set)]
                item_count = support_list[frozenset(candidate)]
                confidence = (item_count/item_set_count) * 100
                output += f"{set(item_set)}\t{set(associate_item_set)}\t"+str('%.2f' % round(support, 2))+"\t"+str('%.2f' % round(confidence, 2))+"\n"

    return output.rstrip("\n")



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("argv is not correct! please check argv one more time")
        quit()
        
    min_sup = int(sys.argv[1])
    min_sup = min_sup/100

    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    #read file and return transaction list and total transaction
    transaction_list, total, support_list, c1 = read_input_file_and_get_c1(input_file_name)

    # find freqeunt pattern
    frequent_pattern_set, support_list = apriori(transaction_list, total, min_sup, support_list, c1)
    result = findAssociationRule(frequent_pattern_set, support_list, total)

    output_file = open(output_file_name, 'w')
    output_file.write(result)
    output_file.close()

    

    
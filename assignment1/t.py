import sys
import itertools

def filtering(item_db, min_sup_cnt):
    frequent_set = {key: item_db[key] for key in item_db.keys() if item_db[key]>=min_sup_cnt}
    return frequent_set

def prune(candidate, prev_cnt, prev_list):
    for item in candidate:
        child_item = list(itertools.combinations(item, prev_cnt))
        chk = True
        for child in child_item:
            if child not in prev_list:
                chk = False
                break
        if chk == False:
            del candidate[candidate.index(item)]
    return candidate

def self_join(prev_items, cnt):
    sorted_prev_list = sorted(prev_items)
    candidate = []
    for a_set in sorted_prev_list:
        for b_set in sorted_prev_list:
            tmp_set = sorted(list(set().union(a_set, b_set)))
            if len(tmp_set) == cnt and tmp_set not in candidate:
                candidate.append(tmp_set)

    return prune(candidate, cnt-1, sorted_prev_list)

def apriori(total_item_db, min_sup_cnt, transaction):
    cnt = 2
    k_th = 1
    while True:
        candidate_item_db = self_join(total_item_db[k_th-1], cnt)
        if len(candidate_item_db)==0:
            break
        frequent_item_db = {} # 빈도수 저장
        for item_set in transaction:
            for item in candidate_item_db:
                tuple_item = tuple(item)
                if set(tuple_item) <= set(item_set): # candidate의 item이 transaction의 item set에 포함된다면
                    if tuple_item in frequent_item_db:
                        frequent_item_db[tuple_item] += 1
                    else:
                        frequent_item_db[tuple_item] = 1
        total_item_db.append(filtering(frequent_item_db, min_sup_cnt))
        cnt+=1
        k_th+=1

def association_rule(total_item_db, transaction_num):
    output = ""
    for i in range(1, len(total_item_db)):
        for item in total_item_db[i]:
            for size in range(1, i + 1):
                tmp_comb = list(itertools.combinations(item, size))
                for condition_item in tmp_comb:
                    result_item = list(item)
                    result_item = tuple([x for x in result_item if x not in condition_item])
                    support = (total_item_db[i][item]/transaction_num)*100
                    confidence = (total_item_db[i][item]/total_item_db[len(set(condition_item))-1][condition_item])*100
                    
                    output += f"{str(set(condition_item)).replace(' ', '')}\t{str(set(result_item)).replace(' ', '')}\t"+str('%.2f' % round(support, 2))+"\t"+str('%.2f' % round(confidence, 2))+"\n"
    return output.rstrip("\n")

if __name__ == "__main__":
    min_support = float(sys.argv[1])/100
    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    f = open(input_file_name, 'r')
    lines = f.readlines()

    first_item_db = {}
    total_item_db = []
    transaction = []

    for line in lines:
        items = line.replace("\n", "").split('\t') 
        item_set = list(map(int, items)) 
        transaction.append(item_set)
        for item in item_set:
            item = tuple([item]) 
            if item in first_item_db:
                first_item_db[item]+=1
            else:
                first_item_db[item]=1

    min_sup_cnt = min_support * len(transaction) 
    first_item_db = dict(sorted(first_item_db.items())) 
    total_item_db.append(filtering(first_item_db, min_sup_cnt))

    apriori(total_item_db, min_sup_cnt, transaction)

    output_file = open(output_file_name, 'w')
    output_file.write(association_rule(total_item_db, len(transaction)))

    f.close()
    output_file.close()
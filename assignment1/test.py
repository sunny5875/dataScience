
def check() :
    f = open("./output.txt",'r')
    input_list = f.readlines()
   

    f2 = open("./output2.txt",'r')
    input_list2 = f2.readlines()
   

    for line in input_list:
        if line not in input_list2:
            print("1: ",line)
            temp = line.split("\t")
            original = temp[2]+ "\t"+temp[3]
            for item in input_list2:
                if original in item:
                    print("2: ", item)
                    
            print("-------")

            




check()
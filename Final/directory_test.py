import os
from collections import defaultdict

result_list = defaultdict(list)
list_pointer = 0



def log_request(path, complete_flag):
    global list_pointer


    box = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as f:  # open in readonly mode
            i = 0
            j = 0
            local_result_list = []
            searchlines = f.readlines()
            image_path = searchlines[0].split(':')[0]
            predictions_num = int(searchlines[1]) - 1
            for i in range(predictions_num):
                box = searchlines[1 + 1 + i].split(',')
                i += 1
            for j in range(predictions_num):
                print(searchlines[2 + i + 1 + j])
                print(2 + i + 1 + j)
                local_result_list.append(str(searchlines[2 + i + 1 + j].split(':')[0]))
                if complete_flag:
                    if local_result_list[j] == 'fedex':
                        result_list[image_path].append("fedex")
                    elif local_result_list[j] == 'dhl':
                        result_list[image_path].append("dhl")
                    elif local_result_list[j] == 'ups':
                        result_list[image_path].append("ups")
                    elif local_result_list[j] == 'food delivery':
                        result_list[image_path].append("food")
                    list_pointer += 1
                else:

                    print(box)
                j += 1
        list_pointer += 1
        print(image_path)
        print(result_list)
            
    f.close()



log_request("/mnt/g/research/ECE-5725-group8/sample_out/",1)
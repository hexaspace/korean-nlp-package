import matplotlib.pyplot as plt
import csv
import os

# 10350
# 9000+1350
# 1350    once 1000~2350
# 2700    double 2000-4700
# 4050    triple 4950-9000,
# 5400    quadruple -3600 (2000~5600)
# 6750    quintuple 0~6750
# 8100    sextuple -900 5700~6600

# constant
CLASS_NUM = 10

# path 
current_path = os.getcwd()
os.chdir(current_path)

def csv2list(filepath):
    file = open(filepath, 'r')
    csvfile = csv.reader(file)
    data = []
    for row in csvfile:
        data.append(row)
    return data

# data
# ./data/evaluation_report_epoch5_learning0_002.csv
#evaluation_report_epoch5_batch_size_64.csv
# evaluation_report_sto2_10man_epoch20
#evaluation_report_sto2_10man_try2
# report_files = ["eval_triple", "eval_all"]  # 비교할 report file 명을 추가
report_files = ["sto2_10man_try2","sto2_10man_epoch20","epoch5_batch_size_64", "epoch5_learning0_002"]  # 비교할 report file 명을 추가
loc_tags = ['STO']    # 3가지 tag를 비교 , 'AFW', 'ORG'
f1_scores = {name: [] for name in loc_tags}
f1_array = []
for f_index in range(len(report_files)):    # report file 반복
<<<<<<< Updated upstream
    csv_data = csv2list(current_path + "report_files\\evaluation_report_"+report_files[f_index]+".csv") #file load
=======
    print("for")
    print(f1_scores)

    # csv_data = csv2list(current_path + "\\evaluation_report_"+report_files[f_index]+".csv") #file load
    csv_data = csv2list("./data/evaluation_report_"+report_files[f_index]+".csv")

>>>>>>> Stashed changes
    EVALUATION_NUM = len(csv_data) // (CLASS_NUM+1)
    last_score = (CLASS_NUM+1)*(EVALUATION_NUM-1)
    # f1_array.append()
    for idx, row in enumerate(csv_data[last_score:]):   # loc, afw, org data 추가
        if idx % (CLASS_NUM+1) == 0: #column names
            continue
        print(row)
        if row[0] in loc_tags:    # only related location tags
            _class_name = row[0]
            _f1_score = row[3]
            f1_scores[_class_name].append(float(_f1_score)) #-(f_index*0.1)
print(f1_scores)
# plot
t = len(loc_tags) # Number of dataset
d = len(report_files) # Number of sets of bars
w = 0.8 # Width of each bar
ax = plt.subplot()
for i in range(len(loc_tags)):
    n = i + 1
    store_x = [t * element + w * n for element in range(d)]
    plt.bar(store_x, f1_scores[loc_tags[i]])
    if (i == int(len(loc_tags)/2)): #중앙값 위치에 x축 이름 적기
        ax.set_xticks(store_x)
        ax.set_xticklabels(report_files)

plt.legend(loc_tags)
plt.title('evaluation compare - ner', fontsize = 20)

plt.show()




import matplotlib.pyplot as plt
import csv
import os

# constant
CLASS_NUM = 14

# path 
current_path = os.getcwd()
os.chdir(current_path)

# model
class F1Score:
    class_name = ""
    f1_score = []

    def __init__(self):
        self.f1_score = []

# functions
def create_F1Score(class_name, f1_score):
    f1_score = F1Score()
    f1_score.class_name = class_name
    f1_score.f1_score = f1_score
    return f1_score

def csv2list(filepath):
    file = open(filepath, 'r')
    csvfile = csv.reader(file)
    data = []
    for row in csvfile:
        data.append(row)
    return data

# data
csv_data = csv2list(current_path + "\\koBERT-NER-master\\evaluation_report.csv")
EVALUATION_NUM = len(csv_data) // (CLASS_NUM+1)
evalutation_iteration = [i for i in range(EVALUATION_NUM)]
class_names = [row[0] for row in csv_data[1:CLASS_NUM+1]]
# f1_scores = [create_F1Score(row[0], []) for row in csv_data[1:CLASS_NUM+1]]
f1_scores = {name: [] for name in class_names}

# update f1_scores
for idx, row in enumerate(csv_data):
    if idx % (CLASS_NUM+1) == 0: #column names
        continue

    _class_name = row[0]
    _precision = row[1]
    _recall = row[2]
    _f1_score = row[3]
    _spport = row[4]
    f1_scores[_class_name].append(float(_f1_score)) #f1_score column

# plot
plt.plot(evalutation_iteration, f1_scores['LOC'], marker='o', label = 'LOC')
plt.plot(evalutation_iteration, f1_scores['AFW'], marker='o', label = 'AFW')
plt.plot(evalutation_iteration, f1_scores['ORG'], marker='o', label = 'ORG')
plt.legend()
plt.title('evaluation - ner', fontsize = 20)
plt.axis([0, EVALUATION_NUM, 0,1 ])
plt.show()



'''
 file descriptions
  - sample_pred_in.txt   기본 테스트 데이터셋
  - output.txt           기본 테스트 데이터셋을 모델에 넣어서 얻은 결과
  - test_dataset.txt     재난문자 테스트 데이터셋
  - test_tag_dataset.txt test_dataset.txt의 각 문장을 올바르게 태깅한 데이터
  - test_output.txt      재난문자 테스트 데이터셋(test_dataset.txt)을 모델에 넣어서 얻은 결과
  - test_accuracy.py     모델의 테스트 결과 정확도 계산
'''
'''
 variable descriptions
  - true_positive   TRUE로 분류한 데이터 중 실제 TRUE인 개수
  - false_positive  TRUE로 분류한 데이터 중 실제 FALSE인 개수
  - true_negative   FALSE로 분류한 데이터 중 실제 FALSE인 개수
  - false_negative  FALSE로 분류한 데이터 중 실제 TRUE인 개수
'''
import os

# 실제 테스트데이터와 모델의 결과 데이터셋의 태그만 추출
def extract_tags(answer_file_path, output_file_path):
    answer_tags = []
    output_tags = []
    with open(answer_file_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if idx % 2 != 0:
                answer_tags.extend(line.split(' '))
            else: continue
        # print(answer_tags)

    with open(output_file_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if idx % 2 != 0:
                output_tags.extend(line.split(' '))
            else: continue
        # print(output_tags)

    return answer_tags, output_tags

# 정확도 계산 함수
def calculate_tag_accuracy(tag, output_tags, answer_tags):
    # 변수 선언
    true_positive, false_positive, true_negative, false_negative = 0, 0, 0, 0 # 정확도 계산에 필요한 변수들
    recall, precision, f1 = 0, 0, 0 # 정확도 결과

    accuracy_terms = {} # 계산한 변수들 저장
    accuracy = {} # recall, precision, f1 저장

    # 정답 데이터와 결과 데이터를 비교
    for output, answer in zip(output_tags, answer_tags):
        if (tag in output) and (tag in answer):
            true_positive += 1
        if (tag in output) and (tag not in answer):
            false_positive += 1
        if (tag not in output) and (tag in answer):
            false_negative += 1
        if (tag not in output) and (tag not in answer):
            true_negative += 1

    # 정확도 계산
    recall = true_positive / (true_positive + false_negative)
    precision = true_positive / (true_positive + false_positive)
    f1 = 2 * (precision * recall) / (precision + recall)

    # 결과 변수에 저장
    accuracy_terms['true_positive'] = true_positive
    accuracy_terms['false_positive'] = false_positive
    accuracy_terms['false_negative'] = false_negative
    accuracy_terms['true_negative'] = true_negative

    accuracy['recall'] = recall
    accuracy['precision'] = precision
    accuracy['f1'] = f1

    # 정확도 리턴
    return accuracy_terms, accuracy
    
if __name__ == "__main__":
    # 파일 경로 선언
    current_path = os.getcwd()
    root_path = current_path + '/deep_learning/test'
    answer_file_path = root_path + '/test_tag_dataset.txt'
    output_file_path = root_path + '/test_output.txt'

    answer_tags, output_tags = extract_tags(answer_file_path, output_file_path)
    _, accuacy = calculate_tag_accuracy('DAT', answer_tags, output_tags)
    print(accuacy)
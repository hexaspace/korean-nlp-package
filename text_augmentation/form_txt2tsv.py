### augmented data를 tsv로 확장자 변경
fwrite = open("./data/tsv_file/disasterSMS3_augmented.tsv", "w", encoding="utf-8")
file =  open("./data/disaster_augmented/output_disasterSMS3_augmented.txt", "r")
line = None
while line != "" :
    line = file.readline()
    fwrite.write(line)

file.close()
fwrite.close()
##### 기존 data와 재난문자 data 합치기 --  원격서버에서 실행할 것
# fwrite_loc = open("test_loc.tsv", "w", encoding="utf-8")
# fread_origin = open("test.tsv","r", encoding="utf-8")
# fread_loc1= open("test_loc_data.tsv", "r", encoding="utf-8")
# # fread_loc2= open("train_loc_data2.tsv", "r", encoding="utf-8")
# # fread_loc3 = open("train_loc_data3.tsv", "r", encoding="utf-8")
# #, encoding="utf-8" 'cp1252'
# for line in fread_origin:
#     fwrite_loc.write(line)
# for line in fread_loc1:
#     fwrite_loc.write(line)




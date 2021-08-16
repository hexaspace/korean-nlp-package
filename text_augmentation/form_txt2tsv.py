
# fwrite = open("./test_loc_data.tsv", "w", encoding="utf-8")
# file =  open("output_diasterSMS1_loc.txt", "r")
#
# ## output_disaster_loc파일을 \t -> \s, \n ->\t, 뷁 지우기
# line = None
# while line != "" :
#     line = file.readline().strip().replace("\t"," ")
#     tag = file.readline().replace("\t"," ").strip("\n")
#     dump = file.readline()
#     print(line +"\t"+ tag)
#     fwrite.write(line + "\t" + tag+"\n")
#
# file.close()
# fwrite.close()

fwrite_loc = open("test_loc.tsv", "w", encoding="utf-8")
fread_origin = open("test.tsv","r", encoding="utf-8")
fread_loc1= open("test_loc_data.tsv", "r", encoding="utf-8")
# fread_loc2= open("train_loc_data2.tsv", "r", encoding="utf-8")
# fread_loc3 = open("train_loc_data3.tsv", "r", encoding="utf-8")
#, encoding="utf-8" 'cp1252'
for line in fread_origin:
    fwrite_loc.write(line)
for line in fread_loc1:
    fwrite_loc.write(line)




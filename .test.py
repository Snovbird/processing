import os
# folder_path = r'C:\Users\matts\Downloads\test'
# print(list(os.walk(folder_path,topdown=False)))
# for root, dirs, files in os.walk(folder_path, topdown=False):
#     print(f"{root=}\n{dirs=}\n{files=}")
# [('C:\\Users\\matts\\Downloads\\test', ['t1', 't2'], []), 
#  ('C:\\Users\\matts\\Downloads\\test\\t1', ['sub1'], ['t1-A.txt']), 
#  ('C:\\Users\\matts\\Downloads\\test\\t1\\sub1', ['sub1sub1'], ['sub1-A1.txt', 'sub1-A2.txt']), 
#  ('C:\\Users\\matts\\Downloads\\test\\t1\\sub1\\sub1sub1', [], []), 
#  ('C:\\Users\\matts\\Downloads\\test\\t2', [], ['t1-A.txt'])]

# [('C:\\Users\\matts\\Downloads\\test\\t1\\sub1\\sub1sub1', [], []), 
# ('C:\\Users\\matts\\Downloads\\test\\t1\\sub1', ['sub1sub1'], ['sub1-A1.txt', 'sub1-A2.txt']), 
# ('C:\\Users\\matts\\Downloads\\test\\t1', ['sub1'], ['t1-A.txt']), 
# ('C:\\Users\\matts\\Downloads\\test\\t2', [], ['t1-A.txt']),
# ('C:\\Users\\matts\\Downloads\\test', ['t1', 't2'], [])]

for file in os.listdir(r'C:\Users\samahalabo\Desktop\5-clips\collected DS-'):
    if os.path.exists(os.path.join(r'C:\Users\samahalabo\Desktop\5-clips\collected DS-', file.replace("_","-"))):
        os.remove(os.path.join(r'C:\Users\samahalabo\Desktop\5-clips\collected DS-', file))
    else:
        os.rename(os.path.join(r'C:\Users\samahalabo\Desktop\5-clips\collected DS-', file), os.path.join(r'C:\Users\samahalabo\Desktop\5-clips\collected DS-', file.replace("_","-")))
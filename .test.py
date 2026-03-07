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

print(os.path.isdir('D:\\0-RECORDINGS\\New folder\\20251103'))
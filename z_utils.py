import datetime
import codecs
import os

#https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
def humanbytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)




#---------------------------------
# URL to File
def strToFile(content, title='NoTitle', ext='txt'):
    # Const
    constDateTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    constCharSet = 'UTF-8'
    constOutputFolder = './output_response/'

    # Folder Safe
    try:
        os.stat(constOutputFolder)
    except:
        os.makedirs(constOutputFolder)

    write_date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_full_path = constOutputFolder + title + '.' + write_date_time + '.' + ext

    f = codecs.open(file_full_path, 'w', constCharSet)
    f.write(content)
    f.close()
    print('Content To File Writed: ' + file_full_path)
    return

#---------------------------------
# File to Str
def fileToStr(filename):
    outStr = ""
    constCharSet = 'UTF-8'
    constOutputFolder = './output_response/'
    file_full_path = constOutputFolder + filename
    f = codecs.open(file_full_path, 'r', constCharSet)
    outStr = f.read()
    f.close()
    return outStr

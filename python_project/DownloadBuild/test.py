import filecmp
from subprocess import call
# print "%05d" % (1,)
# for i in range(1, 99, 1):
#     print "diff -rq ./%05d C:\\Users\\shuangh\\Desktop\\temp\\TelenavMapData\\map\\tiles\\%05d" % (i,i)
print "start"
#comparison = filecmp.dircmp('D:\\TelenavMapData', 'C:\\Users\\shuangh\\Desktop\\temp\\Denali_Here_17Q1_NA_201802132350.tar\\Denali_Here_17Q1_NA_201802132350\\TelenavMapData')
comparison = filecmp.dircmp('C:\\Users\\shuangh\\Desktop\\temp\\config_MY19', 'C:\\Users\\shuangh\\Desktop\\temp\\config_MY20')
#comparison.report_full_closure()
def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print "diff_file %s found in %s and %s" % (name, dcmp.left,
              dcmp.right)
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

#print_diff_files(comparison)

with open("R.java") as f:
    for line in f:
        start = line.find('=0x')
        end = line.find(';', start)
        if start > 0:
            hex_string = line[start + 1: end]
            integer = int(hex_string, 0)
            print '/*' + str(integer) + '*/'+ line,
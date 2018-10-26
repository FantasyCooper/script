import os
import shutil
from zipfile import ZipFile
from subprocess import call
import wget
from pip._vendor import requests
isMY21 = False
####################things to modify################################################
if isMY21:
    HMI = 'http://tar2.telenav.com/repository/telenav/HMI-Common/Denali/release/MY21_Denali_V142.3/5.0.142.3.14055/'
    SDK = 'http://tar2.telenav.com/repository/telenav/Common-Lib/SDK/4.1.13316/'
    RSI = 'http://tar2.telenav.com/repository/telenav/HMI-Common/RSI/release/MY21_Denali_V142.3/1.0.16734/'
#    git_work_path = 'C:\\Users\\shuangh\\Desktop\\Flash_tool_and_build\\telenav_21\\'
    git_work_path = '\\SHUANGH-X230\Users\shuangh\Desktop\Flash_tool_and_build\telenav_20'
    HMI_keys = [['href="denali-android-x86_64', '.apk', 'apps\\GMNav\\', 'apps\\GMNav\\Android.mk'], ['href="production-denali-x86_64', '.apk', 'apps\\GMNav\\', 'apps\\GMNav\\Android.mk'], ['href="denaliNavigationView-android', '.aar', 'libs\\NavigationView\\', 'libs\\Android.mk'], ['href="TelenavP13NBundle', '.jar', 'libs\\P13NBundle', 'libs\\Android.mk']]
    RSI_keys = [['href="rsi1-x86_64', '.apk', 'apps\\RSI\\', 'apps\\RSI\\Android.mk'], ['href="rsi2-x86_64', '.apk', 'apps\\RSI\\', 'apps\\RSI\\Android.mk']]
else:
    HMI = 'http://tar2.telenav.com/repository/telenav/Denali/HMI/RC/4.0.142.3.11866/Artifacts/'
    SDK = 'http://tar2.telenav.com/repository/telenav/Common-Lib/SDK/4.0.142.3.13323/'
#    git_work_path = 'C:\\Users\\shuangh\\Desktop\\Flash_tool_and_build\\telenav_20\\'
    git_work_path = 'Y:\\telenav_20'
    HMI_keys = [['href="denali-android-x86_64', '.apk', 'apps\\GMNav\\', 'apps\\GMNav\\Android.mk'], ['href="production-denali-x86_64', '.apk', 'apps\\GMNav\\', 'apps\\GMNav\\Android.mk'], ['href="navigationView-android', '.aar', 'libs\\NavigationView\\', 'libs\\Android.mk'], ['href="TelenavP13NBundle', '.jar', 'libs\\P13NBundle', 'libs\\Android.mk']]

###########################end modify###############################################
#MY20 80024 MY21 80023
HMI_keys_app_only = [['href="denali-android-x86_64', '.apk', 'apps\\GMNav\\', 'apps\\GMNav\\Android.mk'], ['href="production-denali-x86_64', '.apk', 'apps\\GMNav\\', 'apps\\GMNav\\Android.mk']]
SDK_keys = [['href="NavigationAPIHelper', '.jar', 'libs\\NavigationAPIHelper\\', 'libs\\Android.mk'], ['href="NavigationAPI-', '.zip', 'frameworks\\base\\location\\java\\', 'frameworks\\base\\location\\Android.mk']]
main_app_path = ''

def download_build(url, keys):
    r = requests.get(url)
    for key in keys:
        pos = r.content.find(key[0])
        end = r.content.find(key[1], pos)
        file_name = r.content[pos + 6 : end + len(key[1])]

        folder = git_work_path + key[2]
        file_full_path = os.path.join(folder, file_name)
        if file_full_path.find("denali-android-x86_64") > 0:
            main_app_path = file_full_path
        if key[1] == '.zip':
            if os.path.exists(folder):
                shutil.rmtree(folder)
            if not os.path.exists(folder):
                os.makedirs(folder)
            wget.download(url + file_name, file_full_path)
            zip = ZipFile(file_full_path, 'r')
            zip.extractall(folder)
            zip.close()
            os.remove(folder + file_name)
        else:
             for f in os.listdir(folder):
                if f.find(key[0][7 :]) > 0:
                    os.remove(os.path.join(folder, f))
                    wget.download(url + file_name, file_full_path)
                    new_text = ''
                    with open(os.path.join(git_work_path, key[3]),'rb') as mk_file:
                        new_text = mk_file.read().replace(str(f), file_name)
                    with open(os.path.join(git_work_path, key[3]), "wb") as mk_file:
                        mk_file.write(new_text)
        print(file_name + ' downloaded.')


print "start"
download_build(HMI, HMI_keys)
download_build(SDK, SDK_keys)
if isMY21:
    download_build(RSI, RSI_keys)
#    os.chdir("C:\\Users\\shuangh\\Desktop\\Flash_tool_and_build\\telenav_21\\libs\\common_libs")
#    call("jar","xvf", main_app_path, "libs\\x86_64\\")


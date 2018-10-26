import os

download_path = 'C:\\Users\\shuangh\\Desktop\\Flash_tool_and_build\\build_to_push\\'
git_path = 'C:\\Users\\shuangh\\Desktop\\Flash_tool_and_build\\MY20_git'
HMI_key_pairs = [['href="denali-android-x86_64', '.apk'], ['href="production-denali-x86_64', '.apk'], ['href="navigationView-android', '.aar'], ['href="TelenavP13NBundle', '.jar']]
SDK_key_pairs = [['href="NavigationAPIHelper', '.jar'], ['href="NavigationAPI-', '.zip']]


def update_git_folder():
    set = []
    for f in os.listdir(git_path):
        for key_pair in HMI_key_pairs:
            if(f.name.contains(key_pair[0])):
                set[key_pair[0]] = f.name



update_git_folder()
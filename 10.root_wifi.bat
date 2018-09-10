adb connect 192.168.5.1
adb wait-for-device
adb root
adb connect 192.168.5.1
adb wait-for-device
adb disable-verity
adb wait-for-device
adb remount

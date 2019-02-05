adb connect 192.168.1.100
adb wait-for-device
adb root
adb connect 192.168.1.100
adb wait-for-device
adb disable-verity
adb wait-for-device
adb remount

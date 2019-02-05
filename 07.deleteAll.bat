adb wait-for-device
adb root
adb wait-for-device
adb disable-verity
adb wait-for-device
adb remount
adb wait-for-device
adb shell rm /system/priv-app/denali/denali.apk
adb shell rm -rf /system/priv-app/denali/oat
adb shell rm /system/lib64/libAutoSDKJNI.so
adb shell rm /system/lib64/libGLEngineJNI.so
adb shell rm /system/lib64/libpl_droidsonroids_gif.so

adb shell rm /system/app/GMHomeScreen/GMHomeScreen.apk
adb shell rm -rf /system/app/GMHomeScreen/oat/
adb shell rm -rf /data/data/com.gm.gmhomescreen/
adb push ./resource/GMHomeScreen.apk /system/app/GMHomeScreen/GMHomeScreen.apk
 
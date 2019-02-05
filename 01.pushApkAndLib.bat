@echo off
for /f "delims=" %%a in ('wmic OS Get localdatetime  ^| find "."') do set dt=%%a
set datestamp=%dt:~0,8%
set timestamp=%dt:~8,6%
set YYYY=%dt:~0,4%
set MM=%dt:~4,2%
set DD=%dt:~6,2%
set HH=%dt:~8,2%
set Min=%dt:~10,2%
set Sec=%dt:~12,2%

set stamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%
echo stamp: "%stamp%"
echo datestamp: "%datestamp%"
echo timestamp: "%timestamp%"
@echo on
adb shell rm /system/priv-app/denali/denali.apk
adb shell rm -rf /system/priv-app/denali/oat
adb shell rm -rf /data/data/com.telenav.app.denali.na/
adb shell rm /data/dalvik-cache/x86_64/system@priv-app@denali@denali.apk@classes.dex
adb push ./denali.apk /system/priv-app/denali/

jar xvf denali.apk lib\
adb push ./lib/x86_64/libAutoSDKJNI.so /system/lib64/
adb push ./lib/x86_64/libGLEngineJNI.so /system/lib64/
adb push ./lib/x86_64/libpl_droidsonroids_gif.so /system/lib64/
adb push ./lib/x86_64/libc++_shared.so /system/vendor/lib64/
timeout 10
adb reboot
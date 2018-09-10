adb push ./resource/IDTA_P13N.calovride /cache/calibrations/
rem adb push ./resource/IDT3_P13N.calovride /cache/calibrations/
adb shell chmod 777 /cache/calibrations/*
adb shell setprop persist.gm.register.csm 111720110174777X
adb shell setprop persist.gm.register.cgm PJ13001PLYMTHPXR
adb shell setprop persist.gm.register.vin 1G6KG1112L101C7EE
adb shell setprop persist.auth.vin 1G6KG1112L101C7EE
adb shell am broadcast -a com.gm.android.action.REGISTRATION_START

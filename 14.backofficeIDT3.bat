rem adb push ./resource/IDTA_P13N.calovride /cache/calibrations/
adb push ./resource/IDT3_P13N.calovride /cache/calibrations/
adb shell chmod 777 /cache/calibrations/*
adb shell setprop persist.gm.register.csm CSM742JD63CUN014
adb shell setprop persist.gm.register.cgm CGM18NSU8536P014
adb shell setprop persist.gm.register.vin 1G6AU5S87J023DA78
adb shell setprop persist.auth.vin 1G6AU5S87J023DA78
adb shell am broadcast -a com.gm.android.action.REGISTRATION_START

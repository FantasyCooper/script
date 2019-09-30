import subprocess, datetime
import threading, time, os, re, sys
import traceback

try:
    package = sys.argv[1]
except:
#    package = "com.telenav.arp.navigationview.sample"
#    package = "com.gm.gmhomescreen"
    package = "com.telenav.app.denali.na"

for file_name in os.listdir("."):
    if re.match("logUSSPSS(\d+)\.txt", file_name) is not None or \
                    re.match("logNative(\d+)\.txt", file_name) is not None or \
                    re.match("logDalvik(\d+)\.txt", file_name) is not None or \
                    re.match("logOtherDev(\d+)\.txt", file_name) is not None or\
                    re.match("logSoMmap(\d+)\.txt", file_name) is not None or\
                    re.match("logDexMmap(\d+)\.txt", file_name) is not None or\
                    re.match("logEglMtrack(\d+)\.txt", file_name) is not None or\
                    re.match("logGlMtrack(\d+)\.txt", file_name) is not None or\
                    re.match("logUnknown(\d+)\.txt", file_name) is not None:
        os.remove(file_name)

script_start = time.clock()
crash_moment = 0
now = datetime.datetime.now()

fileName = str(now).replace('-', '').replace(' ', '').replace(':', '').split('.')[0]
fUSSPSS_name = 'logUSSPSS' + fileName + '.txt'
fNative_name = 'logNative' + fileName + '.txt'
fDalvik_name = 'logDalvik' + fileName + '.txt'
fOtherDev_name = 'logOtherDev' + fileName + '.txt'
fSoMmap_name = 'logSoMmap' + fileName + '.txt'
fDexMmap_name = 'logDexMmap' + fileName + '.txt'
fEglMtrack_name = 'logEglMtrack' + fileName + '.txt'
fGlMtrack_name = 'logGlMtrack' + fileName + '.txt'
fUnknown_name = 'logUnknown' + fileName + '.txt'


fUSSPSS = open(fUSSPSS_name, 'w')
fUSSPSS.write('                  Pss      Private  Private Swapped Heap    Heap      Heap\n')
fUSSPSS.write('                 Total     Dirty     Clean  Dirty   Size    Alloc     Free\n')
fUSSPSS.close()

fDalvik = open(fDalvik_name, 'w')
fDalvik.write('                  Pss      Private   Private Swapped Heap    Heap      Heap\n')
fDalvik.write('                 Total     Dirty      Clean  Dirty   Size    Alloc     Free\n')
fDalvik.close()

fNative = open(fNative_name, 'w')
fNative.write('                  Pss      Private   Private Swapped Heap    Heap      Heap\n')
fNative.write('                 Total     Dirty      Clean  Dirty   Size    Alloc     Free\n')
fNative.close()

fOtherDev = open(fOtherDev_name, 'w')
fOtherDev.write('                  Pss      Private   Private Swapped Heap    Heap      Heap\n')
fOtherDev.write('                 Total     Dirty      Clean  Dirty   Size    Alloc     Free\n')
fOtherDev.close()

fSoMmap = open(fSoMmap_name, 'w')
fSoMmap.write('                  Pss      Private   Private Swapped Heap    Heap      Heap\n')
fSoMmap.write('                 Total     Dirty      Clean  Dirty   Size    Alloc     Free\n')
fSoMmap.close()

fDexMmap = open(fDexMmap_name, 'w')
fDexMmap.write('                  Pss      Private   Private Swapped Heap    Heap      Heap\n')
fDexMmap.write('                 Total     Dirty      Clean  Dirty   Size    Alloc     Free\n')
fDexMmap.close()

fEglMtrack = open(fEglMtrack_name, 'w')
fEglMtrack.write('                  Pss      Private   Private Swapped Heap    Heap      Heap\n')
fEglMtrack.write('                 Total     Dirty      Clean  Dirty   Size    Alloc     Free\n')
fEglMtrack.close()

fGlMtrack = open(fGlMtrack_name, 'w')
fGlMtrack.write('                  Pss      Private   Private Swapped Heap    Heap      Heap\n')
fGlMtrack.write('                 Total     Dirty      Clean  Dirty   Size    Alloc     Free\n')
fGlMtrack.close()

fUnknown = open(fUnknown_name, 'w')
fUnknown.write('                  Pss      Private   Private Swapped Heap    Heap      Heap\n')
fUnknown.write('                 Total     Dirty      Clean  Dirty   Size    Alloc     Free\n')
fUnknown.close()


def run_cmd(cmd, output):
    print "cmd: " + cmd + ", output: " + output	
    global crash_moment
    thread_name = "Thread-" + str(threading.current_thread().ident)
    while True:
        try:
            start = time.clock()
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
            ret = p.communicate()[0]
	    try:	
            	p.kill()
	    except Exception, err:
		print ""
            end = time.clock()
            if ret == "":
                if end - script_start < 10:
                    print "APP [" + package + "] is not alive, please check!"
                    time.sleep(3)
                    continue
                else:
                    if crash_moment == 0:
                        crash_moment = end
                    if end - crash_moment < 3:
                        print "[Warning] APP seems crash, monitor will terminate after 3 seconds!"
                        continue
                    else:
                        print "Thread [" + output + "] has terminated!"
                        break
            line = ret.splitlines()[0] + "    " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	    print " ----- BEFORE ----- "  	
    	    print "line " + line
	    print " --------------- AFTER --------------- "  	
            os.system('echo \'' + line + '\' >>' + output)
            print "[" + thread_name + "]" + str(datetime.datetime.now()) + " " + str(output) + " is running ... " + \
                  "Current: " + str(round((end - start), 2)) + "| Total: " + str(round((end - script_start), 2)) + "\r\n"
            time.sleep(3)
        except Exception, e:
	    traceback.print_exc()	
            print e
            print "Execute command failed!"
            time.sleep(5)


threads = []
cmd1 = "adb shell dumpsys meminfo " + package + " | grep TOTAL"
cmd2 = "adb shell dumpsys meminfo " + package + " | grep 'Native Heap'"
cmd3 = "adb shell dumpsys meminfo " + package + " | grep 'Dalvik Heap'"
cmd4 = "adb shell dumpsys meminfo " + package + " | grep 'Other dev'"
cmd5 = "adb shell dumpsys meminfo " + package + " | grep '.so mmap'"
cmd6 = "adb shell dumpsys meminfo " + package + " | grep '.dex mmap'"
cmd7 = "adb shell dumpsys meminfo " + package + " | grep -w 'EGL mtrack'"
cmd8 = "adb shell dumpsys meminfo " + package + " | grep -w 'GL mtrack'"
cmd9 = "adb shell dumpsys meminfo " + package + " | grep 'Unknown'"

t1 = threading.Thread(target=run_cmd, args=(cmd1, fUSSPSS_name))
threads.append(t1)
t2 = threading.Thread(target=run_cmd, args=(cmd2, fNative_name))
threads.append(t2)
t3 = threading.Thread(target=run_cmd, args=(cmd3, fDalvik_name))
threads.append(t3)
t4 = threading.Thread(target=run_cmd, args=(cmd4, fOtherDev_name))
threads.append(t4)
t5 = threading.Thread(target=run_cmd, args=(cmd5, fSoMmap_name))
threads.append(t5)
t6 = threading.Thread(target=run_cmd, args=(cmd6, fDexMmap_name))
threads.append(t6)
t7 = threading.Thread(target=run_cmd, args=(cmd7, fEglMtrack_name))
threads.append(t7)
t8 = threading.Thread(target=run_cmd, args=(cmd8, fGlMtrack_name))
threads.append(t8)
t9 = threading.Thread(target=run_cmd, args=(cmd9, fUnknown_name))
threads.append(t9)

for t in threads:
    t.start()
t1.join()

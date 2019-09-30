import matplotlib
import datetime
import sys, os, re, math

matplotlib.use('Agg')
import matplotlib.pyplot as plt


def generateUssPss(fileUssPss, fileNative, fileDalvik, fileOtherDev,
                   fileSoMmap, fileDexMmap, fileEglMtrack, fileGlMtrack,
                   fileUnknown):
    with open(fileUssPss) as f:
        ussPsslLines = f.readlines()
    with open(fileNative) as f:
        nativeLines = f.readlines()
    with open(fileDalvik) as f:
        dalvikLines = f.readlines()
    with open(fileOtherDev) as f:
        otherDevLines = f.readlines()
    with open(fileSoMmap) as f:
        soMmapLines = f.readlines()
    with open(fileDexMmap) as f:
        dexMmapLines = f.readlines()
    with open(fileEglMtrack) as f:
        eglMtrackLines = f.readlines()
    with open(fileGlMtrack) as f:
        glMtrackLines = f.readlines()
    with open(fileUnknown) as f:
        unknownLines = f.readlines()

    total = 0
    if len(glMtrackLines) == 2 or len(eglMtrackLines) == 2:
        total = min(len(ussPsslLines), len(nativeLines), len(dalvikLines), len(otherDevLines),
                    len(soMmapLines), len(dexMmapLines), len(unknownLines))
    else:
        total = min(len(ussPsslLines), len(nativeLines), len(dalvikLines), len(otherDevLines),
                    len(soMmapLines), len(dexMmapLines), len(unknownLines), len(eglMtrackLines),
                    len(glMtrackLines))

    Y1 = []          #PSS
    Y2 = []          #USS
    Y3 = []          #Dalvik
    Y4 = []          #Native
    Y5 = []          #Other dev
    Y6 = []          #.so mmap
    Y7 = []          #.dex mmap
    Y8 = []          #unknown
    Y9 = []          #EGL mtrack
    Y10 = []         #GL mtrack

    duration1 = 0    #Dalvik
    duration2 = 0    #Native
    duration3 = 0    #PSS, USS
    duration4 = 0    #Other dev
    duration5 = 0    #.so mmap
    duration6 = 0    #.dex mmap
    duration7 = 0    #unknown
    duration8 = 0    #EGL mtrack
    duration9 = 0    #GL mtrack

    for index in range(total):
        ussPssLine = ussPsslLines[index]
        nativeLine = nativeLines[index]
        dalvikLine = dalvikLines[index]
        otherDevLine = otherDevLines[index]
        soMmapLine = soMmapLines[index]
        dexMmapLine = dexMmapLines[index]

        if len(glMtrackLines) > 2 and len(eglMtrackLines) > 2:
            eglMtrackLine = eglMtrackLines[index]
            glMtrackLine = glMtrackLines[index]
        unknownLine = unknownLines[index]

        if index <= 1:
            continue

        matchDalvik = re.match("^\s+Dalvik Heap\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\s.*)",
                               dalvikLine)
        if matchDalvik is not None:
            dalvik = matchDalvik.group(2)
            Y3.append(int(dalvik) / 1024)
            if index == 2:
                start_time = datetime.datetime.strptime(matchDalvik.group(8).strip(), '%Y-%m-%d %H:%M:%S')
            if index == total - 1:
                end_time = datetime.datetime.strptime(matchDalvik.group(8).strip(), '%Y-%m-%d %H:%M:%S')
                duration1 = (end_time - start_time).seconds

        matchNative = re.match("^\s+Native Heap\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\s.*)",
                               nativeLine)
        if matchNative is not None:
            native = matchNative.group(2)
            Y4.append(int(native) / 1024)
            if index == 2:
                start_time = datetime.datetime.strptime(matchNative.group(8).strip(), '%Y-%m-%d %H:%M:%S')
            if index == total - 1:
                end_time = datetime.datetime.strptime(matchNative.group(8).strip(), '%Y-%m-%d %H:%M:%S')
                duration2 = (end_time - start_time).seconds

        matchUssPss = re.match("^\s+TOTAL\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\s.*)", ussPssLine)
        if matchUssPss is not None:
            pss = matchUssPss.group(1)
            uss1 = matchUssPss.group(2)
            uss2 = matchUssPss.group(3)
            Y1.append(int(pss) / 1024)
            Y2.append((int(uss1) + int(uss2)) / 1024)
            if index == 2:
                start_time = datetime.datetime.strptime(matchUssPss.group(8).strip(), '%Y-%m-%d %H:%M:%S')
            if index == total - 1:
                end_time = datetime.datetime.strptime(matchUssPss.group(8).strip(), '%Y-%m-%d %H:%M:%S')
                duration3 = (end_time - start_time).seconds

        matchOtherDev = re.match("^\s+Other dev\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\s.*)",
                                    otherDevLine)
        if matchOtherDev is not None:
            otherDev = matchOtherDev.group(1)
            Y5.append(int(otherDev) / 1024)
            if index == 2:
                start_time = datetime.datetime.strptime(matchOtherDev.group(5).strip(), '%Y-%m-%d %H:%M:%S')
            if index == total - 1:
                end_time = datetime.datetime.strptime(matchOtherDev.group(5).strip(), '%Y-%m-%d %H:%M:%S')
                duration4 = (end_time - start_time).seconds

        matchSoMmap = re.match("^\s+.so mmap\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\s.*)",
                               soMmapLine)
        if matchSoMmap is not None:
            soMmap = matchSoMmap.group(1)
            Y6.append(int(soMmap) / 1024)
            if index == 2:
                start_time = datetime.datetime.strptime(matchSoMmap.group(5).strip(), '%Y-%m-%d %H:%M:%S')
            if index == total - 1:
                end_time = datetime.datetime.strptime(matchSoMmap.group(5).strip(), '%Y-%m-%d %H:%M:%S')
                duration5 = (end_time - start_time).seconds

        matchDexMmap = re.match("^\s+.dex mmap\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\s.*)",
                                dexMmapLine)
        if matchDexMmap is not None:
            dexMmap = matchDexMmap.group(1)
            Y7.append(int(dexMmap) / 1024)
            if index == 2:
                start_time = datetime.datetime.strptime(matchDexMmap.group(5).strip(), '%Y-%m-%d %H:%M:%S')
            if index == total - 1:
                end_time = datetime.datetime.strptime(matchDexMmap.group(5).strip(), '%Y-%m-%d %H:%M:%S')
                duration6 = (end_time - start_time).seconds

        matchUnknown = re.match("^\s+Unknown\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\s.*)",
                                unknownLine)
        if matchUnknown is not None:
            unknown = matchUnknown.group(2)
            Y8.append(int(unknown) / 1024)
            if index == 2:
                start_time = datetime.datetime.strptime(matchUnknown.group(5).strip(), '%Y-%m-%d %H:%M:%S')
            if index == total - 1:
                end_time = datetime.datetime.strptime(matchUnknown.group(5).strip(), '%Y-%m-%d %H:%M:%S')
                duration7 = (end_time - start_time).seconds

        if len(glMtrackLines) > 2 and len(eglMtrackLines) > 2:
            matchEglMtrack = re.match("^\s+EGL mtrack\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\s.*)",
                                      eglMtrackLine)
            if matchEglMtrack is not None:
                eglMtrack = matchEglMtrack.group(1)
                Y9.append(int(eglMtrack) / 1024)
                if index == 2:
                    start_time = datetime.datetime.strptime(matchEglMtrack.group(5).strip(), '%Y-%m-%d %H:%M:%S')
                if index == total - 1:
                    end_time = datetime.datetime.strptime(matchEglMtrack.group(5).strip(), '%Y-%m-%d %H:%M:%S')
                    duration8 = (end_time - start_time).seconds

            matchGlMtrack = re.match("^\s+GL mtrack\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\s.*)",
                                     glMtrackLine)
            if matchGlMtrack is not None:
                glMtrack = matchGlMtrack.group(1)
                Y10.append(int(glMtrack) / 1024)
                if index == 2:
                    start_time = datetime.datetime.strptime(matchGlMtrack.group(5).strip(), '%Y-%m-%d %H:%M:%S')
                if index == total - 1:
                    end_time = datetime.datetime.strptime(matchGlMtrack.group(5).strip(), '%Y-%m-%d %H:%M:%S')
                    duration9 = (end_time - start_time).seconds

    duration = max(duration1, duration2, duration3, duration4, duration5, duration6, duration7, duration8, duration9)

    minYLen = 0
    if len(Y9) == 0 or len(Y10) == 0:
        minYLen = min(len(Y1), len(Y2), len(Y3), len(Y4), len(Y5), len(Y6), len(Y7), len(Y8))
    else:
        minYLen = min(len(Y1), len(Y2), len(Y3), len(Y4), len(Y5), len(Y6), len(Y7), len(Y8), len(Y9), len(Y10))

    step = int(math.ceil(float(duration) / minYLen))
    X = range(0, step * minYLen, step)

    for i in range(0, len(X)):
        X[i] = float(X[i] / 60.0)

    Y1 = Y1[0:minYLen]
    Y2 = Y2[0:minYLen]
    Y3 = Y3[0:minYLen]
    Y4 = Y4[0:minYLen]
    Y5 = Y5[0:minYLen]
    Y6 = Y6[0:minYLen]
    Y7 = Y7[0:minYLen]
    Y8 = Y8[0:minYLen]

    if len(Y9) != 0 and len(Y10) != 0:
        Y9 = Y9[0:minYLen]
        Y10 = Y10[0:minYLen]

    total_Y1 = 0
    total_Y2 = 0
    total_Y3 = 0
    total_Y4 = 0
    total_Y5 = 0
    total_Y6 = 0
    total_Y7 = 0
    total_Y8 = 0
    total_Y9 = 0
    total_Y10 = 0

    for index in range(0, len(Y1)):
        total_Y1 += Y1[index]
    for index in range(0, len(Y2)):
        total_Y2 += Y2[index]
    for index in range(0, len(Y3)):
        total_Y3 += Y3[index]
    for index in range(0, len(Y4)):
        total_Y4 += Y4[index]
    for index in range(0, len(Y5)):
        total_Y5 += Y5[index]
    for index in range(0, len(Y6)):
        total_Y6 += Y6[index]
    for index in range(0, len(Y7)):
        total_Y7 += Y7[index]
    for index in range(0, len(Y8)):
        total_Y8 += Y8[index]
    for index in range(0, len(Y9)):
        total_Y9 += Y9[index]
    for index in range(0, len(Y10)):
        total_Y10 += Y10[index]

    avg_Y1 = total_Y1 / len(Y1)
    avg_Y2 = total_Y2 / len(Y2)
    avg_Y3 = total_Y3 / len(Y3)
    avg_Y4 = total_Y4 / len(Y4)
    avg_Y5 = total_Y5 / len(Y5)
    avg_Y6 = total_Y6 / len(Y6)
    avg_Y7 = total_Y7 / len(Y7)
    avg_Y8 = total_Y8 / len(Y8)

    if len(Y9) != 0 and len(Y10) != 0:
        avg_Y9 = total_Y9 / len(Y9)
        avg_Y10 = total_Y10 / len(Y10)
    Fig = plt.figure(figsize=(24, 8))  # Create a `figure' instance
    Ax = Fig.add_subplot(111)  # Create a `axes' instance in the figure
    Ax.plot(X, Y1, label="PSS")  # Create a Line2D instance in the axes
    Ax.plot(X, Y2, label="USS")
    Ax.plot(X, Y3, label="Dalvik")
    Ax.plot(X, Y4, label="Native")
    Ax.plot(X, Y5, label="Other dev")
    Ax.plot(X, Y6, label=".so mmap")
    Ax.plot(X, Y7, label=".dex mmap")
    Ax.plot(X, Y8, label="Unknown")

    if len(Y9) != 0 and len(Y10) != 0:
        Ax.plot(X, Y9, label="EGL mtrack")
        Ax.plot(X, Y10, label="GL mtrack")

    plt.xlabel("Time(Min)")
    plt.ylabel("Memory(M)")

    if len(Y9) != 0 and len(Y10) != 0:
        plt.title("Average: \n PSS: " + str(avg_Y1) + "M , " +
                  "USS: " + str(avg_Y2) + "M , " +
                  "Dalvik: " + str(avg_Y3) + "M , " +
                  "Native: " + str(avg_Y4) + "M \n" +
                  "Other dev: " + str(avg_Y5) + "M , " +
                  ".so mmap: " + str(avg_Y6) + "M , " +
                  ".dex mmap: " + str(avg_Y7) + "M , " +
                  "Unknown: " + str(avg_Y8) + "M \n" +
                  "EGL mtrack: " + str(avg_Y9) + "M , " +
                  "GL mtrack: " + str(avg_Y10) + "M")
    else:
        plt.title("Average: \n PSS: " + str(avg_Y1) + "M , " +
                  "USS: " + str(avg_Y2) + "M , " +
                  "Dalvik: " + str(avg_Y3) + "M , " +
                  "Native: " + str(avg_Y4) + "M \n" +
                  "Other dev: " + str(avg_Y5) + "M , " +
                  ".so mmap: " + str(avg_Y6) + "M , " +
                  ".dex mmap: " + str(avg_Y7) + "M , " +
                  "Unknown: " + str(avg_Y8) + "M")

    Ax.legend()
    plt.pause(0.1)
    Fig.savefig("Memory_Usage.png")

    # Fig1 = plt.figure(figsize=(24, 8))  # Create a `figure' instance
    # Ax1 = Fig1.add_subplot(111)  # Create a `axes' instance in the figure
    # Ax1.plot(X, Y5, label="$Dalvik Other$")
    # Ax1.plot(X, Y7, label="$.so mmap$")
    # Ax1.plot(X, Y8, label="$.apk mmap$")
    # Ax1.plot(X, Y9, label="$.dex mmap$")
    # Ax1.plot(X, Y10, label="$.oat mmap$")
    # Ax1.plot(X, Y11, label="$.art mmap$")
    # Ax1.plot(X, Y12, label="$Other mmap$")
    # Ax1.plot(X, Y15, label="$Unknown$")
    #
    # plt.xlabel("Time(Min)")
    # plt.ylabel("Memory(M)")
    # plt.title("Average Dalvik Other: " + str(avg_Y5) + "M , " +
    #           "Average .so mmap: " + str(avg_Y7) + "M , " +
    #           "Average .apk mmap: " + str(avg_Y8) + "M , " +
    #           "Average .dex mmap: " + str(avg_Y9) + "M \n, " +
    #           "Average .oat mmap: " + str(avg_Y10) + "M , " +
    #           "Average .art mmap: " + str(avg_Y11) + "M , " +
    #           "Average Other mmap: " + str(avg_Y12) + "M , " +
    #           "Average Unknown: " + str(avg_Y15) + "M")
    #
    # Ax1.legend()
    # Fig1.savefig("Memory_Usage_2.png")


if __name__ == "__main__":
    fileUssPss = None
    fileNative = None
    fileDalvik = None
    fileOtherDev = None
    fileSoMmap = None
    fileDexMmap = None
    fileEglMtrack = None
    fileGlMtrack = None
    fileUnknown = None

    for file_name in os.listdir("."):
        if re.match("logUSSPSS(\d+)\.txt", file_name) is not None:
            fileUssPss = file_name
        if re.match("logNative(\d+)\.txt", file_name) is not None:
            fileNative = file_name
        if re.match("logDalvik(\d+)\.txt", file_name) is not None:
            fileDalvik = file_name
        if re.match("logOtherDev(\d+)\.txt", file_name) is not None:
            fileOtherDev = file_name
        if re.match("logSoMmap(\d+)\.txt", file_name) is not None:
            fileSoMmap = file_name
        if re.match("logDexMmap(\d+)\.txt", file_name) is not None:
            fileDexMmap = file_name
        if re.match("logEglMtrack(\d+)\.txt", file_name) is not None:
            fileEglMtrack = file_name
        if re.match("logGlMtrack(\d+)\.txt", file_name) is not None:
            fileGlMtrack = file_name
        if re.match("logUnknown(\d+)\.txt", file_name) is not None:
            fileUnknown = file_name

    if fileUssPss is None or fileNative is None or fileDalvik is None or \
            fileOtherDev is None or fileSoMmap is None or \
            fileDexMmap is None or fileEglMtrack is None or \
            fileGlMtrack is None or fileUnknown is None:
        raise Exception("Incomplete log files!")

    generateUssPss(fileUssPss, fileNative, fileDalvik, fileOtherDev, fileSoMmap,
                   fileDexMmap, fileEglMtrack, fileGlMtrack, fileUnknown)

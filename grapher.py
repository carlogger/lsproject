import os
import time
import sys

# function borrowed from stack overflow
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

logDir = "logs/"
plotDir = "carlogger.github.io/"

os.chdir(logDir)
os.system("git pull")
os.chdir("..")

skipFiles = True
if len(sys.argv) > 1:
    skipFiles = sys.argv[1] != "--everything"

if not skipFiles:
    print("Not skipping files ...")

for i in range(1,10):
    logLists = listdir_nohidden(logDir + str(i))
    logLists = [ logFile[:-3] for logFile in logLists ]
    logLists = set(logLists)
    ungenPlots = logLists
    if skipFiles:
        plotLists = listdir_nohidden(plotDir + str(i))
        plotLists = [ plotFile[:-3] for plotFile in plotLists ]
        plotLists = set(plotLists)
        ungenPlots = logLists - plotLists # find files that haven't been plotted
    for data in ungenPlots:
        date = data[0:4] + "-" + data[4:6] + "-" + data[6:8] + " " + data[8:10] + ":" + data[10:12]
        logFile = logDir + str(i) + "/" + data + "csv"
        plotFile = plotDir + str(i) + "/" + data + "pdf"
        os.system(""" gnuplot -e "logFile='%s';plotFile='%s';date='%s'" plotscript.plg """ % (logFile, plotFile, date))

#import numpy as np
import PyGnuplot as pg
import os
import time

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
for i in range(1,10):
    logLists = listdir_nohidden(logDir + str(i))
    logLists = [ logFile[:-3] for logFile in logLists ]
    logLists = set(logLists)
    plotLists = listdir_nohidden(plotDir + str(i))
    plotLists = [ plotFile[:-3] for plotFile in plotLists ]
    plotLists = set(plotLists)
    ungenPlots = logLists - plotLists # find files that haven't been plotted
    for data in ungenPlots:
        date = data[0:4] + "-" + data[4:6] + "-" + data[6:8] + " " + data[8:10] + ":" + data[10:12]
        logFile = logDir + str(i) + "/" + data + "csv"
        plotFile = plotDir + str(i) + "/" + data + "pdf"
        pg.c('set datafile separator ","')
        pg.c('set key center top')
        pg.c("set term pdf enhanced size 20cm,20cm color solid font 'Inconsolata,12';")
        pg.c('set out "' + plotFile + '";')
        pg.c('set multiplot layout 3,2 title "' + date + '" font ",16"')
        pg.c('set xtics rotate')
        pg.c('set tics scale 0')
        pg.c('set xrange [0:]')
        pg.c('set yrange [0:]')
        
        pg.c('set title "Vehicle Speed"; set xlabel "time (s)"; set ylabel "speed (mph)"')
        pg.c('unset key')
        pg.c('set yrange [0:90]')
        pg.c("plot '" + logFile + "' u 1:2 w l")

        pg.c('set title "Engine Speed"; set xlabel "time (s)"; set ylabel "speed (rpm)"')
        pg.c('unset key')
        pg.c('set yrange [0:5000]')
        pg.c("plot '" + logFile + "' u 1:3 w l")

        pg.c('set title "Coolant and Intake Temps"; set xlabel "time (s)"; set ylabel "temperature (F)"')
        pg.c('set key right bottom')
        pg.c('set yrange [0:200]')
        pg.c("plot '" + logFile + "' u 1:4 w l t 'coolant', '" + logFile + "' u 1:7 w l t 'intake'")
        # pg.c("plot '" + logFile + "' u 1:7 w l t 'intake'")

        pg.c('set title "Mass Air Flow"; set xlabel "time (s)"; set ylabel "air flow (g/s)"')
        pg.c('unset key')
        pg.c('set yrange [0:60]')
        pg.c("plot '" + logFile + "' u 1:5 w l")

        pg.c('set title "Engine Load"; set xlabel "time (s)"; set ylabel "load (percentage)"')
        pg.c('unset key')
        pg.c('set yrange [0:100]')
        pg.c("plot '" + logFile + "' u 1:6 w l")

        pg.c('set title "Instant Gas Mileage"; set xlabel "time (s)"; set ylabel "mileage (mpg)"')
        pg.c('unset key')
        pg.c('set yrange [0:110]')
        pg.c("plot '" + logFile + "' u 1:($6 == 0 ? 110 : $5 == 0 ? NaN : 13 * $2 / $5) w l")
        
        # pg.pdf(plotDir + str(i) + "/" + data + "pdf")
        pg.c('reset')
        pg.c('unset multiplot')


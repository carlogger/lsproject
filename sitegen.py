#!/usr/bin/python3
import os

plotDir = "carlogger.github.io/"

# function borrowed from stack overflow
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

header = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Car Data Archives</title>
<link href="https://fonts.googleapis.com/css?family=Roboto:300&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Orbitron:400,700" rel="stylesheet">
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<div id="banner">
<h1>Car Data Archives</h1>
</div>
"""

content = ""

footer = """
</body>
</html>
"""

cars = [
    "2006 VW Jetta TDI",
    "Car 2",
    "Car 3",
    "Car 4",
    "Car 5",
    "Car 6",
    "Car 7",
    "Car 8",
    "Car 9"
    ]

for i in range(1,10):
    content += "<h2>" + cars[i-1] + "</h2>"
    plotLists = listdir_nohidden("carlogger.github.io/" + str(i))
    plotLists = sorted(plotLists)
    for plot in plotLists:
        date = plot[0:4] + "-" + plot[4:6] + "-" + plot[6:8] + " " + plot[8:10] + ":" + plot[10:12]
        content += "<a href='"
        content += str(i) + "/" + plot
        content += "'>"
        content += date
        content += "</a><br />"

f = open(plotDir + "index.html", "w")
f.write(header+content+footer)
f.close()

os.chdir(plotDir)
os.system("git add .")
os.system("git commit -m 'auto-commit'")
os.system("git push origin master")

        

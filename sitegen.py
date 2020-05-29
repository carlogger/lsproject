#!/usr/bin/python3
import os

plotDir = "carlogger.github.io/"

# function borrowed from stack overflow
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

header = """
<html>
<head>
<title>Car Data Archives</title>
</head>
<body>
<h1>Car Data Archives</h1>
<hr />
"""

content = ""

footer = """
</body>
</html>
"""

for i in range(1,10):
    content += "<h2>Car " + str(i) + "</h2>"
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

        

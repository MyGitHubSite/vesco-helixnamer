#!/usr/bin/env python3

HX_MODELCATALOG = "/Applications/Line6/HX Edit.app/Contents/Resources/HX_ModelCatalog.json"
HX_CONTROLS = "/Applications/Line6/HX Edit.app/Contents/Resources/HelixControls.json"
PGE_MODELCATALOG = "/Applications/Line6/POD Go Edit.app/Contents/Resources/PGModelCatalog.json"
PGE_CONTROLS = "/Applications/Line6/POD Go Edit.app/Contents/Resources/PGControls.json"
DATA_MODEL_CATALOG = "modelcatalog.dat"
DATA_CONTROLS = "controls.dat"

# TODO: turn this into an enum or something cooler if I ever learn Python
MODE_NAME = "#!NAME"
MODE_SHORTNAME = "#!SHORT_NAME"
MODE_RAWSTRING = "#!RAW_STRING"

if __name__ != "__main__":
    print("wat")
    exit(1)

def doReplace(origText, withText, inFileName, mode):
    import subprocess
    origText = fixChars(origText)
    withText = fixChars(withText)
    if mode == MODE_NAME:
        origText = f'"name":"{origText}"'
        withText = f'"name":"{withText}"'
    if mode == MODE_SHORTNAME:
        origText = f'"shortName": "{origText}"'
        withText = f'"shortName": "{withText}"'
    if mode == MODE_RAWSTRING:
        origText = f'"{origText}"'
        withText = f'"{withText}"'
    replacementExpr = f's/{origText}/{withText}/g'
    print(f'mapping: {replacementExpr} in {inFileName}')
    subprocess.call(["sed", "-i", ".bak", replacementExpr, inFileName])

def fixChars(textToFix):
    textToFix = textToFix.replace("/", "\/")
    textToFix = textToFix.replace("&", "\&")
    textToFix = textToFix.replace('"', '\\\\"')
    textToFix = textToFix.replace('®', '')
    return textToFix

def showRealNames(inJsonFile, withDataFrom):
    # The raw names file has alternating lines in pairs where where the first line
    # is the "Line 6 Name" (like Kinky Boost) and the second line is the "real"
    # name (like Xotic EP Booster).
    # Lines that start with '#' are comments.
    name_file_raw = open(withDataFrom)

    # Once both are collected, a `sed` takes place and the vars are cleared.
    sixName = ""
    realName = ""
    currentMode = MODE_NAME
    for line in name_file_raw.readlines():
        line = line.strip()
        if line.startswith("#!"):
            currentMode = line
            print(f'NOW USING MODE {currentMode}')
            continue
        if line.startswith('#'):
            print(line)
            continue
        if sixName == "":
            sixName = line
            continue
        if realName == "":
            if line != "Line 6 Original":
                realName = line
                doReplace(origText = sixName, withText = realName, inFileName = inJsonFile, mode = currentMode)
            sixName = ""
            realName = ""

showRealNames(inJsonFile = HX_MODELCATALOG, withDataFrom = DATA_MODEL_CATALOG)
showRealNames(inJsonFile = HX_CONTROLS, withDataFrom = DATA_CONTROLS)

showRealNames(inJsonFile = PGE_MODELCATALOG, withDataFrom = DATA_MODEL_CATALOG)
showRealNames(inJsonFile = PGE_CONTROLS, withDataFrom = DATA_CONTROLS)

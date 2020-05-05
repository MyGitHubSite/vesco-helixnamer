#!/usr/bin/env python3

APP_ROOT = "/Applications/Line6"

HX_ROOT = f'{APP_ROOT}/HX Edit.app/Contents/Resources'
HX_CATALOG_NAME = 'HX_ModelCatalog.json'
HX_CONTROL_NAME = 'HelixControls.json'
HX_MODELCATALOG = f'{HX_ROOT}/{HX_CATALOG_NAME}'
HX_CONTROLS = f'{HX_ROOT}/{HX_CONTROL_NAME}'

PG_ROOT = f'{APP_ROOT}/POD Go Edit.app/Contents/Resources'
PG_CATALOG_NAME = 'PGModelCatalog.json'
PG_CONTROL_NAME = 'PGControls.json'
PG_MODELCATALOG = f'{PG_ROOT}/{PG_CATALOG_NAME}'
PG_CONTROLS = f'{PG_ROOT}/{PG_CONTROL_NAME}'

DATA_MODEL_CATALOG = "modelcatalog.dat"
DATA_CONTROLS = "controls.dat"

# TODO: turn this into an enum or something cooler if I ever learn Python
MODE_NAME = "#!NAME"
MODE_SHORTNAME = "#!SHORT_NAME"
MODE_RAWSTRING = "#!RAW_STRING"

from enum import Enum
class Editor(Enum):
    HxEdit = 1
    PgEdit = 2

if __name__ != "__main__":
    print("wat")
    exit(1)

################################################################################
# CLI args
import argparse
parser = argparse.ArgumentParser(description='HX Edit and POD Go Edit model re-namer')
parser.add_argument('-v', action='store_true', help='verbose logging at DEBUG level if not overridden by LOGLEVEL env var')
parser.add_argument('--dryrun', action='store_true', help='does all the logging and parsing, but no actual replacements')
parser.add_argument('--reset', action='store_true', help='resets the names back to the Line 6 defaults')
args = vars(parser.parse_args())

################################################################################
# logging setup
import logging
import os
log = logging.getLogger(__name__)
defaultLevel = "DEBUG" if args['v'] else "INFO"
logging.basicConfig(level=os.environ.get("LOGLEVEL", defaultLevel), format='%(levelname)8s: %(message)s')

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
    log.debug('mapping: %s in %s', replacementExpr, inFileName)
    if not args['dryrun']:
        subprocess.call(["sed", "-i", ".bak", replacementExpr, inFileName])

def fixChars(textToFix):
    textToFix = textToFix.replace("/", "\/")
    textToFix = textToFix.replace("&", "\&")
    textToFix = textToFix.replace('"', '\\\\"')
    textToFix = textToFix.replace('®', '')
    return textToFix

def showRealNames(inJsonFile, withDataFrom, forEditor):
    # The raw names file has alternating lines in pairs where where the first line
    # is the "Line 6 Name" (like Kinky Boost) and the second line is the "real"
    # name (like Xotic EP Booster).
    # Lines that start with '#' are comments.
    name_file_raw = open(withDataFrom)

    # Once both are collected, a `sed` takes place and the vars are cleared.
    doHx = True
    doPg = True
    sixName = ""
    realName = ""
    currentMode = MODE_NAME
    for line in name_file_raw.readlines():
        line = line.strip()
        # TODO: if line is HX_ON, HX_OFF, PG_ON, PG_OFF
        if line.startswith("#!HX_OFF"):
            doHx = False
            if forEditor is Editor.HxEdit:
                log.debug("Switching HX Edit OFF")
            continue
        elif line.startswith("#!HX_ON"):
            doHx = True
            if forEditor is Editor.HxEdit:
                log.debug("Switching HX Edit ON")
            continue
        elif line.startswith("#!PG_OFF"):
            doPg = False
            if forEditor is Editor.HxEdit:
                log.debug("Switching PG Edit OFF")
            continue
        elif line.startswith("#!PG_ON"):
            doPg = True
            if forEditor is Editor.HxEdit:
                log.debug("Switching PG Edit ON")
            continue
        elif line.startswith("#!"):
            currentMode = line
            log.debug('NOW USING MODE %s', currentMode)
            continue
        if line.startswith('#'):
            log.info(line)
            continue
        if forEditor is Editor.HxEdit and not doHx:
            continue
        if forEditor is Editor.PgEdit and not doPg:
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

if args['reset']:
    import subprocess
    log.info('resetting to default Line 6 names')

    subprocess.call(['cp', f'{APP_ROOT}/{HX_CATALOG_NAME}', HX_ROOT])
    subprocess.call(['cp', f'{APP_ROOT}/{HX_CONTROL_NAME}', HX_ROOT])
    subprocess.call(['cp', f'{APP_ROOT}/{PG_CATALOG_NAME}', PG_ROOT])
    subprocess.call(['cp', f'{APP_ROOT}/{PG_CONTROL_NAME}', PG_ROOT])

else:
    log.info('replacing strings')

    showRealNames(inJsonFile = HX_MODELCATALOG, withDataFrom = DATA_MODEL_CATALOG, forEditor=Editor.HxEdit)
    showRealNames(inJsonFile = HX_CONTROLS, withDataFrom = DATA_CONTROLS, forEditor=Editor.HxEdit)

    showRealNames(inJsonFile = PG_MODELCATALOG, withDataFrom = DATA_MODEL_CATALOG, forEditor=Editor.PgEdit)
    showRealNames(inJsonFile = PG_CONTROLS, withDataFrom = DATA_CONTROLS, forEditor=Editor.PgEdit)

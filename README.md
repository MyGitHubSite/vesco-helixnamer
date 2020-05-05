# Model Re-namer For Line 6 Edit Programs

A basic tool to edit the names shown in Line 6 HX Edit or Line 6 POD Go Edit.

# For the non-programmer...

If you are just here to get the files to mod your installation, then head over to
[this site](https://benvesco.com/store/line-6-edit-real-names-mod) for
instructions and download links:

[Instructions!](https://benvesco.com/store/line-6-edit-real-names-mod)

# For the programmer

* Do you love Python?
* Do you love to help?
* Do you want to contribute to this project?

## Here is how you can help

* Fork this repo and make a pull request with your cool ideas
* Get in touch with me to talk more!
  * On Facebook in the [Line 6 Helix Family User Group OFFICIAL and ORIGINAL](https://www.facebook.com/groups/line6helixusergroup/)
  * On YouTube by [commenting on this video](https://www.youtube.com/watch?v=P6Gd5LzjM3k)
* Possible contributions:
  * Instead of `sed`, parse the JSON into a dictionary and replace the exact
    elements. This would be much less likely to replace extra text, but would
    also be more fragile if L6 change the JSON schema.
  * Better data file format with easier or more tolerant data entry
  * Better data file format that an IDE would understand
  * Safer handling of more possible special characters
  * Directives that would be more tolerant of JSON space vs. no space between
    key and value and the `:` separator
  * Better detection of where the JSON files live instead of hard-coded paths
  * Ensure a pristine backup in the parent directory before doing any processing
  * Ability to run without requiring `sudo`
  * Windows compatibility?

## The .dat file format

### The files

* **controls.dat** describes replacements into `HelixControls.json` and
  `PGControls.json`
* **modelcatalog.dat** describes replacements into `HX_ModelCatalog.json` and
  `PGModelCatalog.json`

### Summary

* Alternating lines, fake name, real name, fake name, real name, etc. with one
  per line
* Any line starting with a `#!` is a directive (see below)
* Any line starting with a `#` is a comment and will be ignored
* Whitespace is trimmed from each line before processing (literally `.trim()`)

### Detail

This is a very basic file format based on ease of data entry. This is done by
copy/paste entire tables of information from the Line 6 manual PDF into the data
file. Most of the time the tables will paste alternating lines like:

```
fake name 1
real name 1
fake name 2
real name 2
fake name 3
real name 3
...
```

This example above is the core format for this file. Lines must alternate
starting with the fake name on the first line and the real name on the second
line. One per line.

Some of the PDF tables paste in a different format that looks like:

```
...
fake name 4 real name 4
fake name 5 real name 5
fake name 6 real name 6
...
```

In those cases, one must manually correct the error by splitting each line in
the correct place.

### Directives

Directives are instructions to control how the string replacements will be
formatted. Once given, a directive remains active until another directive is
encountered. A directive is any line that starts with `#!` and the currently
supported directives are listed here.

* `#!NAME` replaces by looking for JSON `"name":"The Name"`
* `#!SHORT_NAME` replaces by looking for JSON `"shortName": "The Name"`
* `#!RAW_STRING` replaces by looking for `"The Name"`
* `#!HX_OFF` stop processing replacements for HX Edit
* `#!HX_ON` resume processing replacements for HX Edit
* `#!PG_OFF` stop processing replacements for POD Go Edit
* `#!PG_ON` resume processing replacements for POD Go Edit

### Comments

All lines starting with `#` are comments (except for diretives, described
above). These lines are ignored and not considered data, but they do print out
as logging while the script is running.

## The processing script (Python)

### Summary

1. Read the `.dat` files, accruing pairs of fake and real names
2. Feed each accrued pair of fake, real names into a `sed` command
3. Loop until done

### Special characters

A number of fake or real model names include special characters that can break
the `sed` command being fed to the command line. There is an attempt made to
preserve these special chars in the real model names by escaping them before
running the `sed` command. There are probably more special characters or better
ways to handle this but they are currently being accounted for only as we run
into them and they cause a problem.

* `/` escape/preserve
* `&` escape/preserve
* `"` escape/preserve
* `®` removed

### Backups

The `sed` command is being run with the `-i` flag to make a backup, but this is
not an appropriate backup. The flag will overwrite the backup each time you run
the script. It is strongly recommended to fully back up your original JSON files
before running any code from this repository.

## RUN IT!!!

Basically, have Python 3 installed and:

```
sudo ./modelnames.py

# If you have copied your original JSON files into the parent 'Line 6' directory,
# you can reset to those original files with
sudo ./modelnames.py --reset

# --dryrun flag does everything except the actual text replacements
# -v flag for verbose (DEBUG) level logging
```

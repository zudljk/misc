#!/usr/bin/osascript


set rsyncTemplate to "/usr/local/bin/rsync --archive --verbose --delete-after --exclude .Doc* --exclude .fs* --exclude .Spot* --exclude .Trash* --exclude .Temp* --exclude Backup "

try
  tell application "Finder"
    set myDir to (container of (path to me))
    set targetDir to POSIX file "/Volumes/SeagateExp/Bilder"

    if myDir is equal to targetDir then
      set targetDir to POSIX file "/Volumes/SeagateUSB3/Bilder"
    end if

    #set progress description to "Bla"
    # ("Synchronizing " & myDir & " to " & targetDir)

    set years to folders of myDir
    set targetDir to POSIX path of targetDir
  end tell

set progress description to "Synchronizing ..."
set progress total steps to the length of years

set i to 1
repeat with yearDir in years
  tell application "Finder" to set n to (name of yearDir) as text
  tell application "Finder" to set f1 to POSIX path of (yearDir as alias)

  set rsyncCommand to rsyncTemplate & f1 & " " & targetDir & "/" & n
set progress additional description to n
#			do shell script rsyncCommand
delay 1
set progress completed steps to i
set i to i + 1
end repeat
on error e
display alert e
end try

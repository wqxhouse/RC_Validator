#!/bin/sh

# We use this shell script "RC.sh" to run the main Java class.  This 
# shell script is copied to a file called "RC" which is then named the
# same as the C++ executables.  The "RC.sh" file is used in case a grader
# deleted the "RC" file thinking it was an executable.

java RC $*

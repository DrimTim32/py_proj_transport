test.bat executes all tests
assuming there are two environment variables, python and python2
python is src to python.exe with python 3 version
python2 is src to python.exe with python 2 version

-nc
 with this switch script does not clean temporary files

user can specify what python version ( 2 or 3 ) will execute scripts, if not provided both are testing

Example:
test.bat 3 -nc
will test against python 3 and will not clean afterwards

test.bat 2
will test against python 2 and will clean temp files
@ECHO OFF

set @version=""
set @clean="yes"
:init
if "%1"=="2" goto lsetVersion
if "%1"=="3" goto lsetVersion
if "%1"=="-nc" goto lnoclean
if "%1"=="" goto start
goto lerror

:lsetVersion
set @version=%1
shift
goto init

:lnoclean
set @clean="no"
shift
goto init


:lerror
echo %0 usage error

:start
PowerShell.exe -file test.ps1 %@version% %@clean%
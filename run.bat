:: Go to bat file direcotry
cd %~dp0

:: Unzip ZIP to currant direcotry
7za x Task.zip

:: cd to Path of desired binary (Modifiable)
cd Task\Thor

:: clean
::cmd.exe /c cleaner.bat

:: Create output direcotry
if not exist "..\..\output\" mkdir ..\..\output

:: Run desired command (Modifiable)
:CheckOS
IF EXIST "%PROGRAMFILES(X86)%" (GOTO 64BIT) ELSE (GOTO 32BIT)

:64BIT
thor64-lite.exe --allhds --soft -c 15 --minmem 512 --verylowprio -a Filescan --nothordb --logfile ":hostname:_thor_:time:.txt" --jsonfile ":hostname:_thor_:time:.json" --csvfile ":hostname:_files_md5s.csv" --utc --rfc3339 --reduced --silent -e ..\..\output
GOTO END

:32BIT
thor-lite.exe --allhds --soft -c 15 --minmem 512 --verylowprio -a Filescan --nothordb --logfile ":hostname:_thor_:time:.txt" --jsonfile ":hostname:_thor_:time:.json" --csvfile ":hostname:_files_md5s.csv" --utc --rfc3339 --reduced --silent -e ..\..\output  
GOTO END

:END
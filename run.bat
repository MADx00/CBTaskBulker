:: Go to bat file direcotry
cd %~dp0

:: Unzip ZIP to currant direcotry
7za x Task.zip
cd Task\loki

:: clean
::cmd.exe /c cleaner.bat

:: Create output direcotry
if not exist "..\..\output\" mkdir ..\..\output

:: Run desired command
loki.exe --allhds --alldrives --noprocscan --dontwait --onlyrelevant --csv -l ..\..\output\loki-%computername%.csv
@Echo Off
Title 从coding云端更新 SS 配置文件
cd /d %~dp0
set BackDir=.
wget --ca-certificate=ca-bundle.crt -c https://coding.net/u/Alvin9999/p/ip/git/raw/master/ssconfig.txt
del ".\gui-config.json_backup"
ren ".\gui-config.json"  gui-config.json_backup
certutil -decode %~dp0ssconfig.txt %~dp0gui-config.json
del "%~dp0ssconfig.txt"
ECHO.&ECHO.已更新SS配置文件,请按任意键退出程序. &PAUSE >NUL 2>NUL
@Echo Off
Title 从GitHub云端更新 Agent 最新可用 IP
cd /d %~dp0
del ".\proxy.user.ini_backup"
ren ".\proxy.user.ini"  proxy.user.ini_backup
wget --ca-certificate=ca-bundle.crt -c https://raw.githubusercontent.com/Alvin9999/pac2/master/proxy.user.ini
ECHO.&ECHO.已更新完成最新可用IP,请按任意键退出程序. &PAUSE >NUL 2>NUL
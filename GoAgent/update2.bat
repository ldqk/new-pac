@Echo Off
Title 从OSC云端更新 Agent 最新可用 IP
cd /d %~dp0
del "..\Agent\proxy.user.ini_backup"
ren "..\Agent\proxy.user.ini"  proxy.user.ini_backup
wget --ca-certificate=ca-bundle.crt -c https://coding.net/u/Alvin9999/p/ip/git/raw/master/proxy.user.ini
ECHO.&ECHO.已更新完成最新可用IP,请按任意键退出程序. &PAUSE >NUL 2>NUL
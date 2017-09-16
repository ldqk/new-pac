@Echo Off
Title 从COD云端更新 GoProxy 最新可用 IP or 配置
cd /d %~dp0
del ".\gae.user.json_backup"
ren ".\gae.user.json"  gae.user.json_backup
wget --ca-certificate=ca-bundle.crt -c https://coding.net/u/Alvin9999/p/pac/git/raw/master/gae.user.json
ECHO.&ECHO.已更新完成最新可用IP,请按任意键退出,并重启翻墙程序. &PAUSE >NUL 2>NUL
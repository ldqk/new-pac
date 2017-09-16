@Echo Off
Title 从GitHub云端更新 SS 配置文件
cd /d %~dp0
del ".\gui-config.json_backup"
ren ".\gui-config.json"  gui-config.json_backup
wget --ca-certificate=ca-bundle.crt -c https://raw.githubusercontent.com/Alvin9999/pac2/master/ssconfig.txt
certutil -decode %~dp0ssconfig.txt %~dp0gui-config.json
ECHO.&ECHO.已更新SS配置文件,请按任意键退出,并重启翻墙程序. &PAUSE >NUL 2>NUL
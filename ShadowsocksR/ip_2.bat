@Echo Off
Title 从coding云端更新 SS 配置文件
cd /d %~dp0
del gui-config.json
wget --ca-certificate=ca-bundle.crt -c https://coding.net/u/Alvin9999/p/ip/git/raw/master/ssconfig.txt
certutil -decode ssconfig.txt gui-config.json
del ssconfig.txt
ECHO.&ECHO.已更新SSR配置文件,请按任意键退出,并重启程序. &PAUSE >NUL 2>NUL
@Echo Off
Title 从GitHub云端更新 SS 配置文件
cd /d %~dp0
del gui-config.json
wget --ca-certificate=ca-bundle.crt -c https://raw.githubusercontent.com/Alvin9999/pac2/master/ssconfig.txt
del ".\gui-config.json"
certutil -decode ssconfig.txt gui-config.json
del ssconfig.txt
pause
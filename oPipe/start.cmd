@echo off
if exist %WINDIR%\Microsoft.NET\Framework\v3.5 (start /b oPipe3.exe) else (start /b oPipe.exe)
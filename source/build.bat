del ..\release\*.* /s /f /q
rmdir ..\release\*.* /s /f /q
rmdir ..\release\ /s /q
mkdir ..\release

del build\*.* /s /f /q
rmdir build\*.* /s /f /q
rmdir build\ /s /q
mkdir build

set TCL_LIBRARY=C:\Users\fra\AppData\Local\Programs\Python\Python37\tcl\tcl8.6
set TK_LIBRARY=C:\Users\fra\AppData\Local\Programs\Python\Python37\tcl\tk8.6

Python.exe setup.py build

cd build
rename exe.win-amd64-3.7 AMOS-Demo(Win64)
cd "AMOS-Demo(Win64)"

del openvr_api.dll
del openvr_plugin.dll

cd ..
"C:\Program Files\7-Zip\7z.exe" a ..\..\release\AMOS-Demo(Win64).zip
"C:\Program Files\7-Zip\7z.exe" a ..\..\release\AMOS-Demo(Win64).zip ..\ad_coupon_AF_issue_06.jpg
"C:\Program Files\7-Zip\7z.exe" a ..\..\release\AMOS-Demo(Win64).zip ..\file_id.diz
"C:\Program Files\7-Zip\7z.exe" a ..\..\release\AMOS-Demo(Win64).zip ..\screenshot.png

pause
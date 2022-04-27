if not exist %3 (
   mkdir %3 
)

net user %1 %2 /add

if %ERRORLEVEL% EQU 0 (
    icacls %3 /setowner %1 /t /c
)

net share %1="%3" /UNLIMITED /GRANT:%1,FULL
icacls %3 /grant:r %1:(OI)(CI)F /t

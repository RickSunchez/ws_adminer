@REM 1 - username 2 - foldername 3 - sharename

net share %3="%2" /UNLIMITED /GRANT:%1,FULL
icacls %2 /grant:r %1:(OI)(CI)F /t
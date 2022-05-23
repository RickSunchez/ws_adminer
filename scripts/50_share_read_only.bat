@REM 1 - username 2 - foldername 3 - sharename

icacls %2 /deny %1:(OI)(CI)F /t
icacls %2 /setowner "admin" /t /c

@REM net share %3 /delete
@REM net share %3="%2" /UNLIMITED /GRANT:%1,READ
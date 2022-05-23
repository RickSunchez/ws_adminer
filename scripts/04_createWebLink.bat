@ECHO OFF

SET "PATH_TO_URL=%1.url"

(
    ECHO.[InternetShortcut]
    ECHO.URL=%2
)>%PATH_TO_URL%
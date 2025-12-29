@ECHO OFF

pushd %~dp0

if "%1" == "" goto help
if "%1" == "help" goto help
if "%1" == "html" goto html

:html
sphinx-build -b html source build/html
goto end

:help
echo.
echo Использование: make ^<command^>
echo.
echo Доступные команды:
echo   html      - создать HTML документацию
echo   help      - показать эту справку
echo.

:end
popd
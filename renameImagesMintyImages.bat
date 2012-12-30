@echo off
if /I [%1] == [] (
echo Usage: renameImagesMintyImages ^<"hat name"^> ["style"]
echo Quotes are required if hat or style names have spaces.
exit /b 1
)
set _hat=%~1

set _style=%~2
echo Pruning 0 byte files...
for %%A in (*.png) do if %%~zA==0 del /F /Q "%%A"
if /I [%2] NEQ [] ( call :_style & exit /b 0 ) else ( call :_nostyle & exit /b 0 )
exit /b 0

:_nostyle
rename "_0000_Layer-3.png" "Painted %_hat% UNPAINTED.png" 2>nul
:: non-team paints
rename "_0001_Layer-2.png" "Painted %_hat% 2D2D24.png" 2>nul
rename "_0002_Layer-1.png" "Painted %_hat% BCDDB3.png" 2>nul

:: Support for fast export script
rename "_Layer-3.png" "Painted %_hat% UNPAINTED.png" 2>nul
::non-team paints
rename "_Layer-2.png" "Painted %_hat% 2D2D24.png" 2>nul
rename "_Layer-1.png" "Painted %_hat% BCDDB3.png" 2>nul
echo.
echo [%_hat%] done.
goto :EOF

:_style
rename "_0000_Layer-3.png" "Painted %_hat% UNPAINTED %_style%.png" 2>nul
::non-team paints
rename "_0001_Layer-2.png" "Painted %_hat% 2D2D24 %_style%.png" 2>nul
rename "_0002_Layer-1.png" "Painted %_hat% BCDDB3 %_style%.png" 2>nul
:: Support for fast export script
rename "_Layer-3.png" "Painted %_hat% UNPAINTED %_style%.png" 2>nul
::non-team paints
rename "_Layer-2.png" "Painted %_hat% 2D2D24 %_style%.png" 2>nul
rename "_Layer-1.png" "Painted %_hat% BCDDB3 %_style%.png" 2>nul
echo.
echo [%_hat%] with style [%_style%] done.
goto :EOF
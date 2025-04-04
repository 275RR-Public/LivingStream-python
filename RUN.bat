@echo off
setlocal enabledelayedexpansion
echo Checking installation status...
findstr /C:"success" lib\install_status.txt >nul 2>&1
if !errorlevel! == 0 (
    echo Successful app installation detected.
    call .venv\Scripts\activate
    echo Running app.py in virtual environment...
    .venv\Scripts\python.exe app.py
    pause
) else (
    echo No app installation detected.
    echo Running install.py...
    python lib\install.py
    set install_error=!errorlevel!
    if !install_error! == 0 (
        echo Successful installation completed.
        call .venv\Scripts\activate
        echo Running app.py in virtual environment...
        .venv\Scripts\python.exe app.py
        pause
    ) else (
        echo Installation failed with error code !install_error!
        echo Please check the error messages above.
        pause
    )
)
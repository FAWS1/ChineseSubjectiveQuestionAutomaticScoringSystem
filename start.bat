@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
color 0A
title 中文主观题评分系统启动器

:: 创建日志文件
set "LOG_FILE=%~dp0startup_log.txt"
echo 启动时间: %date% %time% > "%LOG_FILE%"
echo 系统启动日志 >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo ===================================
echo 正在启动中文主观题评分系统...
echo ===================================
echo.
echo 启动信息已记录到 %LOG_FILE%
echo.

echo 检查系统环境... >> "%LOG_FILE%"

echo ===================================

echo 检查Python环境...
echo 检查Python环境... >> "%LOG_FILE%"
python --version 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到Python环境，请安装Python并确保已添加到PATH中。
    echo [错误] 未检测到Python环境，请安装Python并确保已添加到PATH中。 >> "%LOG_FILE%"
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 1
)
echo Python环境检测成功！
echo Python环境检测成功！ >> "%LOG_FILE%"
echo.

echo 检查Node.js环境...
echo 检查Node.js环境... >> "%LOG_FILE%"
node --version 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到Node.js环境，请安装Node.js并确保已添加到PATH中。
    echo [错误] 未检测到Node.js环境，请安装Node.js并确保已添加到PATH中。 >> "%LOG_FILE%"
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 1
)
echo Node.js环境检测成功！
echo Node.js环境检测成功！ >> "%LOG_FILE%"
echo.

:: 检查目录结构
echo 检查项目目录结构... >> "%LOG_FILE%"
if not exist "%~dp0backend\" (
    echo [错误] 未找到后端目录，请确保目录结构完整。
    echo [错误] 未找到后端目录，请确保目录结构完整。 >> "%LOG_FILE%"
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

if not exist "%~dp0frontend\" (
    echo [错误] 未找到前端目录，请确保目录结构完整。
    echo [错误] 未找到前端目录，请确保目录结构完整。 >> "%LOG_FILE%"
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

echo 目录结构检查完成！ >> "%LOG_FILE%"

echo 检查后端依赖...
echo 检查后端依赖... >> "%LOG_FILE%"
cd /d "%~dp0backend"
if not exist requirements.txt (
    echo [错误] 未找到后端依赖文件 requirements.txt
    echo [错误] 未找到后端依赖文件 requirements.txt >> "%LOG_FILE%"
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

pip list | findstr "Django" >nul
set DJANGO_INSTALLED=%ERRORLEVEL%
if %DJANGO_INSTALLED% NEQ 0 (
    echo 正在安装后端依赖...
    echo 正在安装后端依赖... >> "%LOG_FILE%"
    echo.
    python -m pip install -r requirements.txt > "%~dp0backend_install.log" 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [错误] 安装后端依赖失败，请检查网络连接或手动安装。
        echo [错误] 安装后端依赖失败，详细信息请查看 backend_install.log >> "%LOG_FILE%"
        echo.
        echo 详细错误信息已保存到 %~dp0backend_install.log
        echo 按任意键退出...
        pause >nul
        exit /b 1
    )
    echo 后端依赖安装成功！
    echo 后端依赖安装成功！ >> "%LOG_FILE%"
    echo.
) else (
    echo 后端依赖已安装！
    echo 后端依赖已安装！ >> "%LOG_FILE%"
    echo.
)

echo 检查前端依赖...
echo 检查前端依赖... >> "%LOG_FILE%"
cd /d "%~dp0frontend"
if not exist package.json (
    echo [错误] 未找到前端依赖文件 package.json
    echo [错误] 未找到前端依赖文件 package.json >> "%LOG_FILE%"
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

if not exist node_modules (
    echo 正在安装前端依赖...
    echo 正在安装前端依赖... >> "%LOG_FILE%"
    echo.
    npm install > "%~dp0frontend_install.log" 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [错误] 安装前端依赖失败，请检查网络连接或手动安装。
        echo [错误] 安装前端依赖失败，详细信息请查看 frontend_install.log >> "%LOG_FILE%"
        echo.
        echo 详细错误信息已保存到 %~dp0frontend_install.log
        echo 按任意键退出...
        pause >nul
        exit /b 1
    )
    echo 前端依赖安装成功！
    echo 前端依赖安装成功！ >> "%LOG_FILE%"
    echo.
) else (
    echo 前端依赖已安装！
    echo 前端依赖已安装！ >> "%LOG_FILE%"
    echo.
)

echo 前端环境检测成功！
echo 前端环境检测成功！ >> "%LOG_FILE%"
echo.

echo ===================================
echo 启动后端服务器...
echo ===================================
echo 启动后端服务器... >> "%LOG_FILE%"

:: 检查后端服务器是否已经在运行
netstat -ano | findstr ":8000" >nul
if %ERRORLEVEL% EQU 0 (
    echo [警告] 端口8000已被占用，可能是后端服务器已经在运行。
    echo [警告] 端口8000已被占用，可能是后端服务器已经在运行。 >> "%LOG_FILE%"
    echo 继续启动可能会导致冲突。
    echo.
    set /p CONTINUE_CHOICE=是否继续启动？(Y/N): 
    if /i "!CONTINUE_CHOICE!" NEQ "Y" (
        echo 用户选择退出。 >> "%LOG_FILE%"
        echo 按任意键退出...
        pause >nul
        exit /b 1
    )
)

cd /d "%~dp0backend"
start "后端服务器" cmd /c "python manage.py runserver 2> "%~dp0backend_error.log""

echo 等待后端服务器启动...
echo 等待后端服务器启动... >> "%LOG_FILE%"
echo.

:: 增加等待时间，确保后端服务器有足够时间启动
timeout /t 10 /nobreak >nul

:: 检查后端服务器是否成功启动
netstat -ano | findstr ":8000" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [警告] 无法确认后端服务器是否成功启动，请检查后端启动窗口。
    echo [警告] 无法确认后端服务器是否成功启动。 >> "%LOG_FILE%"
    echo 如果后端服务器未启动，请查看 backend_error.log 文件获取错误信息。
    echo.
    set /p CONTINUE_CHOICE=是否继续启动前端服务？(Y/N): 
    if /i "!CONTINUE_CHOICE!" NEQ "Y" (
        echo 用户选择退出。 >> "%LOG_FILE%"
        echo 按任意键退出...
        pause >nul
        exit /b 1
    )
) else (
    echo 后端服务器已启动！
    echo 后端服务器已启动！ >> "%LOG_FILE%"
    echo.
)

echo ===================================
echo 启动前端服务器...
echo ===================================
echo 启动前端服务器... >> "%LOG_FILE%"

:: 检查前端服务器是否已经在运行
netstat -ano | findstr ":5173" >nul
if %ERRORLEVEL% EQU 0 (
    echo [警告] 端口5173已被占用，可能是前端服务器已经在运行。
    echo [警告] 端口5173已被占用，可能是前端服务器已经在运行。 >> "%LOG_FILE%"
    echo 继续启动可能会导致冲突。
    echo.
    set /p CONTINUE_CHOICE=是否继续启动？(Y/N): 
    if /i "!CONTINUE_CHOICE!" NEQ "Y" (
        echo 用户选择退出。 >> "%LOG_FILE%"
        echo 按任意键退出...
        pause >nul
        exit /b 1
    )
)

cd /d "%~dp0frontend"
start "前端服务器" cmd /c "npm run dev 2> "%~dp0frontend_error.log""

echo 等待前端服务器启动...
echo 等待前端服务器启动... >> "%LOG_FILE%"
echo.

:: 增加等待时间，确保前端服务器有足够时间启动
timeout /t 10 /nobreak >nul

:: 检查前端服务器是否成功启动
netstat -ano | findstr ":5173" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [警告] 无法确认前端服务器是否成功启动，请检查前端启动窗口。
    echo [警告] 无法确认前端服务器是否成功启动。 >> "%LOG_FILE%"
    echo 如果前端服务器未启动，请查看 frontend_error.log 文件获取错误信息。
    echo.
) else (
    echo 前端服务器已启动！
    echo 前端服务器已启动！ >> "%LOG_FILE%"
    echo.
)

echo ===================================
echo 系统启动流程完成！
echo ===================================
echo 系统启动流程完成！ >> "%LOG_FILE%"
echo.

echo 访问说明：
echo - 后端服务器访问地址: http://127.0.0.1:8000
echo - 前端服务器访问地址: http://localhost:5173
echo.
echo 注意事项：
echo 1. 请确保使用完整的URL地址（包含http://）访问服务
echo 2. 如果无法访问，请检查：
echo    - 是否有其他程序占用了5173或8000端口
echo    - 前端启动窗口中显示的实际URL地址是否与上述地址不同
echo    - 防火墙是否阻止了应用程序的网络访问
echo 3. 请不要关闭此窗口，关闭窗口将导致服务停止运行
echo.
echo 如果系统未正常启动，请查看以下日志文件：
echo - 启动日志: %LOG_FILE%
echo - 后端错误日志: %~dp0backend_error.log
echo - 前端错误日志: %~dp0frontend_error.log
echo.
echo 如需退出系统，请关闭所有命令行窗口。
echo.
echo 按任意键继续查看此窗口(不会关闭已启动的服务)...
pause >nul

:: 添加无限循环确保窗口不会关闭
echo 主控制窗口保持运行中，关闭此窗口将导致服务停止...
echo 如需退出，请直接关闭此窗口。
:keep_window_open
timeout /t 60 /nobreak >nul
goto keep_window_open
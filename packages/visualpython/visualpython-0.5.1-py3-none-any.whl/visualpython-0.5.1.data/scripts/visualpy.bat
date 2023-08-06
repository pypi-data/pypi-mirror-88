@echo off
rem #==========================================================================
rem # Filename : visualpy.bat
rem # function : control Visual Python for windows
rem # Creator  : BlackLogic - LJ
rem # version  : 1.10
rem # License  :
rem # Date     : 2020 07.30
rem # MDate    : 2020 10.27
rem #==========================================================================

rem ## setting variables
set v_prod=visualpython
(echo "%v_prod%" & echo.) | findstr /O . | more +1 | (set /P RESULT= & call exit /B %%RESULT%%)
set /A v_prd_length=%ERRORLEVEL%-5
set v_option=%1
for /f "delims=, tokens=1*" %%i in ('pip show %v_prod% 2^>^&1 ^| find "Location"') do (
set v_1=%%i)
set v_path1=%v_1:~10%
set v_str1=jupyter nbextension
set v_str2=%v_prod%/src/main
set v_srch=pip search %v_prod%
set v_upgr=pip install %v_prod% --upgrade
set v_unst=pip uninstall %v_prod%

where /q conda-env
IF ERRORLEVEL 1 (
    ECHO.
    ECHO Not a conda env.
    set v_path2=%APPDATA%\jupyter\nbextensions\
) ELSE (
    ECHO.
    ECHO conda env.
    set v_path2=%v_path1:~,-18%\share\jupyter\nbextensions\
)

rem ## Main Block
:l_main
    IF /i "%v_option%"=="" goto :l_help

    for %%i in (-h help)           do if /i %v_option% == %%i call :l_help
    for %%i in (-e enable)         do if /i %v_option% == %%i call :l_enable
    for %%i in (-d disable)        do if /i %v_option% == %%i call :l_disable
    for %%i in (-i install)        do if /i %v_option% == %%i call :l_install
    for %%i in (-up upgrade)       do if /i %v_option% == %%i call :l_upgrade
    for %%i in (-v version)        do if /i %v_option% == %%i call :l_version
    for %%i in (-ce checkext)      do if /i %v_option% == %%i call :l_check_extension
    for %%i in (-cb checkbpl)      do if /i %v_option% == %%i call :l_check_visualpython
    for %%i in (-vc versioncheck)  do if /i %v_option% == %%i call :l_version_cmp
    for %%i in (-un uninstall)     do if /i %v_option% == %%i goto :l_uninstall
    goto :eof


rem ## Function Block
:l_help
    echo.
    echo usage: visualpy option
    echo optional arguments:
    echo  -h,  help        show this help message and exit
    echo  -e,  enable      enable Visual Python
    echo  -d,  disable     disable Visual Python
    echo  -i,  install     install Visual Python extensions
    echo  -un, uninstall   uninstall Visual Python packages
    echo  -up, upgrade     upgrade Visual Python Package
    echo  -v,  version     show Visual Python current version
    echo.
    goto :eof

:l_check_extension
    IF NOT EXIST %v_path2% call :l_prt_extensiondir
    goto :eof

:l_check_visualpython
    IF EXIST %v_path2%%v_prod% (
            set v_flag=1
        ) ELSE (
            set v_flag=2
        )
    goto :eof

:l_install
	rem "" is for envname with space.
    IF EXIST "%v_path2%%v_prod%" ( call :l_prt_be_line
                                   echo Check installed %v_prod% Path :
                                   echo %v_path2%%v_prod%
                                   goto :l_prt_visualpythondir
    ) ELSE ( call :l_copy_files
             call :l_enable
    )
rem    IF NOT EXIST "%v_path2%%v_prod%" ( 
rem	         call :l_copy_files
rem             call :l_enable
rem    ) ELSE ( echo.
rem             echo installed %v_prod% Path :
rem             echo %v_path2%%v_prod%
rem             goto :l_prt_visualpythondir
rem    )
    goto :eof

:l_enable
    call :l_prt_be_line
    %v_str1% enable %v_str2%
    call :l_prt_af_line
    goto :eof

:l_disable
    call :l_prt_be_line
    %v_str1% disable %v_str2%
    call :l_prt_af_line
    goto :eof

:l_overwrite
    rem if visaulpython 없는경우 install로 수행
    rem else remove & install
        IF EXIST %v_path2%%v_prod% (
            call :l_disable
            call :l_remove_files
            call :l_copy_files
            call :l_enable
        ) else (
            goto :l_prt_notexists_visualpythondir
        )
    goto :eof

:l_copy_files
    call :l_prt_be_line
    echo source : %v_path1%\%v_prod%
    rem "" is for envname with space.
    xcopy /q /y /e "%v_path1%\%v_prod%" "%v_path2%%v_prod%\"
    echo target : %v_path2%%v_prod%\
    call :l_prt_af_line
    goto :eof

:l_remove_files
    call :l_prt_be_line
    echo Remove Visual Python Directories.
    rem "" is for envname with space.
    rmdir /s /q "%v_path2%%v_prod%"
    call :l_prt_af_line
    goto :eof

:l_version_cmp
    call :l_version

    if %ver_1% == %ver_2% (
            rem echo version same
            set v_ver_flag=1
    ) else (
            rem echo version diff
            set v_ver_flag=0
        )
    goto :eof

:l_upgrade
      call :l_version_cmp
      if %v_ver_flag% == 0 (
          echo Running upgrade visualpython.
          call :l_disable
          %v_upgr%
          call :l_copy_files
          call :l_enable
      goto :eof
      ) else (
          call :l_prt_be_line
          echo Already installed last version.
          call :l_prt_af_line
      )
    goto :eof

:l_version
    call :l_prt_be_line
    for /f "tokens=2" %%i in ('pip search %v_prod% 2^>^&1 ^| find /i "latest"') do (
    set ver_1=%%i)

    for /f "tokens=2" %%i in ('pip show %v_prod% 2^>^&1 ^| find "Version"') do (
    set ver_2=%%i)

    echo Last release version : %ver_1%
    echo Installed version    : %ver_2%

    call :l_prt_af_line
    goto :eof

:l_prt_extensiondir
    call :l_prt_be_line
    echo Nbextension not activated
    echo Plz install nbextension
    call :l_prt_af_line
    goto :eof

:l_prt_visualpythondir
    call :l_prt_be_line
    echo Already exists Visual Python.
	echo.
	echo remove the existing VisualPython and install last version VisualPython again.
	echo.
    echo [run cmd] 
	echo  visualpy uninstall
	echo  pip install visualpython
	echo  visualpy install
    call :l_prt_af_line
    goto :eof

:l_prt_notexists_visualpythondir
    call :l_prt_be_line
    echo Visual Python extension not installed.
    echo.
    echo restart cmd : "visualpython -i"
    call :l_prt_af_line
    goto :eof

:l_prt_be_line
    echo.
    echo =========================================================================================
    goto :eof

:l_prt_af_line
    echo =========================================================================================
    goto :eof

:l_uninstall
    IF EXIST "%v_path2%%v_prod%" (
        call :l_disable
        call :l_remove_files
        echo "%v_path2%%v_prod%"
        call :l_prt_af_line
        %v_unst%
    ) else (
        call :l_prt_be_line
        echo %v_path1:~,-18%\share\jupyter\nbextensions\
        echo %v_path2%%v_prod%
        call :l_prt_af_line
        %v_unst%
    )


rem ## release variable
set v_option=
set v_path1=
set v_path2=
set v_str1=
set v_str2=
set v_srch=
set v_upgr=
set v_unst=
set ver_1=
set ver_2=
set v_1=
set v_2=
set v_flag=
set v_prod=
set v_ver_flag=

rem #==========================================================================
rem #End of File
rem #==========================================================================
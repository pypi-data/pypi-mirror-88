@rem taskarg: ${file}
@Echo off
set OLDHOME_FOLDER=%~dp0
pushd %OLDHOME_FOLDER%
call activate_with_vars.bat

call memory_profiling_time.cmd %MAIN_SCRIPT_FILE%

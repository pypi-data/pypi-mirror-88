@rem taskarg: ${file}
@Echo off

set OLDHOME_FOLDER=%~dp0

pushd %OLDHOME_FOLDER%

call .\activate_with_vars.bat

rem ---------------------------------------------------
set _date=%DATE:/=-%
set _time=%TIME::=%
set _time=%_time: =0%
rem ---------------------------------------------------
rem ---------------------------------------------------
set _decades=%_date:~-2%
set _years=%_date:~-4%
set _months=%_date:~3,2%
set _days=%_date:~0,2%
rem ---------------------------------------------------
set _hours=%_time:~0,2%
set _minutes=%_time:~2,2%
set _seconds=%_time:~4,2%
rem ---------------------------------------------------



set INPATH=%~dp1

set INFILE=%~nx1

set INFILEBASE=%~n1

pushd %INPATH%

mkdir %WORKSPACEDIR_BATCH%\misc\memory_profiling

rem call pip install -q memory-profiler
rem call pip install -q matplotlib

mprof.exe clean
mprof.exe run --include-children %~1
mprof.exe plot --flame
mprof.exe plot -o %WORKSPACEDIR_BATCH%\misc\memory_profiling\[%_years%-%_months%-%_days%_%_hours%-%_minutes%-%_seconds%]_mem_%INFILEBASE%.svg
mprof.exe clean

rem call pip uninstall -q -y memory-profiler
rem call pip uninstall -q -y psutil
rem call pip uninstall -q -y matplotlib
rem call pip uninstall -q -y certifi
rem call pip uninstall -q -y cycler
rem call pip uninstall -q -y kiwisolver
rem call pip uninstall -q -y numpy
rem call pip uninstall -q -y pillow
rem call pip uninstall -q -y pyparsing
rem call pip uninstall -q -y python-dateutil
rem call pip uninstall -q -y six


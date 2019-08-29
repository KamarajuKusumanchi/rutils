REM Dump windows environment variables
REM
REM System environment variables are user environment variables are dumped into
REM two separate files.
REM
REM Sample usage:
REM cmd
REM cd output\directory
REM \full\path\of\dump_env_vars.bat
reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" > system_env_vars.txt
reg query HKEY_CURRENT_USER\Environment > user_env_vars.txt

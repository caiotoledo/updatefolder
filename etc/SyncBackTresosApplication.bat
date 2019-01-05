::Prepared template file for use of Conan and set the environment variables
::To use this, Conan must be installed and Conan cache must be correct.

@call scripts/prepare.bat || echo failed prepare.bat && goto :error


IF "%CONTI_DOIT_ENVIRONMENT_ROOT_DIR%"=="" (
	@echo Variable CONTI_DOIT_ENVIRONMENT_ROOT_DIR is NOT defined
	goto :error
)
IF "%CONTI_DOIT_ENVIRONMENT_BUILD_DIR%"=="" (
	@echo Variable CONTI_DOIT_ENVIRONMENT_BUILD_DIR is NOT defined
	goto :error
)
IF "%CONTI_DOIT_ENVIRONMENT_REPO_DIR%"=="" (
	@echo Variable CONTI_DOIT_ENVIRONMENT_REPO_DIR is NOT defined
	goto :error
)

:: Check if command line parameter (variant) is given
    :: if no, call the script, that the user must select a variant
    :: if yes, call the scripts with the given variant
IF "%~1"=="" (
    @call python scripts/callerupdatefolder.py -cmds=update_folder -root_dir=%CONTI_DOIT_ENVIRONMENT_ROOT_DIR% -build_dir=%CONTI_DOIT_ENVIRONMENT_BUILD_DIR% -repo_dir=%CONTI_DOIT_ENVIRONMENT_REPO_DIR% -variant=* -selectionmode=select || echo failed script && goto :error
) ELSE (
    @call python scripts/callerupdatefolder.py -cmds=update_folder -root_dir=%CONTI_DOIT_ENVIRONMENT_ROOT_DIR% -build_dir=%CONTI_DOIT_ENVIRONMENT_BUILD_DIR% -repo_dir=%CONTI_DOIT_ENVIRONMENT_REPO_DIR% -variant="%~1" -selectionmode=first || echo failed script && goto :error
)

@call "tool/conan/out/deactivate.bat" || echo failed deactivate && goto :error

:success
@exit /B 0

:error
@echo usage:
@echo failure in %0
@call "tool/conan/out/deactivate.bat"
@exit /B 1
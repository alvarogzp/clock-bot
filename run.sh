#!/bin/sh

SLEEP_TIME_SECONDS=0
DEBUG_ENABLED=true

VIRTUALENV_LOCATION="venv"
VIRTUALENV_ACTIVATE_SCRIPT_PATH="$VIRTUALENV_LOCATION/bin/activate"
VIRTUALENV_PYTHON_INTERPRETER="python3"
VIRTUALENV_CREATE_COMMAND="$VIRTUALENV_PYTHON_INTERPRETER -m venv"
VIRTUALENV_PYTHON_SCRIPT_TO_CHECK_IF_INSIDE='
import sys
prefix = getattr(sys, "real_prefix", None)
if prefix is not None: sys.exit(0)  # activated
prefix = getattr(sys, "base_prefix", None)
if prefix is None: sys.exit(1)  # not activated
if prefix != sys.prefix: sys.exit(0)  # activated
sys.exit(1)  # not activated
'

EXIT_STATUS_TO_HALT_BOT=55
RUN_BOT_COMMAND="./main.py"


is_first_execution()
{
    [ "$RE_RUNNING" != "true" ]
}

perform_first_execution_tasks()
{
    cd_to_current_script_location
    update_code
    rerun_current_script
}

cd_to_current_script_location()
{
    current_script_location="$(dirname "$0")"
    cd "$current_script_location"
}

perform_main_tasks()
{
    setup_virtualenv
    build_bot
    run_bot
    check_halt_received $?
    sleep ${SLEEP_TIME_SECONDS}
    update_code
    sleep ${SLEEP_TIME_SECONDS}
    rerun_current_script
}

setup_virtualenv()
{
    if [ ! -d "$VIRTUALENV_LOCATION" ]
    then
        debug "Creating virtualenv on '$VIRTUALENV_LOCATION'"
        ${VIRTUALENV_CREATE_COMMAND} "$VIRTUALENV_LOCATION"
    fi
    if ! is_virtualenv_activated
    then
        debug "Activating virtualenv on '$VIRTUALENV_LOCATION'"
        . "$VIRTUALENV_ACTIVATE_SCRIPT_PATH"
    fi
    if ! is_virtualenv_activated
    then
        debug "Could not set-up virtualenv, exiting!"
        exit 1
    fi
}

is_virtualenv_activated()
{
    "$VIRTUALENV_PYTHON_INTERPRETER" -c "$VIRTUALENV_PYTHON_SCRIPT_TO_CHECK_IF_INSIDE"
}

build_bot()
{
    install_requirements
}

install_requirements()
{
    debug "Installing requirements"
    pip install -r requirements.txt
}

run_bot()
{
    debug "Starting bot instance"
    "$RUN_BOT_COMMAND"
    exit_status=$?
    debug "Bot instance finished"
    return ${exit_status}
}

check_halt_received()
{
    exit_status="$1"
    if should_stop_execution "$exit_status"
    then
        debug "Halt received, stopping"
        exit "$exit_status"
    fi
}

should_stop_execution()
{
    exit_status="$1"
    [ "$exit_status" -eq "$EXIT_STATUS_TO_HALT_BOT" ]
}

update_code()
{
    debug "Updating code (pulling from repo)"
    git pull
}

rerun_current_script()
{
    current_script_name="$(basename "$0")"
    RE_RUNNING=true
    . "./$current_script_name"
}

debug()
{
    if [ "$DEBUG_ENABLED" = "true" ]
    then
        echo ">> $@"
    fi
}


if is_first_execution
then
    perform_first_execution_tasks
else
    perform_main_tasks
fi

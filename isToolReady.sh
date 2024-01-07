#!/bin/bash

# Get the directory of the script
script_dir="$(dirname "$(readlink -f "$0")")"

# Specify the relative path to the configuration file
config_file="$script_dir/config.txt"

# Check if the config file exists
if [ -e "$config_file" ]; then
    # Read the configuration values
    write_time_file_seconds=$(jq -r .writeTimeFileEveryXSeconds "$config_file")
    consider_tool_down_seconds=$(jq -r .considerToolAsDownAfterXUnupdatedSeconds "$config_file")

    # Specify the relative path to the file in the same directory as the script
    time_file="$script_dir/timefile.txt"

    # Check if the file exists
    if [ -e "$time_file" ]; then
        # Get the modification time of the file
        file_modification_time=$(stat -c %Y "$time_file")

        # Get the current time
        current_time=$(date +%s)

        # Calculate the difference in seconds
        time_difference=$((current_time - file_modification_time))

        # Check if the content is older than the specified duration
        if [ "$time_difference" -gt "$consider_tool_down_seconds" ]; then
            echo "Content in $time_file is older than $consider_tool_down_seconds seconds. Exiting with non-zero status."
            exit 1
        else
            echo "Content in $time_file is not older than $consider_tool_down_seconds seconds. Exiting with zero status."
            exit 0
        fi
    else
        echo "File $time_file does not exist. Exiting with non-zero status."
        exit 1
    fi
else
    echo "Config file $config_file does not exist. Exiting with non-zero status."
    exit 1
fi

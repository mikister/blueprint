#!/usr/bin/env bash



# Check if blueprint directory exist; create if not
if [[ ! -d "/home/$(whoami)/.blueprint" ]]; then
    mkdir "/home/$(whoami)/.blueprint"
fi

# Change owner on .blueprint directory from root to current user
sudo chown -R "$(whoami):$(whoami)" "/home/$(whoami)/.blueprint"


# Copy neccesary scripts to /usr/local/bin/
sudo cp ./blueprint.py /usr/local/bin/
sudo cp ./blueprint /usr/local/bin

# Make /usr/local/bin/blueprint executable
sudo chmod +x /usr/local/bin/blueprint

#!/usr/bin/env bash



# Check if blueprint directory exist; create if not
if [[ ! -d "/home/$(whoami)/.blueprint" ]]; then
    mkdir "/home/$(whoami)/.blueprint"
fi

sudo chown -R "$(whoami):$(whoami)" "/home/$(whoami)/.blueprint"


# Copy script to /usr/local/bin/
sudo cp ./blueprint.py /usr/local/bin/

# Copy command script to /usr/local/bin
sudo cp ./blueprint /usr/local/bin

# Make /usr/local/bin/blueprint executable
sudo chmod +x /usr/local/bin/blueprint

# blueprint

A tool that manages templates and boilerplate files for you.

## Usage

Lets say you have a **blueprint** (WIP name for a collection of files and dirs) that you called `flask-boilerplate`. You go to an empty directory for your new flask project and type this in the terminal:

```shell
blueprint flask-boilerplate
```

That's it!

If this is what you put in your blueprint:

```
.
├── templates
|   └── example_template.html
├── static
|   ├── style.css
|   └── main.js
└── start_server.py
```
Then that is exactly what you will get, added to your project.


## Instaling

### Linux

Either download the files or use git:

```sh
# HTTPS
# If you have no idea what is the difference between 
# these two options, HTTPS is the one you should pick.
git clone https://github.com/mikister/blueprint.git

# SSH
git clone git@github.com:mikister/blueprint.git
```

Then when you are inside the repo run the `install.sh` file:

```sh
./install.sh
```

| This is an archive of a side project from ancient times. Reader be warned, for the spaghetti contained within can drive even the most rational to madness. |
| --- |

# debateGate.net

This is all the code for debateGate.net

# Install (Linux)
You can run this series of commands in the directory you wish to install debateGate in:

`wget https://gist.githubusercontent.com/devsebb/1a61d31f7ea169b6f6a2973614e9633e/raw/8601ecf0b719db9bf8ae792d8573292e693fa383/debateGate_install.sh`

`chmod +x ./debateGate_install.sh`

`./debateGate_install.sh`


This will download the install script, make the it executable, and install the project. If you want to download the file via your browser instead of using wget, you can grab it from [here](https://gist.github.com/devsebb/1a61d31f7ea169b6f6a2973614e9633e). Note that you may need to use your package manager to install platform-specific packages (Ubuntu has python3-venv, for example) for this to work.

You will then need to install Postgresql and createdb a new database. Also, in app/main.py, you'll probably want to change the mode from "prod" to "dev". Doing this means you'll also need to self-sign and put in the base directory (above app/) an ssl.crt and an ssl.key.

Then, you'll need to add the following information into config.py.template in the appropriate places, **and rename it to config.py**:

1. Google API client ID
2. Google API client secret
3. A different redirect URI
4. A Gmail address and password, for emailing
5. Database name, corresponding to your Postgres database.

After you do all this, you can move setup_database.sh from the scripts/database folder into the base folder, above app/, and execute it. For a successful execution you may need to source the virtual environment:

`source flask/bin/activate`

You should now have a working install of debateGate.

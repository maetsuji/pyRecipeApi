# This script is used to run the pyRecipeAPI application.
# It sets up the environment, installs dependencies, and starts the application.
# It is assumed that the script is run from the root directory of the project.
# Ensure the script is run from the root directory of the project
# Check if the script is being run from the root directory 
if [ ! -f "requirements.txt" ]; then
    echo "Please run this script from the root directory of the project."
    exit 1
fi

# Check if the user is running the script with sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo."
    exit 1
fi

# Check if python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python could not be found. Proceeding to install Python..."
    # check if user uses pacman or apt
    if command -v pacman &> /dev/null
    then
        echo "Installing Python using pacman...
        sudo pacman -S python"
    elif command -v apt &> /dev/null
    then
        echo "Installing Python using apt... 
        sudo apt install python3"
    else
        echo "Please install Python manually."
    fi
fi

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Proceeding to install pip..."
    # check if user uses pacman or apt
    if command -v pacman &> /dev/null
    then
        echo "Installing pip using pacman...
        sudo pacman -S python-pip"
    elif command -v apt &> /dev/null
    then
        echo "Installing pip using apt... 
        sudo apt install python3-pip"
    else
        echo "Please install pip manually."
    fi
fi
# Check if pip-compile is installed
if ! command -v pip-compile &> /dev/null
then
    echo "pip-compile could not be found. Proceeding to install pip-tools..."
    # check if user uses pacman or apt
    if command -v pacman &> /dev/null
    then
        echo "Installing pip-tools using pacman...
        sudo pacman -S python-pip-tools"
    elif command -v apt &> /dev/null
    then
        echo "Installing pip-tools using apt... 
        sudo apt install python3-pip-tools"
    else
        echo "Please install pip-tools manually."
    fi
fi
# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "docker-compose could not be found. Proceeding to install docker-compose..."
    # check if user uses pacman or apt
    if command -v pacman &> /dev/null
    then
        echo "Installing docker-compose using pacman...
        sudo pacman -S docker-compose"
    elif command -v apt &> /dev/null
    then
        echo "Installing docker-compose using apt... 
        sudo apt install docker-compose"
    else
        echo "Please install docker-compose manually."
    fi
fi
# Check if docker is installed
if ! command -v docker &> /dev/null
then
    echo "docker could not be found. Proceeding to install docker..."
    # check if user uses pacman or apt
    if command -v pacman &> /dev/null
    then
        echo "Installing docker using pacman...
        sudo pacman -S docker"
    elif command -v apt &> /dev/null
    then
        echo "Installing docker using apt... 
        sudo apt install docker"
    else
        echo "Please install docker manually."
    fi
fi

pip-compile requirements.in --strip-extras
sudo docker-compose up --build --remove-orphans
# Game Service
[![Python 3.7](https://img.shields.io/badge/python-3.7-green.svg)](https://www.python.org/downloads/release/python-370/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

API Endpoints for games supplied by The Global Digital Library.

## Installation
#### Before you start

- [node](https://nodejs.org/) version should be 10 or above (to check `node -v`) or use [nvm](https://github.com/creationix/nvm).
- [serverless](https://serverless.com/) should be installed globally (`npm install -g serverless`)
- [pyenv](https://github.com/pyenv/pyenv) should be installed (`brew install pyenv`)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) should be installed (`brew install pyenv-virtualenv`)

#### Install Dependencies
* `cd game-service/`
* `npm install`

### Set up virtual environment for python

```
# 1. Activate pyenv - add to ~/.bash_profile
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# 2. Create virtual-env for service
pyenv virtualenv -p python3.7 3.7.0 game-service`

# 3. Activate virtualenv
pyenv activate game-service

# 4. Install depenencies
cd game-service
pip install -r requirements.txt

```

### Run local dev-server
```
# If part of GDL-team:
gdl deploy local game-service

# If not part of GDL-team:
cd game-service
./run_local.sh  #This will probably fail unless all env-variables are set.

```


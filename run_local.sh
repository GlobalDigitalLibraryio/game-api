#!/bin/bash

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export PYENV_VIRTUALENV_DISABLE_PROMPT=0
pyenv activate game-service
sls dynamodb install --localPath ./bin
(sls dynamodb start)
(sls wsgi serve)
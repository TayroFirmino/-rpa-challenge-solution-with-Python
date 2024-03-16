#!/bin/bash

####################################################################################
# Script: start.sh
# Descrição: Cria uma venv caso nao exista, ativa, instala dependencia, executa main
# Autor: Tayro Firmino
# Data: 13/03/2024
####################################################################################

alias python=python3

venv_dir="."

activate_arquivo="$venv_dir/bin/activate"

ativarVenv() {
  source bin/activate
}

criarVenv() {
  python -m venv .
}

if [ ! -f "$activate_arquivo" ]; then
  criarVenv
fi

ativarVenv

pip install -r requirements.txt | grep -v 'already satisfied'

# Instala o chromium
if ! python -m pip show playwright &> /dev/null; then
  playwright install chromium
fi

python main.py
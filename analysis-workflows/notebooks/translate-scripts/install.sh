#!/bin/bash
cd $HOME
git clone https://github.com/ucberkeley/brc-cyberinfrastructure.git
cd $HOME/brc-cyberinfrastructure
git checkout dev

# Add translate scripts to path
echo "export PATH=$HOME/brc-cyberinfrastructure/analysis-workflows/notebooks/translate-scripts:\$PATH" >> ~/.bashrc
source ~/.bashrc

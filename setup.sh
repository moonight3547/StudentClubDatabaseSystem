conda create -n stuclubdb_env python==3.10
conda activate stuclubdb_env
pip install -r requirements.txt
brew install mysql
brew services start mysql

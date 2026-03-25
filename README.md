# LEARNINGS-python-api-development
All the code related to freeCodeCamp.org Python API Development (https://www.youtube.com/watch?v=0sOvCWFmrtA)

# Before running pip install -r requirements.txt, Run the following command to install psycopg2 :
### 1. For macOS (Homebrew)
```bash
brew install libpq
echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 2. For Linux :
```bash
sudo apt update
sudo apt install -y build-essential libpq-dev python3-dev
```

## Activate your Virtual Env. and update some libraries :
```bash
source <PATH-TO-YOUR-VENV>/bin/activate
pip install -U pip setuptools wheel
```

> Now run `pip install -r requirements.txt`

> Note that all alembic commands are present at : https://alembic.sqlalchemy.org/en/latest/api/ddl.html
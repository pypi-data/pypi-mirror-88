
# Python DataBase Entity Model

SDK fornece uma série de recursos que aumentam muito a produtividade no desenvolvimento de aplicações integrada a banco de dados com gerenciamento de objeto.

# Instalação
Instalação utilizando Pip
```bash
pip install dbmodel
```
Git/Clone
```
git clone https://github.com/robertons/dbmodel
cd dbmodel
pip install -r requirements.txt
python setup.py install
```

## Generate Entity Model

```python
import os
import dbmodel

dbmodel.Make(dir = os.path.dirname(os.path.abspath(__file__)), db_user="user", db_password="pass", db_host="host", db_port=3306, db_database="dbname")

```

> Make will create folder on your project like this:

```bash
.
├── ...
├── model                    # Entity Model Folder
│   ├── __init__.py          
│   ├── table_a              # TableA Entity Class
│   ├── table_b              # TableB Entity Class
│   └── table_b              # TableC Entity Class
└── ...
```

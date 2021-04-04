## Korean name generator

Fetches most popular first and last names from websites
register them in test db

#### How to run

Change configurations
- LASTNAME_MAX_PAGE = 20 : The number of pages when fetching first names. It affects diversity of generations
- HOSTNAME = 'localhost'
- USER = 'root'
- PASSWORD = 'my-secret-pw'
- DBNAME = 'project'

Update query statement
```
    sql = 'INSERT INTO student (name, dept_id, grade) VALUES(%s, %s, %s)'
```

Set number of names to generate. Default: 20000
```buildoutcfg
def run_main():
    register_students(num=20000, delete_existings=True)
```

Run script
```buildoutcfg
python3 main.py
```

Check new names in db (workbench query)
```
SELECT * FROM student;
```
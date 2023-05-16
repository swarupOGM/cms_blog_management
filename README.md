## cms_blog_management
`CREATE UPLOADS FILE UNDER static FOLDER`

## CREATE VIRTUAL ENVIRONMENT
  `ACTIVATE AND pip install -r requiremnts.txt`

## To Migrate Follow the below instruction-->>
` 1.flask db init
 2.flask db migrate -m "Initial migration."
 3.flask db upgrade`
 
## To create Super user-->>
`flask shell
 >> from app import db, User
 >> u = User(username="", password="", is_admin=True)
 >> db.session.add(u)
 >> db.session.commit()`

import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

def create_account(name, password):
   user = PasswordUser(models.User())
   user.username = name
   user.password = password
   session = settings.Session()
   session.add(user)
   session.commit()
   session.close()


create_account("admin", "admin")

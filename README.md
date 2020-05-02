# Diary
An app that takes daily entries of how your day went , write down memories of the day, and tag each memory as you feel.
Retrieve from content of previous dates.
the purpose of tagging is to have a stats of what you have been through over time, the percentage of happiness or sadness according to what you tag will be calculated at the end of each month
Also, with time, entries will be automatically tagged according to previous tagged entries, that is a sentiment engine will be trained.
All still a work in progress....

Local installation process
clone repo, ofcourse
Create a database 'Diary'
import the `users` table and `entries` table in the sql_dumps
import it into yhe diary data base yoou created.
Modify SQL credentials according to your engine in the app.py file

 ` app.config['MYSQL_HOST'] = '127.0.0.1'
  app.config['MYSQL_PORT'] = 3306
  app.config['MYSQL_USER'] = 'root'
  app.config['MYSQL_PASSWORD'] = 'root'`
 
run app : python app.py from Diary directory
login details:
  username : munny
  password : munny.
or create an account.

            
  

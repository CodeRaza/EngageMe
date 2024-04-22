@ECHO OFF

SET DB_USER=root
SET DB_PW=root
SET DB_HOSTNAME=localhost
SET DB_PORT=33066
SET DB_NAME=incident_management


SET MAIL_SERVER=smtp.googlemail.com
SET MAIL_PORT=465
SET MAIL_USERNAME=fahadfarhad602@gmail.com
SET MAIL_PASSWORD=nlkatfahwxjrqjsf
SET MAIL_USE_TLS=false
SET MAIL_USE_SSL=true
SET MAIL_USE_SSL=true
SET MAIL_SECRET_KEY=test


CMD /k "python runApp.py"
from errno import errorcode
import os
import mysql.connector 

# Obtain connection string information from the portal
config = {
  'host': 'kostiaraamarta.mysql.database.azure.com',
  'user': 'kostiaraamarta',
  'password':'Mozarella1945',
  'database':'kostiaraamarta',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '/DigiCertGlobalRootG2.crt.pem'
}

# Construct connection string
try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor(dictionary=True)
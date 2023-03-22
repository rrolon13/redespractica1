import time
from datetime import datetime, timedelta
print(time.time())

fecha1 = '2023-03-08'
fecha2 = '2002-12-27'

dias = str(datetime.strptime(fecha1, '%Y-%m-%d') - datetime.strptime(fecha2, '%Y-%m-%d'))
print("Dias vividos: ", dias[0:4])
print("Mod 3: ", int(dias[0:4])%3)
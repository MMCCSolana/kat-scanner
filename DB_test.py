from numpy import floor
from pandas.core.base import DataError
import psycopg2
from datetime import datetime
import pandas as pd

con = psycopg2.connect(
            host = "ec2-35-153-88-219.compute-1.amazonaws.com",
            database = "d8moers639v8ep",
            user = "rtqdsyhnkwqepo",
            password = "9756e62250ffd60cbd98b664fc857623393385145d7fd429c67b9186b94d5afc"
    )

cur = con.cursor()

#init table if reset
# cur.execute("CREATE TABLE floor (date TIMESTAMPTZ, SA numeric, DE numeric, ME numeric)")
# cur.execute("SET timezone = 'America/Chicago'")
# con.commit()
# con.close()

#ins in values
#ins_script = "INSERT INTO floor (date, SA, DE, ME) VALUES (%s,%s,%s,%s)"
#ins_value = (datetime.now(),7,8,4)
#cur.execute(ins_script,ins_value)

#select values
floor_data = pd.DataFrame()
cur.execute("SELECT to_char(date, 'YYYY-MM-DD HH24:00'), SA, DE, ME, listed FROM floor")
data = cur.fetchall()
for entry in data:
    date, SA_f, DE_f,ME_f,listed = entry
    row = pd.DataFrame(data = [date, SA_f, DE_f,ME_f,listed]).T
    floor_data = floor_data.append(row)
floor_data.columns = ["Date","SA","DE","ME","listed"]
floor_data.sort_values(by = ['Date'], inplace=True)
print(floor_data)

con.commit()
con.close()

# print(floor_data)

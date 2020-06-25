import psycopg2
import numpy as np

def Cp(mylist, usl, lsl):
            arr = np.array(mylist)
            arr = arr.ravel()
            sigma = np.std(arr)
            Cp = float(usl - lsl) / (6 * sigma)
            return Cp

def Cpk(mylist, usl, lsl):
    arr = np.array(mylist)
    arr = arr.ravel()
    sigma = np.std(arr)
    m = np.mean(arr)

    Cpu = float(usl - m) / (3 * sigma)
    Cpl = float(m - lsl) / (3 * sigma)
    Cpk = np.min([Cpu, Cpl])
    return Cpk
####
conn = psycopg2.connect(database="demo", user="postgres", password="admin", host="127.0.0.1",
                        port="5433")
print("Opened database successfully")
cur = conn.cursor()
# cur.execute("SELECT value, low_lim from report_data where start")
ostgres_insert_query = """ SELECT value, low_lim ,up_lim from ddata between start_date = %s and end_date = %s)"""
record_to_insert = (start_date, end_date)
print(start_date, end_date)
cur.execute(postgres_insert_query, record_to_insert)
rows = cur.fetchall()
a = []
for row in rows:
    a.append(row[0])
print(a)  # call the cp cpk function
conn.close()
#######
print(Cp(a,usl,lsl))
print(Cpk(a,usl,lsl))


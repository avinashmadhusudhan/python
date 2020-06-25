import logging
from manufacturing.analysis import calc_pp, calc_ppk
from manufacturing.visual import ppk_plot
import psycopg2
from flask import *

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/')
def customer():
    return render_template('pick_date.html')


@app.route('/success', methods=['POST', 'GET'])
def print_data():
    def query(start_date, end_date):
        conn = psycopg2.connect(database="demo_report", user="postgres", password="admin", host="127.0.0.1",
                                port="5433")
        print("Opened database successfully")

        cur = conn.cursor()
        # cur.execute("SELECT value, low_lim from report_data where start")

        postgres_insert_query = """ SELECT value, low_lim ,up_lim from report_data between start_date = %s and end_date = %s)"""
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
        data_set = a

        spec_limits = {
            'upper_control_limit': rows[0][1],
            'lower_control_limit': rows[0][2]
        }

        pp = calc_pp(data_set, **spec_limits)
        ppk = calc_ppk(data_set, **spec_limits)

        print(f'Cp = {pp:.3g}')
        print(f'Cpk = {ppk:.3g}')
        query.resulttt = []
        query.resulttt = ["Cp", pp]
        query.resulttt = ["Cpk", ppk]

    ##########


    result1 = dict(request.form)
    print(result1['start_date'])
    print(result1['end_date'])
    query(result1['start_date'], result1['end_date'])

    if request.method == 'POST':
        result = (request.form)
        print(result)
        return render_template("result_data.html", result=query.result)
######
if __name__ == '__main__':
    app.run(debug=True)




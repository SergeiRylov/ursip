#!/bin/python3
import sys
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session

from db import Stats, engine

if len(sys.argv) == 1 or not sys.argv[1] in {'-l', '-r'}:
    print('usage: test_task.py [-l | -r filename]\n-l filename: upload file\n-r: show result')
    exit()

session = Session(bind=engine)

if sys.argv[1] == '-l':
    try:
        fl = pd.read_excel(sys.argv[2], nrows=100, usecols='A:F')
        df = np.array(fl)
        for rows in df[2:]:
            company = rows[1]
            for i, total in enumerate(rows[2:]):
                q = 'Qliq' if i in {0, 1} else 'Qoil'
                data = 'data1' if i in {0, 2} else 'data2'
                record = Stats(company=company, q=q, data=data, total=total)
                session.add(record)
        session.commit()
        print("File uploaded successfully")
    except:
        print("ERROR: Can't upload file")

elif sys.argv[1] == '-r':
    with engine.connect() as conn:
        sql = "SELECT s.company, s.q, s.data, SUM(s.total) AS total FROM stats s "
        sql += "GROUP BY s.company, s.q, s.data;"
        result = conn.execute(sql)
        data = result.fetchall()
        df = pd.DataFrame(data, columns=result.keys())
        if not df.empty:
            tbl = pd.pivot_table(df, 
                                index='company',
                                columns=['q', 'data'],
                                values='total',
                                # aggfunc=np.sum
                                )
            print(tbl)
        else:
            print('ERROR: DB is empty')


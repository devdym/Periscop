import os
import pandas as pd
from datetime import datetime


def read_battery_short(file):
    """
    Parse DigiCOURCE battery stats from text file

    Returns
    -------
    [Pandas DataFrame]
        battery stats data
    """

    batt = []

    with open(file) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            if len(line) == 22:
                # print("Line {}: {}".format(cnt, line.strip()))
                tmp = line.strip().split(' ')
                while '' in tmp:
                    tmp.remove('')
                batt.append(tmp)
            # tmp.clear()
            line = fp.readline()
            cnt += 1

    df = pd.DataFrame(batt, columns=['unit', 'bank_a', 'bank_b', 'active_bank'])
    f = os.path.basename(file)
    f = f.split()
    da = f[2]
    datetime_object = datetime.strptime(da, '%m%d%y')
    df['bank_a'] = df['bank_a'].astype('float')
    df['bank_b'] = df['bank_b'].astype('float')
    df['streamer_number'] = df['unit'].str.slice(1, 3)
    df['unit_name'] = df['unit'].str.slice(3, 4)
    df['unit_number'] = df['unit'].str.slice(4, 6)
    df['date_'] = datetime_object

    return df

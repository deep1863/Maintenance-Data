"""Run once to populate sample data matching the reference Excel sheet."""
import sqlite3, os, sys

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'machine_data.db')

sample = [
    # (machine_name, sno, date, breakdown, action, spares, now, nbd, downtime, cleared)
    ('Hydraulic Press #1', 1, '2021-01-16',
     'S/O kept off due to P9 booster get leakage.',
     'New booster fitted.',
     "5'' booster", 'BD', 'New', '1HRS 30MIN', 'Int'),
    ('Mixer 30T', 1, '2021-03-03',
     'Hydraulic power pack HMI get hang',
     'Due to its PLC which was in classifier panel show SF mode and stop mode as PLC CPU get damaged so it is replaced from removing CPU from 30T mixer panel (L & T)',
     'PLC CPU', 'BD', 'New', '6 HRS', 'Int'),
    ('Hydraulic Press #1', 2, '2021-04-10',
     'Main cylinder pressure dropping intermittently.',
     'Replaced hydraulic seal kit on main cylinder. Pressure tested and confirmed stable.',
     'Seal kit, O-rings', 'BD', 'Repeat', '3 HRS', 'Int'),
    ('CNC Machine #1', 1, '2021-05-15',
     'Monthly preventive maintenance - spindle lubrication and axis calibration.',
     'Lubricated all spindle bearings, calibrated X/Y/Z axes, cleaned coolant tank and filter.',
     'Lubricant oil, filter', 'PM', 'N/A', '2 HRS', 'Int'),
    ('Conveyor Belt A', 1, '2021-06-02',
     'Belt slipping on drive pulley under load.',
     'Tightened belt tension, replaced worn lagging on drive pulley.',
     'Lagging strip, bolts', 'BD', 'Repeat', '4 HRS', 'Ext'),
    ('CNC Machine #1', 2, '2021-07-20',
     'Coolant pump motor failed, machine stopped mid-cycle.',
     'Replaced coolant pump motor (0.75 kW). Rewired to original specs and tested.',
     'Coolant pump motor 0.75kW', 'BD', 'New', '5 HRS', 'Ext'),
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
for row in sample:
    m = c.execute('SELECT id FROM machines WHERE name=?', (row[0],)).fetchone()
    if not m:
        c.execute('INSERT INTO machines (name) VALUES (?)', (row[0],))
        mid = c.lastrowid
    else:
        mid = m[0]
    exists = c.execute('SELECT id FROM maintenance_log WHERE machine_id=? AND entry_date=? AND breakdown_details=?',
                       (mid, row[2], row[3])).fetchone()
    if not exists:
        c.execute('''INSERT INTO maintenance_log
            (machine_id, sno, entry_date, breakdown_details, action_taken,
             spares_used, nature_of_work, nature_of_bd, total_down_time, bd_cleared)
            VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (mid, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
conn.commit()
conn.close()
print("Sample data loaded successfully!")

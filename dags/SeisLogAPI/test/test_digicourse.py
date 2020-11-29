from dags.SeisLogAPI.digicourse import read_battery_short


def test_read_battery_short():
	file = '../data\\Batt-Volt on 090320 at 16 hours.txt'
	b = read_battery_short(file)
	assert len(b) == 252
	assert type(b).__name__ is 'DataFrame'
	assert b.columns.tolist() == ['unit', 'bankA', 'bankB', 'activeBank',
								  'streamerNumber', 'unitName', 'unitNumber', 'date_']

from dags.SeisLogAPI.nav import read_wing_angle


def test_read_wing_angle():
	file = '../data\\TPLA19-1054P1009-ChObs_Wing_Angles.sts'
	b = read_wing_angle(file)
	assert len(b) == 174
	assert type(b).__name__ is 'DataFrame'
	assert b.columns.tolist() == ['name', 'min', 'max', 'mean', 'sd', 'obs', 'rej',
								  'streamer', 'compass', 'linename', 'seq']

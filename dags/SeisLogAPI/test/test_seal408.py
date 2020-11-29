from dags.SeisLogAPI.seal408 import read_instest2, read_instestlimits2


def test_read_instest2():
	file = '../data\\DT311219.txt'
	b = read_instest2(file)
	assert len(b) == 3888
	assert type(b).__name__ is 'DataFrame'
	assert b.columns.tolist() == ['ass_sn', 'trace', 'streamer', 'fdu_sn', 'type', 'cap', 'cutoff', 'noise',
								  'leakage', 'updated', 'section_rank', 'ch_nb', 'failure']

def test_read_instestlimits2():
	file = '../data\\DT311219.txt'
	b = read_instestlimits2(file, '311219')
	assert len(b) == 4
	assert type(b).__name__ is 'DataFrame'
	assert b.columns.tolist() == ['sensor_nb', 'noise', 'cap_min', 'cap_max', 'cutoff_min',
								  'cutoff_max', 'leakage', 'updated']

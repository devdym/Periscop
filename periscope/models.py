from periscope import db


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Text)
    client = db.Column(db.Text)
    job_number = db.Column(db.Text)
    project_name = db.Column(db.Text)
    status = db.Column(db.Text)
    type = db.Column(db.Text)
    vessel = db.Column(db.Text)
    batteries = db.relationship('Batteries', backref='project', lazy='dynamic')
    ballasting = db.relationship('Ballasting', backref='project', lazy='dynamic')
    tension = db.relationship('Tension', backref='project', lazy='dynamic')
    tensionavg = db.relationship('TensionAvg', backref='project', lazy='dynamic')
    importlog = db.relationship('ImportLog', backref='project', lazy='dynamic')
    instest = db.relationship('InsTest', backref='project', lazy='dynamic')
    instestres = db.relationship('InsTestRes', backref='project', lazy='dynamic')

    def __init__(self, project_name, vessel):
        self.project_name = project_name
        self.vessel = vessel

    def __repr__(self):
        return self.project_name + self.vessel


class Ballasting(db.Model):
    __tablename__ = 'ballasting'
    id = db.Column(db.Integer, primary_key=True)
    compass = db.Column(db.Integer)
    linename = db.Column(db.Text)
    max_wa = db.Column(db.Float)
    mean_wa = db.Column(db.Float)
    min_wa = db.Column(db.Float)
    name = db.Column(db.Text)
    obs = db.Column(db.Integer)
    rej = db.Column(db.Integer)
    sd = db.Column(db.Float)
    seq = db.Column(db.Integer)
    streamer = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, compass, linename, max_wa, mean_wa,
                 min_wa, name, obs, rej, sd, seq, streamer):
        self.compass = compass
        self.linename = linename
        self.max_wa = max_wa
        self.mean_wa = mean_wa
        self.min_wa = min_wa
        self.name = name
        self.obs = obs
        self.rej = rej
        self.sd = sd
        self.seq = seq
        self.streamer = streamer

    def __repr__(self):
        return str(self.compass) + str(self.seq) + str(self.mean_wa) + str(self.streamer)


class Batteries(db.Model):
    __tablename__ = 'batteries'
    id = db.Column(db.Integer, primary_key=True)
    active_bank = db.Column(db.Text)
    bank_a = db.Column(db.Float)
    bank_b = db.Column(db.Float)
    date_ = db.Column(db.Date)
    streamer_number = db.Column(db.Integer)
    unit = db.Column(db.Text)
    unit_name = db.Column(db.Text)
    unit_number = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, active_bank, bank_a, bank_b, date_,
                 streamer_number, unit, unit_name, unit_number):
        self.active_bank = active_bank
        self.bank_a = bank_a
        self.bank_b = bank_b
        self.date_ = date_
        self.streamer_number = streamer_number
        self.unit = unit
        self.unit_name = unit_name
        self.unit_number = unit_number

    def __repr__(self):
        return str(self.streamer_number) + ' ' + str(self.unit_number) + ' ' + str(self.bank_a) + ' ' + str(self.bank_b) + ' ' + self.active_bank + ' ' + str(self.date_)


class Tension(db.Model):
    __tablename__ = 'tension'
    id = db.Column(db.Integer, primary_key=True)
    date_ = db.Column(db.Date)
    streamer = db.Column(db.Integer)
    tension = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, date_, streamer, tension):
        self.date_ = date_
        self.streamer = streamer
        self.tension = tension

    def __repr__(self):
        return self.date_ + self.streamer + self.tension


class TensionAvg(db.Model):
    __tablename__ = 'tensionavg'
    id = db.Column(db.Integer, primary_key=True)
    date_ = db.Column(db.Date)
    streamer = db.Column(db.Integer)
    tension = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, date_, streamer, tension):
        self.date_ = date_
        self.streamer = streamer
        self.tension = tension

    def __repr__(self):
        return str(self.date_) + str(self.streamer) + str(self.tension)


class ImportLog(db.Model):
    __tablename__ = 'importlog'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, file):
        self.file = file

    def __repr__(self):
        return self.file


class InsTest(db.Model):
    __tablename__ = 'instest'
    id = db.Column(db.Integer, primary_key=True)
    ass_sn = db.Column(db.Integer)
    cap = db.Column(db.Float)
    ch_nb = db.Column(db.Integer)
    cutoff = db.Column(db.Float)
    failure = db.Column(db.Text)
    fdu_sn = db.Column(db.Integer)
    leakage = db.Column(db.Float)
    noise = db.Column(db.Float)
    section_rank = db.Column(db.Integer)
    streamer = db.Column(db.Integer)
    trace = db.Column(db.Integer)
    type = db.Column(db.Integer)
    updated = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, ass_sn, cap, ch_nb, cutoff, failure, fdu_sn,
                 leakage, noise, section_rank, streamer, trace, sensor_type, updated):
        self.ass_sn = ass_sn
        self.cap = cap
        self.ch_nb = ch_nb
        self.cutoff = cutoff
        self.failure = failure
        self.fdu_sn = fdu_sn
        self.leakage = leakage
        self.noise = noise
        self.section_rank = section_rank
        self.streamer = streamer
        self.trace = trace
        self.type = sensor_type
        self.updated = updated

    def __repr__(self):
        return self.streamer + ' ' + self.trace + ' ' + self.ass_sn + ' ' + \
               str(self.cap) + ' ' + \
               str(self.cutoff)  + ' ' + \
               str(self.leakage)  + ' ' + \
               str(self.noise)        


class InsTestRes(db.Model):
    __tablename__ = 'instestlimit'
    id = db.Column(db.Integer, primary_key=True)
    cap_min = db.Column(db.Float)
    cap_max = db.Column(db.Float)
    cutoff_min = db.Column(db.Float)
    cutoff_max = db.Column(db.Float)
    leakage = db.Column(db.Float)
    noise = db.Column(db.Float)
    sensor_nb = db.Column(db.Integer)
    updated = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, cap_min, cap_max, cutoff_min,
                 cutoff_max, leakage, noise, sensor_nb, updated):
        self.cap_min = cap_min
        self.cap_max = cap_max
        self.cutoff_min = cutoff_min
        self.cutoff_max = cutoff_max
        self.leakage = leakage
        self.noise = noise
        self.sensor_nb = sensor_nb
        self.updated = updated

    def __repr__(self):
        return self.sensor_nb + self.cap_max + self.cap_min

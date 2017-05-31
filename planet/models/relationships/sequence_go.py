from planet import db


class SequenceGOAssociation(db.Model):
    __tablename__ = 'sequence_go'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    sequence_id = db.Column(db.Integer, db.ForeignKey('sequences.id', ondelete='CASCADE'))
    go_id = db.Column(db.Integer, db.ForeignKey('go.id', ondelete='CASCADE'))

    evidence = db.Column(db.Enum('EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP',
                                 'ISS', 'ISO', 'ISA', 'ISM', 'IGC', 'IBA', 'IBD', 'IKR', 'IRD', 'RCA',
                                 'TAS', 'NAS', 'IC', 'ND', 'IEA', name='evidence'))
    source = db.Column(db.Text)

    predicted = db.Column(db.Boolean, default=False)
    prediction_data = db.Column(db.Text)

    sequence = db.relationship('Sequence', backref=db.backref('go_associations',
                                                              lazy='dynamic',
                                                              passive_deletes=True), lazy='joined')

    go = db.relationship('GO', backref=db.backref('sequence_associations',
                                                  lazy='dynamic',
                                                  passive_deletes=True), lazy='joined')

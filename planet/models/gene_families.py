from planet import db
from planet.models.relationships import sequence_family, family_xref

class GeneFamilyMethod(db.Model):
    __tablename__ = 'gene_family_methods'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.Text)
    family_count = db.Column(db.Integer)

    families = db.relationship('GeneFamily', backref=db.backref('method', lazy='joined'), lazy='dynamic')

    def __init__(self, method):
        self.method = method

    @staticmethod
    def update_count():
        """
        To avoid long count queries, the number of families for a given method can be precalculated and stored in
        the database using this function.
        """
        methods = GeneFamilyMethod.query.all()

        for m in methods:
            m.family_count = m.families.count()

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)


class GeneFamily(db.Model):
    __tablename__ = 'gene_families'
    id = db.Column(db.Integer, primary_key=True)
    method_id = db.Column(db.Integer, db.ForeignKey('gene_family_methods.id'), index=True)
    name = db.Column(db.String(50, collation='NOCASE'), unique=True, index=True)
    clade_id = db.Column(db.Integer, index=True)

    sequences = db.relationship('Sequence', secondary=sequence_family, lazy='dynamic')

    xrefs = db.relationship('XRef', secondary=family_xref, lazy='dynamic')

    def __init__(self, name):
        self.name = name

    @property
    def species_codes(self):
        """
        Finds all species the family has genes from
        :return: a list of all species (codes)
        """
        pass
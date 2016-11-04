from planet import db

from planet.models.gene_families import GeneFamilyMethod
from planet.models.xrefs import XRef


def create_plaza_xref_families(method_id):
    """
    Creates xrefs to PLAZA 3.0 Dicots

    :param method_id: Internal ID of the gene family method
    """
    method = GeneFamilyMethod.query.get(method_id)

    families = method.families.all()

    for f in families:
        xref = XRef()
        xref.name = f.name
        xref.platform = "PLAZA 3.0 Dicots"
        xref.url = "http://bioinformatics.psb.ugent.be/plaza/versions/plaza_v3_dicots/gene_families/view/" + \
                   f.name.upper()
        f.xrefs.append(xref)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
from planet import db

from sqlalchemy import and_

sequence_go = db.Table('sequence_go',
                       db.Column('id', db.Integer, primary_key=True),
                       db.Column('sequence_id', db.Integer, db.ForeignKey('sequences.id'), index=True),
                       db.Column('go_id', db.Integer, db.ForeignKey('go.id'), index=True)
                       )

sequence_interpro = db.Table('sequence_interpro',
                             db.Column('id', db.Integer, primary_key=True),
                             db.Column('sequence_id', db.Integer, db.ForeignKey('sequences.id'), index=True),
                             db.Column('interpro_id', db.Integer, db.ForeignKey('interpro.id'), index=True),
                             )

sequence_family = db.Table('sequence_family',
                           db.Column('id', db.Integer, primary_key=True),
                           db.Column('sequence_id', db.Integer, db.ForeignKey('sequences.id'), index=True),
                           db.Column('gene_family_id', db.Integer, db.ForeignKey('gene_families.id'), index=True)
                           )

sequence_coexpression_cluster = \
    db.Table('sequence_coexpression_cluster',
             db.Column('id', db.Integer, primary_key=True),
             db.Column('sequence_id', db.Integer, db.ForeignKey('sequences.id'), index=True),
             db.Column('coexpression_cluster_id', db.Integer, db.ForeignKey('coexpression_clusters.id'), index=True)
             )

coexpression_cluster_similarity = \
    db.Table('coexpression_cluster_similarity',
             db.Column('id', db.Integer, primary_key=True),
             db.Column('source_id', db.Integer, db.ForeignKey('coexpression_clusters.id'), index=True),
             db.Column('target_id', db.Integer, db.ForeignKey('coexpression_clusters.id'), index=True)
             )

sequence_xref = db.Table('sequence_xref',
                         db.Column('id', db.Integer, primary_key=True),
                         db.Column('sequence_id', db.Integer, db.ForeignKey('sequences.id'), index=True),
                         db.Column('xref_id', db.Integer, db.ForeignKey('xrefs.id'), index=True)
                         )

sequence_sequence_ecc = db.Table('sequence_sequence_ecc',
                                 db.Column('id', db.Integer, primary_key=True),
                                 db.Column('query_id', db.Integer, db.ForeignKey('sequences.id'), index=True),
                                 db.Column('target_id', db.Integer, db.ForeignKey('sequences.id'), index=True)
                                 )

family_xref = db.Table('family_xref',
                       db.Column('id', db.Integer, primary_key=True),
                       db.Column('gene_family_id', db.Integer, db.ForeignKey('gene_families.id'), index=True),
                       db.Column('xref_id', db.Integer, db.ForeignKey('xrefs.id'), index=True)
                       )

cluster_go_enrichment = db.Table('cluster_go_enrichment',
                                 db.Column('id', db.Integer, primary_key=True),
                                 db.Column('cluster_id', db.Integer, db.ForeignKey('coexpression_clusters.id'), index=True),
                                 db.Column('go_id', db.Integer, db.ForeignKey('go.id'), index=True)
                                 )


class SequenceCoexpressionClusterAssociation(db.Model):
    __tablename__ = 'sequence_coexpression_cluster'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    probe = db.Column(db.String(50), index=True)
    sequence_id = db.Column(db.Integer, db.ForeignKey('sequences.id'))
    coexpression_cluster_id = db.Column(db.Integer, db.ForeignKey('coexpression_clusters.id'))


class CoexpressionClusterSimilarity(db.Model):
    __tablename__ = 'coexpression_cluster_similarity'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('coexpression_clusters.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('coexpression_clusters.id'))

    gene_family_method_id = db.Column('gene_family_method_id', db.Integer, db.ForeignKey('gene_family_methods.id'),
                                      index=True)

    jaccard_index = db.Column(db.Float, index=True)
    p_value = db.Column(db.Float, index=True)
    corrected_p_value = db.Column(db.Float, index=True)

    source = db.relationship('CoexpressionCluster', lazy='joined', foreign_keys=[source_id])
    target = db.relationship('CoexpressionCluster', lazy='joined', foreign_keys=[target_id])

    gene_family_method = db.relationship('GeneFamilyMethod', lazy='joined')


class SequenceFamilyAssociation(db.Model):
    __tablename__ = 'sequence_family'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    sequence_id = db.Column(db.Integer, db.ForeignKey('sequences.id'))
    gene_family_id = db.Column(db.Integer, db.ForeignKey('gene_families.id'))

    sequence = db.relationship('Sequence', lazy='joined')
    family = db.relationship('GeneFamily', lazy='joined')


class SequenceInterproAssociation(db.Model):
    __tablename__ = 'sequence_interpro'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    sequence_id = db.Column(db.Integer, db.ForeignKey('sequences.id'))
    interpro_id = db.Column(db.Integer, db.ForeignKey('interpro.id'))
    start = db.Column(db.Integer, default=None)
    stop = db.Column(db.Integer, default=None)

    domain = db.relationship('Interpro', lazy='select')


class SequenceGOAssociation(db.Model):
    __tablename__ = 'sequence_go'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    sequence_id = db.Column(db.Integer, db.ForeignKey('sequences.id'))
    go_id = db.Column(db.Integer, db.ForeignKey('go.id'))

    evidence = db.Column(db.Enum('EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP',
                                 'ISS', 'ISO', 'ISA', 'ISM', 'IGC', 'IBA', 'IBD', 'IKR', 'IRD', 'RCA',
                                 'TAS', 'NAS', 'IC', 'ND', 'IEA', name='evidence'))
    source = db.Column(db.Text)


class SequenceSequenceECCAssociation(db.Model):
    __tablename__ = 'sequence_sequence_ecc'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    query_id = db.Column(db.Integer, db.ForeignKey('sequences.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('sequences.id'))

    ecc = db.Column(db.Float)
    p_value = db.Column(db.Float)
    corrected_p_value = db.Column(db.Float)

    gene_family_method_id = db.Column(db.Integer, db.ForeignKey('gene_family_methods.id'))
    query_network_method_id = db.Column(db.Integer, db.ForeignKey('expression_network_methods.id'))
    target_network_method_id = db.Column(db.Integer, db.ForeignKey('expression_network_methods.id'))

    gene_family_method = db.relationship('GeneFamilyMethod', lazy='joined')
    query_expression_network_method = db.relationship('ExpressionNetworkMethod',
                                                      foreign_keys=[query_network_method_id],
                                                      lazy='joined')
    target_expression_network_method = db.relationship('ExpressionNetworkMethod',
                                                       foreign_keys=[target_network_method_id],
                                                       lazy='joined')

    @staticmethod
    def get_ecc_network(sequence, network, family):
        data = SequenceSequenceECCAssociation.query.filter(and_(
                SequenceSequenceECCAssociation.query_id == sequence,
                SequenceSequenceECCAssociation.query_network_method_id == network,
                SequenceSequenceECCAssociation.gene_family_method_id == family)).all()

        # return an empty dict in case there are no hits for this query
        if len(data) < 1:
            return {'nodes': [], 'edges': []}

        # add the query node
        d = data[0]
        nodes = [{"id": d.query_id,
                  "name": d.query_sequence.name,
                  "species_id": d.query_sequence.species_id,
                  "species_name": d.query_sequence.species.name,
                  "gene_id": d.query_id,
                  "gene_name": d.query_sequence.name,
                  "network_method_id": network,
                  "node_type": "query"}]
        edges = []

        networks = {}

        for d in data:
            nodes.append({"id": d.target_id,
                          "name": d.target_sequence.name,
                          "species_id": d.target_sequence.species_id,
                          "species_name": d.target_sequence.species.name,
                          "gene_id": d.target_id,
                          "network_method_id": d.target_network_method_id,
                          "gene_name": d.target_sequence.name})

            if d.target_network_method_id not in networks.keys():
                networks[d.target_network_method_id] = []
            networks[d.target_network_method_id].append(d.target_id)

            # TODO: add p-value and corrected p once implemented
            edges.append({"source": d.query_id,
                          "target": d.target_id,
                          "ecc_score": d.ecc,
                          "edge_type": 'ecc_prime'})

        for n, sequences in networks.items():
            new_data = SequenceSequenceECCAssociation.query.filter(and_(
                SequenceSequenceECCAssociation.query_id.in_(sequences),
                SequenceSequenceECCAssociation.target_id.in_(sequences),
                SequenceSequenceECCAssociation.target_network_method_id == n,
                SequenceSequenceECCAssociation.query_network_method_id == n,
                SequenceSequenceECCAssociation.gene_family_method_id == family,
                SequenceSequenceECCAssociation.query_id != SequenceSequenceECCAssociation.target_id
            )).all()

            for nd in new_data:
                # TODO: add p-value and corrected p once implemented
                # make sure the connection doesn't exist already
                if not any(d['source'] == nd.target_id and d['target'] == nd.query_id for d in edges):
                    edges.append({"source": nd.query_id,
                                  "target": nd.target_id,
                                  "ecc_score": nd.ecc,
                                  "edge_type": 'ecc_secondary'})

        return {"nodes": nodes, "edges": edges}


class ClusterGOEnrichment(db.Model):
    __tablename__ = 'cluster_go_enrichment'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('coexpression_clusters.id'))
    go_id = db.Column(db.Integer, db.ForeignKey('go.id'))

    """
    Counts required to calculate the enrichment,
    store here for quick access
    """
    cluster_count = db.Column(db.Integer)
    cluster_size = db.Column(db.Integer)
    go_count = db.Column(db.Integer)
    go_size = db.Column(db.Integer)

    """
    Enrichment score (log-transformed), p-value and corrected p-value. Calculated using the hypergeometric
    distribution and applying FDR correction (aka. BH)
    """
    enrichment = db.Column(db.Float)
    p_value = db.Column(db.Float)
    corrected_p_value = db.Column(db.Float)

    @property
    def cluster_percentage(self):
        return self.cluster_count*100/self.cluster_size

    @property
    def genome_percentage(self):
        return self.go_count*100/self.go_size


# class ProbeGOEnrichment(db.Model):
#     __tablename__ = 'probe_go_enrichment'
#
#     id = db.Column(db.Integer, primary_key=True)
#     probe_id = db.Column(db.Integer, db.ForeignKey('expression_network.id'), index=True)
#     go_id = db.Column(db.Integer, db.ForeignKey('go.id'), index=True)
#
#     """
#     Counts required to calculate the enrichment,
#     store here for quick access
#     """
#     cluster_count = db.Column(db.Integer)
#     cluster_size = db.Column(db.Integer)
#     go_count = db.Column(db.Integer)
#     go_size = db.Column(db.Integer)
#
#     """
#     Enrichment score (log-transformed), p-value and corrected p-value. Calculated using the hypergeometric
#     distribution and applying FDR correction (aka. BH)
#     """
#     enrichment = db.Column(db.Float)
#     p_value = db.Column(db.Float)
#     corrected_p_value = db.Column(db.Float)

"""
Everything that needs to be set up to get flask running is initialized in this file.

  * set up and configure the app
  * start the database (db)
  * load LoginManager (for user system)
  * start Flask Debug Toolbar
  * load all (!) models used (essential to create the database using db_create)
  * load all (!) controllers and register their blueprints to a subdomain
  * add admin panel

  * set up global things like the search form and custom 403/404 error messages
"""
from flask import Flask, render_template, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.cache import Cache

from flask_admin import Admin
from flask_htmlmin import HTMLMIN

from flask_debugtoolbar import DebugToolbarExtension

from planet.extensions.blast import BlastThread

db = SQLAlchemy()
login_manager = LoginManager()
toolbar = DebugToolbarExtension()
cache = Cache()
htmlmin = HTMLMIN()
blast_thread = BlastThread()

def create_app(config):
    # Set up app, database and login manager before importing models and controllers
    # Important for db_create script

    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    # Enable login manager

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Enable DebugToolBar
    toolbar.init_app(app)

    # Enable cach
    cache.init_app(app)

    # Enable HTMLMIN
    htmlmin.init_app(app)

    LOGIN_ENABLED = app.config['LOGIN_ENABLED']
    BLAST_ENABLED = app.config['BLAST_ENABLED']

    # Enable BLAST
    if BLAST_ENABLED:
        blast_thread.init_app(app)

    # Import all models here
    from planet.models.users import User
    from planet.models.species import Species
    from planet.models.sequences import Sequence
    from planet.models.go import GO
    from planet.models.interpro import Interpro
    from planet.models.gene_families import GeneFamilyMethod, GeneFamily
    from planet.models.coexpression_clusters import CoexpressionClusteringMethod, CoexpressionCluster
    from planet.models.expression_profiles import ExpressionProfile
    from planet.models.expression_networks import ExpressionNetworkMethod, ExpressionNetwork
    from planet.models.clades import Clade
    from planet.models.xrefs import XRef

    # Import all relationships (tables for many-to-many relationships)
    import planet.models.relationships

    # Import controllers and register as blueprint
    from planet.controllers.main import main
    from planet.controllers.auth import auth, no_login
    from planet.controllers.blast import blast
    from planet.controllers.sequence import sequence
    from planet.controllers.species import species
    from planet.controllers.go import go
    from planet.controllers.interpro import interpro
    from planet.controllers.family import family
    from planet.controllers.expression_cluster import expression_cluster
    from planet.controllers.expression_profile import expression_profile
    from planet.controllers.expression_network import expression_network
    from planet.controllers.search import search
    from planet.controllers.help import help
    from planet.controllers.heatmap import heatmap
    from planet.controllers.profile_comparison import profile_comparison
    from planet.controllers.graph_comparison import graph_comparison

    app.register_blueprint(main)
    if LOGIN_ENABLED:
        app.register_blueprint(auth, url_prefix='/auth')
    else:
        app.register_blueprint(no_login, url_prefix='/auth')
    if BLAST_ENABLED:
        app.register_blueprint(blast, url_prefix='/blast')
    app.register_blueprint(sequence, url_prefix='/sequence')
    app.register_blueprint(species, url_prefix='/species')
    app.register_blueprint(go, url_prefix='/go')
    app.register_blueprint(interpro, url_prefix='/interpro')
    app.register_blueprint(family, url_prefix='/family')
    app.register_blueprint(expression_cluster, url_prefix='/cluster')
    app.register_blueprint(expression_profile, url_prefix='/profile')
    app.register_blueprint(expression_network, url_prefix='/network')
    app.register_blueprint(search, url_prefix='/search')
    app.register_blueprint(help, url_prefix='/help')
    app.register_blueprint(heatmap, url_prefix='/heatmap')
    app.register_blueprint(profile_comparison, url_prefix='/profile_comparison')
    app.register_blueprint(graph_comparison, url_prefix='/graph_comparison')

    # Admin panel
    if LOGIN_ENABLED:
        from planet.admin.views import MyAdminIndexView
        from planet.admin.views import SpeciesAdminView, GeneFamilyMethodAdminView, ExpressionNetworkMethodAdminView, \
            CoexpressionClusteringMethodAdminView

        admin = Admin(app, index_view=MyAdminIndexView(template='admin/home.html'))
        admin.add_view(SpeciesAdminView(Species, db.session, url='species/'))
        admin.add_view(GeneFamilyMethodAdminView(GeneFamilyMethod, db.session, url='families/', category="Methods"))
        admin.add_view(ExpressionNetworkMethodAdminView(ExpressionNetworkMethod, db.session, url='networks/',
                                                        category="Methods"))
        admin.add_view(CoexpressionClusteringMethodAdminView(CoexpressionClusteringMethod, db.session, url='clusters/',
                                                             category="Methods"))



    #  ______________________________
    # < Beware, code overrides below >
    #  ------------------------------
    #    \         ,        ,
    #     \       /(        )`
    #      \      \ \___   / |
    #             /- _  `-/  '
    #            (/\/ \ \   /\
    #            / /   | `    \
    #            O O   ) /    |
    #            `-^--'`<     '
    #           (_.)  _  )   /
    #            `.___/`    /
    #              `-----' /
    # <----.     __ / __   \
    # <----|====O)))==) \) /====
    # <----'    `--' `.__,' \
    #              |        |
    #               \       /
    #         ______( (_  / \______
    #       ,'  ,-----'   |        \
    #       `--{__________)        \/


    # Custom error handler for 404 errors

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('error/403.html'), 403

    # Register form for basic searches, needs to be done here as it is included on every page!
    from planet.forms.search import BasicSearchForm

    @app.before_request
    def before_request():
        g.login_enabled = LOGIN_ENABLED
        g.blast_enabled = BLAST_ENABLED
        g.search_form = BasicSearchForm()
        g.page_items = 30

    return app

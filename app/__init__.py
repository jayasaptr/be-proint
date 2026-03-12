from flask import Flask
from .config import Config, db_connection
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.url_map.strict_slashes = False

    # CORS configuration
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import models
    from app.models import edulevel, edumajor, eduinstitution, maritalstatus, city, religion, site, kecamatan, jobtitle, vacantpos, posadtgrphd, posadtgrpdt, posadtgrpmbr, state, cardtype, questtopic, question, candidate, race

    # Test database connection
    db_connection()

    # Import and register blueprints
    from app.routes.edulevel_route import edulevel_bp
    from app.routes.edumajor_route import edumajor_bp
    from app.routes.eduinstitution_route import eduinstitution_bp
    from app.routes.maritalstatus_route import maritalstatus_bp
    from app.routes.city_route import city_bp
    from app.routes.religion_route import religion_bp
    from app.routes.site_route import site_bp
    from app.routes.kecamatan_route import kecamatan_bp
    from app.routes.jobtitle_route import jobtitle_bp
    from app.routes.vacantpos_route import vacantpos_bp
    from app.routes.posadtgrphd_route import posadtgrphd_bp
    from app.routes.posadtgrpdt_route import posadtgrpdt_bp
    from app.routes.state_route import state_bp
    from app.routes.cardtype_route import cardtype_bp
    from app.routes.questtopic_route import questtopic_bp
    from app.routes.question_route import question_bp
    from app.routes.candidate_route import candidate_bp
    from app.routes.race_route import race_bp

    app.register_blueprint(edulevel_bp, url_prefix="/api/edulevels")
    app.register_blueprint(edumajor_bp, url_prefix="/api/edumajors")
    app.register_blueprint(eduinstitution_bp, url_prefix="/api/eduinstitutions")
    app.register_blueprint(maritalstatus_bp, url_prefix="/api/maritalstatuses")
    app.register_blueprint(city_bp, url_prefix="/api/cities")
    app.register_blueprint(religion_bp, url_prefix="/api/religions")
    app.register_blueprint(site_bp, url_prefix="/api/sites")
    app.register_blueprint(kecamatan_bp, url_prefix="/api/kecamatans")
    app.register_blueprint(jobtitle_bp, url_prefix="/api/jobtitles")
    app.register_blueprint(vacantpos_bp, url_prefix="/api/vacancies")
    app.register_blueprint(posadtgrphd_bp, url_prefix="/api/posadtgrphd")
    app.register_blueprint(posadtgrpdt_bp, url_prefix="/api/posadtgrpdt")
    app.register_blueprint(state_bp, url_prefix="/api/states")
    app.register_blueprint(cardtype_bp, url_prefix="/api/cardtypes")
    app.register_blueprint(questtopic_bp, url_prefix="/api/questtopics")
    app.register_blueprint(question_bp, url_prefix="/api/questions")
    app.register_blueprint(candidate_bp, url_prefix="/api/candidates")
    app.register_blueprint(race_bp, url_prefix="/api/races")

    # Custom JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"message": "Token has expired", "error": "token_expired"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"message": "Invalid token", "error": "invalid_token"}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {"message": "Authorization token is missing", "error": "authorization_required"}, 401

    return app

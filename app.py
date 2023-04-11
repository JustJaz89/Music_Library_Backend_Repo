from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from marshmallow import post_load, fields, ValidationError
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Song(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    artist = db.Column(db.String(255), nullable = False)
    album = db.Column(db.String(255), nullable = False)
    genre = db.Column(db.String(255), nullable = False)
    release_date = db.Column(db.Date)
    running_time = db.Column(db.Float)
    

    def __repr__(self):
        return f"{self.title} {self.artist} {self.album} {self.genre} {self.release_date} {self.running_time}"

# Schemas
class SongSchema(ma.Schema):
    id = fields.Integer(primary_key = True)
    title = fields.String(required = True)
    artist = fields.String(required = True)
    album = fields.String(required = True)
    genre = fields.String(required = True)
    release_date = fields.Date()
    running_time = fields.Float()
    

    class Meta:
        fields = ("title", "artist", "album", "genre", "release_date", "running_time")

    @post_load
    def create_song(self, data, **kwargs):
        return Song(**data)

song_schema = SongSchema()
songs_schema = SongSchema(many = True)


# Resources
class SongListResource(Resource):
    def get(self):
        all_songs = Song.query.all()
        return songs_schema.dump(all_songs)
    
    def post(self):
        form_data = request.get_json()
        try:
            new_song = song_schema.load(form_data)
            db.session.add(new_song)
            db.session.commit()
            return song_schema.dump(new_song), 201
        except ValidationError as err:
            return err.messages, 400

class SongResource(Resource):
    def get(self, song_id):
        song_from_db = Song.query.get_or_404(song_id)
        return song_schema.dump(song_from_db), 200
    
    def put(self, song_id):
        song_from_db = Song.query.get_or_404(song_id)
        if "title" in request.json:
            song_from_db.title = request.json["title"]
        if "artist" in request.json:
            song_from_db.artist = request.json["artist"]
        if "album" in request.json:
            song_from_db.album = request.json["album"]
        if "genre" in request.json:
            song_from_db.genre = request.json["genre"]
        if "release_date" in request.json:
            song_from_db.release_date = request.json["release_date"]
        if "running_time" in request.json:
            song_from_db.running_time = request.json["running_time"]
        db.session.commit()
        return song_schema.dump(song_from_db), 200
    
    def delete(self, song_id):
        song_from_db = Song.query.get_or_404(song_id)
        db.session.delete(song_from_db)
        return "", 204

# Routes
api.add_resource(SongListResource, "/api/songs")
api.add_resource(SongResource, "/api/songs/<int:song_id>")
from flask import Flask, request, session, make_response, jsonify
from flask_restful import Api, Resource
from models import db, bcrypt, User, JournalEntry
from flask_migrate import Migrate
import os
#use of resources using flask=RESTFUL instead of @app.route
#Class based resources -
#initialise Flask

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = "dev-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'production.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False  
app.config['SESSION_COOKIE_HTTPONLY'] = True

#initialise extensions
db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def login_required(func):
    #Decoratoe to protect the routes
    def wrapper(*args,**kwargs):
        if not get_current_user():
            return {"error": "Unauthorized - Please log in"}, 401
        return func(*args, **kwargs)
    return wrapper

class Signup(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return {"error": "Username and password required"}, 400
        
        if User.query.filter_by(username=data['username']).first():
            return {"error": "Username already exists"}, 400
        
        try:
            new_user = User(username=data['username'])
            new_user.password_hash = data['password']
            
            db.session.add(new_user)
            db.session.commit()
            
            #To auto login
            session['user_id'] = new_user.id
            
            return new_user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        
class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id
            return user.to_dict(), 200

        return {"error": "Invalid username or password"}, 401
    
class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class CheckSession(Resource):
    def get(self):
        user = get_current_user()
        if user:
            return user.to_dict(), 200
        return {"error": "Not logged in"}, 401
    
class JournalList(Resource):
    @login_required
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        user = get_current_user()

        pagination = JournalEntry.query.filter_by(user_id=user.id)\
            .order_by(JournalEntry.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        entries = [entry.to_dict() for entry in pagination.items]
        
        return {
            "entries": entries,
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "per_page": pagination.per_page
        }, 200
        
    @login_required
    def post(self):
        data = request.get_json()
        user = get_current_user()
            
        if not data or not data.get('title') or not data.get('content'):
            return {"error": "Title and content are required"}, 400
        
        new_entry = JournalEntry(
            title=data['title'],
            content=data['content'],
            mood=data.get('mood'),
            user_id=user.id
        )
        
        db.session.add(new_entry)
        db.session.commit()
        
        return new_entry.to_dict(), 201
    
class JournalResource(Resource):
    @login_required
    def get(self, id):
        
        user = get_current_user()
        entry = JournalEntry.query.filter_by(id=id, user_id=user.id).first()
        
        if not entry:
            return {"error": "Journal entry not found or access denied"}, 404
        return entry.to_dict(), 200
    
    @login_required
    def patch(self, id):
        """PATCH /journals/<id>"""
        user = get_current_user()
        entry = JournalEntry.query.filter_by(id=id, user_id=user.id).first()
        
        if not entry:
            return {"error": "Journal entry not found or access denied"}, 404
        
        data = request.get_json()
        if data.get('title'):
            entry.title = data['title']
        if data.get('content'):
            entry.content = data['content']
        if data.get('mood') is not None:
            entry.mood = data['mood']
            
        db.session.commit()
        return entry.to_dict(), 200
    
    @login_required
    def delete(self, id):
        user = get_current_user()
        entry = JournalEntry.query.filter_by(id=id, user_id=user.id).first()

        if not entry:
            return {"error": "Journal entry not found or access denied"}, 404
        
        db.session.delete(entry)
        db.session.commit()
        return {}, 204

#Regiter resources
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

api.add_resource(JournalList, '/journals')
api.add_resource(JournalResource, '/journals/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
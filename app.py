from flask import Flask, request, jsonify, Blueprint
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
import datetime
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash

# create an instance of flask
app = Flask(__name__)

# create api object
api = Api(app)
# create db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cv.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# sqlalchemy mapper
db = SQLAlchemy(app)

CORS(app)


@app.route("/")
class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'{self.username}-{self.password}'


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = Login.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    if check_password_hash(user.password, password):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return jsonify({'message': 'Invalid username or password'}), 401


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    nationality = db.Column(db.String(30), nullable=False)
    interests = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.age} - {self.nationality} - {self.interests}"


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institute = db.Column(db.String(30), nullable=False)
    course = db.Column(db.String(30), nullable=False)
    duration = db.Column(db.String(30), nullable=False)
    score = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"{self.institute} - {self.course} - {self.duration} - {self.score}"


class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(30), nullable=False)
    company = db.Column(db.String(30), nullable=False)
    duration = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{self.role} - {self.company} - {self.duration} - {self.description}"


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    level = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Float)

    def __repr__(self):
        return f"{self.name} - {self.level} - {self.rating}"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    technologies = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{self.title} - {self.technologies} - {self.description}"


class GetAbout(Resource):
    def get(self):
        abouts = About.query.all()
        educ_list = []
        for info in abouts:
            info_data = {'Id': info.id, 'Nombre': info.name, 'Edad': info.age, 'Nacionalidad': info.nationality,
                         'Intereses': info.interests, 'Descripcion': info.description}
            educ_list.append(info_data)
        return {"About": educ_list}, 200


class UpdateAbout(Resource):
    def put(self, id):
        if request.is_json:
            info = Education.query.get(id)
            if info is None:
                return {'error': 'not found'}, 404
            else:
                info.name = request.json['Nombre']
                info.age = request.json['Edad']
                info.nationality = request.json['Nacionalidad']
                info.interests = request.json['Intereses']
                info.description = request.json['Descripcion']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400


class GetEducation(Resource):
    def get(self):
        educacion = Education.query.all()
        educ_list = []
        for edu in educacion:
            edu_data = {'Id': edu.id, 'Instituto': edu.institute, 'Curso': edu.course, 'Duracion': edu.duration,
                        'Puntaje': edu.score}
            educ_list.append(edu_data)
        return {"Educacion": educ_list}, 200


class UpdateEducation(Resource):
    def put(self, id):
        if request.is_json:
            edu = Education.query.get(id)
            if edu is None:
                return {'error': 'not found'}, 404
            else:
                edu.institute = request.json['Instituto']
                edu.course = request.json['Curso']
                edu.duration = request.json['Duracion']
                edu.score = request.json['Puntaje']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400


class GetWorkExperience(Resource):
    def get(self):
        works = WorkExperience.query.all()
        works_list = []
        for work in works:
            work_data = {'Id': work.id, 'Rol': work.role, 'Compañia': work.company, 'Duracion': work.duration,
                         'Descripcion': work.description}
            works_list.append(work_data)
        return {"Experiencia": works_list}, 200


class UpdateWorkExperience(Resource):
    def put(self, id):
        if request.is_json:
            work = WorkExperience.query.get(id)
            if work is None:
                return {'error': 'not found'}, 404
            else:
                work.role = request.json['Rol']
                work.company = request.json['Compañia']
                work.duration = request.json['Duracion']
                work.description = request.json['Descripcion']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400


class GetSkill(Resource):
    def get(self):
        skills = Skill.query.all()
        skills_list = []
        for skill in skills:
            skill_data = {'Id': skill.id, 'Nombre': skill.name, 'Nivel': skill.level, 'Rango': skill.rating}
            skills_list.append(skill_data)
        return {"Habilidades": skills_list}, 200


class UpdateSkill(Resource):
    def put(self, id):
        if request.is_json:
            skill = Skill.query.get(id)
            if skill is None:
                return {'error': 'not found'}, 404
            else:
                skill.name = request.json['Nombre']
                skill.level = request.json['Nivel']
                skill.rating = request.json['Rango']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400


class GetProject(Resource):
    def get(self):
        projects = Project.query.all()
        project_list = []
        for project in projects:
            project_data = {'Id': project.id, 'Titulo': project.title, 'Tecnologias': project.technologies,
                            'Descripcion': project.description}
            project_list.append(project_data)
        return {"Proyectos": project_list}, 200


class UpdateProject(Resource):
    def put(self, id):
        if request.is_json:
            project = Project.query.get(id)
            if project is None:
                return {'error': 'not found'}, 404
            else:
                project.title = request.json['Titulo']
                project.technologies = request.json['Tecnologias']
                project.description = request.json['Descripcion']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400


api.add_resource(GetAbout, '/get_about')
api.add_resource(UpdateAbout, '/upt_about/<int:id>')
api.add_resource(GetEducation, '/get_edu')
api.add_resource(UpdateEducation, '/upt_edu/<int:id>')
api.add_resource(GetWorkExperience, '/get_exp')
api.add_resource(UpdateWorkExperience, '/upt_exp/<int:id>')
api.add_resource(GetSkill, '/get_skill')
api.add_resource(UpdateSkill, '/upt_skill/<int:id>')
api.add_resource(GetProject, '/get_project')
api.add_resource(UpdateProject, '/upt_project/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)

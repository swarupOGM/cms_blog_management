from flask import Flask, render_template, request, redirect, session, g, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, history
import requests
from os import environ
import uuid
from base64 import b64encode
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
print()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@localhost/{}'.format(environ['DB_USER'],environ['DB_PASS'], environ['DB_DATABASE'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@localhost/{}'.format('aggdirect1','IamSwarup1', 'growealth')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'somesecretkeythatonlyishouldknow'
migrate=Migrate(app,db) #Initializing migrate.

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def generate_uuid():
    return str(uuid.uuid4())

##modele for role master
class Blog(db.Model):
    id = db.Column(db.String(100), primary_key=True, default=generate_uuid)
    blog_title = db.Column(db.String(100), unique=True, nullable=False)
    blog_description = db.Column(db.String(500), nullable=False)
    created_by = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    image_name = db.Column(db.String(200), unique=True, nullable=True)
    image = db.Column(db.LargeBinary(length=16777216))

    def __repr__(self) -> str:
        return f"{self.id} - {self.role_title}"

#blog comment
class Comment(db.Model):
    id = db.Column(db.String(100), primary_key=True, default=generate_uuid)
    comment_txt = db.Column(db.String(1000), nullable=False)
    blog_id = db.Column(db.String(100), db.ForeignKey('blog.id'), nullable=False)
    created_by = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.blog_id} - {self.comment_txt}"
#declaring the user model
class User(db.Model):
    id = db.Column(db.String(100), primary_key=True, default=generate_uuid)
    first_name = db.Column(db.String(100), unique=False, nullable=True)
    last_name = db.Column(db.String(100), unique=False, nullable=True)
    username = db.Column(db.String(80), unique=False, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    contact_no = db.Column(db.String(15), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    profile_image_name = db.Column(db.String(255), nullable=True)
    profile_image = db.Column(db.LargeBinary(length=16777216))


    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"
    ## method to get the full name
    def full_name(self):
        return self.first_name + ' ' + self.last_name 



@app.route('/growealth', methods=['GET'])
def index_page():
    blog = Blog.query.all()
    return render_template('index.html', blogs=blog)

#reset password
@app.route('/password/reset',methods=['GET','POST'])
def reset_password():
    message = None
    admin_user = User.query.first()
    if request.method =='POST':
        print("under the id")
        user_name = request.form.get('username')
        last_passowrd = request.form.get('last_password')
        password = request.form.get('password')
        user_obj = User.query.filter_by(username=user_name, password=last_passowrd).first()
        if user_obj:
            user_obj.password = password if password else last_passowrd
            db.session.add(user_obj)
            db.session.commit()
            print("this is under if")
            session.pop('username',None)
            session.pop('user_id',None)
            return redirect(url_for('profile'))
        message = "Last Password is not correct!"
    
    if 'user_id' in session:
        return render_template('reset_password.html', all_employee=admin_user, message=message)
    else:
        return redirect(url_for('login'))



##delete blog
@app.route('/delete/blog/<id>',methods=['GET'])
def deleteblog(id):
    if request.method=='GET':
        print("under the id")
        if Blog.query.filter_by(id=id).first() is not None:
            print("in")
            blog_obj = Blog.query.filter_by(id=id).one()
            db.session.delete(blog_obj)
            db.session.commit()
            blog = Blog.query.all()           
            admin_user = User.query.first()
            message = "Deleted Successfully!"
            return render_template('blog_list.html', all_employee=admin_user, blogs=blog, message=message)
    if 'user_id' in session:
        return redirect(url_for("blog_list"))
    else:
        return redirect(url_for('login'))
#edit blog
@app.route('/edit/blog/<id>', methods=['GET', 'POST'])
def edit_blog(id):
    if request.method=='GET':
        print("under the id")
        blog_obj = Blog.query.filter_by(id=id).first()
    elif request.method == 'POST':
        blog_obj = Blog.query.filter_by(id=id).first()
        blog_obj.blog_title = request.form.get('title')
        blog_obj.blog_description = request.form.get('desc')
        db.session.add(blog_obj)
        db.session.commit()
        blog = Blog.query.all()           
        admin_user = User.query.first()
        message = "Updated Successfully!"
        return render_template('blog_list.html', all_employee=admin_user, blogs=blog, message=message)
    admin_user = User.query.first() 
    if 'user_id' in session:
        return render_template('blog_edit.html', all_employee=admin_user, blog=blog_obj )
    else:
        return redirect(url_for('login'))

@app.route('/add/blog/', methods=['GET', 'POST'])
def add_blog():
    if request.method=='POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        image = request.files.get('image')
        #image save
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
        image.save(path)
        blog = Blog(blog_title=title, blog_description=desc, created_by=session['user_id'], date_created=datetime.now(),
                    image_name=image.filename, image=image.read())        
        db.session.add(blog)
        db.session.commit()   
    admin_user = User.query.first() 
    # all_role = role.query.all()
    # print(all_role)
    if 'user_id' in session:
        return render_template('personnel.html', all_employee=admin_user )
    else:
        return render_template('employee_login.html')


@app.route('/blog/list/', methods=['GET'])
def blog_list():
    if request.method=='GET':
        blog = Blog.query.all()           
    admin_user = User.query.first() 
    # all_role = role.query.all()
    # print(all_role)
    if 'user_id' in session:
        return render_template('blog_list.html', all_employee=admin_user, blogs=blog )
    else:
        return render_template('employee_login.html')


############################################## ADD EMPLOYEE VIEW ##################################################################
##edit admin profile
@app.route('/edit/profile/', methods=['GET', 'POST'])
def register_employee():
    admin_user = User.query.first()
    if request.method=='POST':
        user = User.query.first()
        print(user.username)
        user.email = request.form.get('email')
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.contact_no = request.form.get('phone')
        profile_image = request.files.get('profile_photo')
        print(request.files.get('profile_photo'))
        user.profile_image = profile_image.read()
        user.profile_image_name = profile_image.filename
        #image save
        profile_image.seek(0)
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(profile_image.filename))
        profile_image.save(path)
        # user.profile_image = photo
        db.session.add(user)
        db.session.commit()
        message = "Profile Updated Successfully!"
        return render_template('edit_profile.html', all_employee=admin_user, message=message)   
     
    # all_role = role.query.all()
    # print(all_role)
    if 'user_id' in session:
        return render_template('edit_profile.html', all_employee=admin_user )
    else:
        return render_template('employee_login.html')


############################################## SESSION CHECK ##################################################################
## execute before requesting every endpoint to check that the user is still logged in or not
@app.before_request
def before_request():
    g.user = None
    users = User.query.all()
    if 'user_id' in session:
        try:
            user = [x for x in users if x.id == session['user_id']]
            if user:
                g.user = user
        except:
            pass

############################################## EMPLOYEE LOGIN VIEW ##################################################################      

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("in login")
        # session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        user = [x for x in users if x.username == username]
        if user:
            user = user[0]
            print(check_password_hash(user.password, password))
            if user.is_admin:
                session['user_id'] = user.id
                return redirect(url_for('register_employee',  user=user.is_admin))
            elif user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                print("in if")
                # print(user)
                if user.is_admin:
                    return redirect(url_for('register_employee',  user=user.is_admin))
                else:
                    return redirect(url_for('search_stock',  user=user.is_admin))


            else:
                message = "the username and password you entered is incorrect"
            return render_template('login.html', message=message)
        else:
            message = "the username and password you entered is incorrect"
            return render_template('login.html', message=message)

            
        

    return render_template('login.html')

##setup the default route
@app.route('/')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return redirect(url_for('register_employee'))


############################################## LOGOUT VIEW ##################################################################
@app.route('/logout/')
def logout():
    session.pop('username',None)
    session.pop('user_id',None)
    return redirect(url_for('profile'))



if __name__ == "__main__":
    app.run(debug=True)

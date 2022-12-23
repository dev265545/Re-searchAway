from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json



# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='devarchitekansh'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get((user_id))



# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost:3307/project'
db=SQLAlchemy(app)


# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))


class Paper(db.Model):
    P_ID = db.Column(db.Integer, primary_key=True)
    auth_id=db.Column(db.String(50))
    Title = db.Column(db.String(50))
    Abstract = db.Column(db.Text)
    Publisher_id = db.Column(db.Integer)
    Field_Of_research = db.Column(db.String(50))
    Date_of_Publish = db.Column(db.Date)
    likes = db.Column(db.Integer)

class Publisher(db.Model):
    pub_id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(100))
    # cid=db.Column(db.Integer,primary_key=True)
    # branch=db.Column(db.String(100))

    # cid=db.Column(db.Integer,primary_key=True)
    # branch=db.Column(db.String(100))    

class Attendence(db.Model):
    aid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(100))
    attendance=db.Column(db.Integer())

class Trig(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.String(50),primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
class LikedPaper(db.Model):
    liked_user_id = db.Column(db.String(50), db.ForeignKey(User.id),primary_key=True )
    liked_p_id = db.Column(db.String(50), db.ForeignKey(Paper.P_ID),primary_key=True )
class to_be_read(db.Model):
    user_id_read = db.Column(db.String(50), db.ForeignKey(User.id),primary_key=True )
    read_p_id = db.Column(db.String(50), db.ForeignKey(Paper.P_ID),primary_key=True )    





    

@app.route('/')
def index(): 
    # print(current_user.id)
    return render_template('index.html')

@app.route('/displaypapers')
def displaypapers():
    query=db.engine.execute(f"SELECT * FROM `paper` JOIN `user` ON user.id = paper.auth_id JOIN `publisher` ON publisher.Pub_id = paper.Publisher_id") 
    return render_template('displaypapers.html',query=query)
@app.route('/likedpapers')
def likedpapers():
    query=db.engine.execute(f"SELECT * FROM `paper` JOIN `user` ON user.id = paper.auth_id JOIN `publisher` ON publisher.Pub_id = paper.Publisher_id join liked_paper on liked_paper.liked_user_id='{current_user.id}'and liked_paper.liked_p_id=paper.P_ID ") 
    return render_template('likedpapers.html',query=query)
@app.route('/bookmarkedpapers')
def bookmarkedpapers():
    query=db.engine.execute(f"SELECT * FROM `paper` JOIN `user` ON user.id = paper.auth_id JOIN `publisher` ON publisher.Pub_id = paper.Publisher_id join to_be_read on to_be_read.user_id_read='{current_user.id}'and to_be_read.read_p_id=paper.P_ID ") 
    return render_template('bookmarkedpapers.html',query=query)         

@app.route('/searchbypublisher',methods=['POST','GET'])
def searchbypublisher():
    pub=db.engine.execute(f"SELECT * FROM `publisher`")
    if request.method=="POST":
        branch=request.form.get('publisher')
        
        query=db.session.query(
    User.name, Paper.Title,Paper.Abstract,Paper.Date_of_Publish,Paper.Field_Of_research, Publisher.Name).filter( User.id == Paper.auth_id).filter(Paper.Publisher_id == Publisher.pub_id).filter(Publisher.pub_id== branch ).all()
       
        return render_template('searchbypublisher.html',pub=pub,bio=query)

    return render_template('searchbypublisher.html',pub=pub)

@app.route('/publisher',methods=['POST','GET'])
def publisher():
    if request.method=="POST":
        pub=request.form.get('pub')
        query=Publisher.query.filter_by(name=pub).first()
        if query:
            flash("Publisher Already Exist","warning")
            return redirect('/publisher')
        pub=Publisher(name=pub)
        db.session.add(pub)
        db.session.commit()
        flash("Publisher Added","success")
    return render_template('publisher.html')





@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=="POST":
        branch=request.form.get('roll')
        br = "%{}%".format(branch)
        bio=Paper.query.filter(Paper.Field_Of_research.like(br)).first()
       
        return render_template('search.html',bio=bio)
        
    return render_template('search.html')


@app.route('/searchbyaid', methods=['POST', 'GET'])
def searchbyaid():
    query=db.engine.execute(f"SELECT * FROM `paper` JOIN `user` ON user.id = paper.auth_id JOIN `publisher` ON publisher.Pub_id = paper.Publisher_id where user.id ='{current_user.id}'") 
    return render_template('searchbyaid.html', bio=query)

    


@app.route('/searchbyname', methods=['POST', 'GET'])
def searchbyname():
    if request.method == "POST":
        branch = request.form.get('aname')
        br="%{}%".format(branch)
        query=db.session.query(
    User.name, Paper.Title,Paper.Abstract,Paper.Date_of_Publish,Paper.Field_Of_research, Publisher.Name).filter( User.id == Paper.auth_id).filter(Paper.Publisher_id == Publisher.pub_id).filter(User.name.like(br)).all()
        
        return render_template('searchbyname.html',bio=query)
        

    return render_template('searchbyname.html')


# @app.route("/delete/<string:id>",methods=['POST','GET'])
# @login_required
# def delete(id):
#     db.engine.execute(f"DELETE FROM `paper` WHERE `paper`.`id`={id}")
#     flash("Slot Deleted Successful","danger")
#     return redirect('/paperdetails')


@app.route("/edit/<string:P_ID>/<string:id>",methods=['POST','GET'])
@login_required
def edit(P_ID,id):
    posts=Paper.query.filter_by(P_ID=P_ID).filter_by(auth_id=id).first()
    isliked=LikedPaper.query.filter_by(liked_user_id=current_user.id).filter_by(liked_p_id=P_ID).first()
    print(isliked)
    if isliked == None:
        print(isliked)
        likes = posts.likes +1
        db.engine.execute(f"UPDATE `paper` SET `likes`='{likes}' WHERE `paper`.`P_ID`={posts.P_ID}")
        db.engine.execute(f"INSERT INTO `liked_paper` (`liked_user_id`,`liked_p_id`) VALUES ('{current_user.id}','{P_ID}')")
        flash("You liked this Paper","success")
        return redirect('/displaypapers')

    
    flash("Already liked by you","success")
    return redirect('/displaypapers')
    
@app.route("/toberead/<string:P_ID>/<string:id>",methods=['POST','GET'])
@login_required
def bookmarked(P_ID,id):
    posts=Paper.query.filter_by(P_ID=P_ID).filter_by(auth_id=id).first()
    isbookmarked=to_be_read.query.filter_by(user_id_read=current_user.id).filter_by(read_p_id=P_ID).first()
    print(isbookmarked)
    if isbookmarked == None:
        print(isbookmarked)
        # likes = posts.likes +1
        # db.engine.execute(f"UPDATE `paper` SET `likes`='{likes}' WHERE `paper`.`P_ID`={posts.P_ID}")
        db.engine.execute(f"INSERT INTO `to_be_read` (`user_id_read`,`read_p_id`) VALUES ('{current_user.id}','{P_ID}')")
        flash("You bookmarked this paper","success")
        return redirect('/displaypapers')

    
    flash("Already bookmakred by you","success")
    return redirect('/displaypapers')
    
    
    


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        id = request.form.get('user_id')
        name=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`id`,`name`,`email`,`password`) VALUES ('{id}','{name}','{email}','{encpassword}')")

        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addpaper',methods=['POST','GET'])
@login_required
def addpaper():
    dept=db.engine.execute("SELECT * FROM `publisher`")
    if request.method=="POST":
        auth_id = request.form.get('auth_id')
        papername=request.form.get('papername')
        date=request.form.get('date')
        link=request.form.get('link')
    
        publisher=request.form.get('publisher')
        abstract=request.form.get('abstract')
        field=request.form.get('field')
      
        query=db.engine.execute(f"INSERT INTO `paper` (`Title`, `Abstract`, `Field_Of_research`, `Publisher_id`, `Date_of_Publish`,`auth_id`,`link`) VALUES('{papername}','{abstract}', ' {field} ', '{publisher}', '{date}','{auth_id}','{link}')")
        flash("Paper Added into the Database","info")


    return render_template('paper.html',dept=dept)


app.run(debug=True)    
from .database import db

class admin(db.Model):
    __tablename__='admin'
    admin_id =db.Column(db.Integer, autoincrement=True, primary_key=True,unique=True)
    username=db.Column(db.String, unique=True)
    password=db.Column(db.String, unique=True)


class user(db.Model):
    __tablename__='user'
    user_id =db.Column(db.Integer, autoincrement=True, primary_key=True)
    username=db.Column(db.String, unique=True)
    password=db.Column(db.String, unique=True)
    books_issued=db.Column(db.Integer)


class section(db.Model):
    __tablename__='section'
    section_id =db.Column(db.Integer, autoincrement=True, primary_key=True)
    admin_id=db.Column(db.Integer, db.ForeignKey("admin.admin_id"))
    title=db.Column(db.String, unique=True)
    date =db.Column(db.Integer)
    image=db.Column(db.String)
    description=db.Column(db.String)


class books(db.Model):
    __tablename__='books'
    sec_id =db.Column(db.Integer, db.ForeignKey("section.section_id"))
    section=db.Column(db.String)
    book_id=db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    user_issued=db.Column(db.Integer,db.ForeignKey("user.user_id"))
    Title =db.Column(db.String)
    Author=db.Column(db.String )
    Content=db.Column(db.String )
    Image=db.Column(db.String)
    file =db.Column(db.String)

class book_issue(db.Model):
    __tablename__='book_issue'
    issue_id =db.Column(db.Integer, autoincrement=True, primary_key=True)
    title=db.Column(db.String, db.ForeignKey("books.book_id"),unique=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.user_id"),unique=True)
    admin_id =db.Column(db.Integer )
    date_issue=db.Column(db.Date)
    date_return=db.Column(db.Date)
    days_left=db.Column(db.Integer)
    book_id=db.Column(db.Integer)
class allotment(db.Model):
    __tablename__="allotment"
    req_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id=db.Column(db.Integer)
    title=db.Column(db.Integer, db.ForeignKey("books.Title"))
    user_id=db.Column(db.Integer, db.ForeignKey("user.user_id"))
    status=db.Column(db.String ,default='UnderProcess')
    date=db.Column(db.Date)

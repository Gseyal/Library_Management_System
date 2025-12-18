from flask import Flask
from flask import flash
from flask import request
from flask import render_template
from flask import current_app as app
from flask import redirect
from flask import current_app as app
import os
from io import BytesIO
import base64
from application.models import *
from .database import db
from .database import engine
from datetime import date,timedelta,datetime
import matplotlib
matplotlib.use('svg')
from matplotlib import pyplot as plt
from sqlalchemy.sql import text
from sqlalchemy import select
global id
id=1
#route to starting app
@app.route("/",methods=["GET","POST"])
def hello():
    return render_template("Login_2.html")
#route to return to the logined user_dash
@app.route("/Homepage")
def home():
    client=request.args.get('client')
    my_dict=section.query.all()
    user_id=id
    return render_template("admin_dashboard.html",data=my_dict,name=client,id=user_id)
#route to login in the app with /login?client=ADMIN and replicate the user_id to the global variable
@app.route("/login",methods=["GET","POST"])
def check():
    client=request.args.get('client')
    login=request.form['User']
    password=request.form['passw']
    if client=='ADMIN':
        data=admin.query.filter_by(username=login).first()
        if data.password==password:
                global id
                id=data.admin_id
                user_id= data.admin_id
        else:
           
            return redirect('/')
        
    else:
        data=user.query.filter_by(username=login).first()
        if data and data.password==password:
           
           id=data.user_id
           user_id= data.user_id
        else:
            return redirect('/')
    my_dict=section.query.all()
    return render_template("admin_dashboard.html",data=my_dict,name=client,id=user_id)
# route to register new user only
@app.route('/register',methods=['GET','POST'])
def register():
    login=request.form['User']
    password=request.form['passw']
    
    to_add=user(username=login,password=password,books_issued=0)
    db.session.add(to_add)
    db.session.commit()
    db.session.close()
    return redirect('/')
#route to logout from any point in the library(both ADMIN or USER)
@app.route("/logout",methods=["GET","POST"])
def logout():
    return redirect("/")
#route to add sections in the Library (only ADMIN)
@app.route("/add", methods=["GET","POST"])
def add():
    client=request.args.get('client')
    path=r'templates'
    title=request.form["title"]
    date=request.form['date']
    image=request.form['image']
    description=request.form['description']
    
    global id
    new_item=section(title=title,date=date,image=image,description=description,admin_id=id)
    db.session.add(new_item)
    db.session.commit()

    Template_file=open('template.html')
    content=Template_file.read()
    Template_file.close()
    file_name=request.form["title"]+".html"
    file=open(os.path.join(path,file_name),'w')
    file.write(content)
    file.close()
    my_dict=section.query.all()
    return render_template("admin_dashboard.html",data=my_dict,name=client)
#route to deleter sections along with section books in the Library only admin has access to this function (only ADMIN)
@app.route('/delete_section',methods=["GET","POST"])
def delete():
    title=request.args.get('title')
    name=request.args.get('client')
    section.query.filter_by(title=title).delete()
    db.session.commit()
    books.query.filter_by(section=title).delete()
    db.session.commit()
    path=r'templates'
    file_name=title+".html"
    os.remove(os.path.join(path,file_name))
    togo="/Homepage?client="+name
    return redirect(togo)
#funtion route to delete the book in the section without disturbing the whole section (only ADMIN)
@app.route('/delete_section_book', methods=["GET","POST"])
def book_del():
    client=request.args.get('client')
    page=request.args.get('section')
    book=request.args.get('book')
    books.query.filter_by(Title=book).delete()
    db.session.commit()
    x=page+".html"
    data=db.session.query(books).filter(books.section==page).all()
    return render_template(x,data=data,name=page,client=client)
#this route will check for every section to have their books on show and don't end up mixed
@app.route('/section_books',methods=["GET","POST"])
def move():
    sect_id=request.args.get('sect_id')
    page=request.args.get('page')
    name=request.args.get('who')
    x=page+".html"
    if name=='USER':
        data=books.query.filter_by(user_issued='NONE',section=page).all()
    else:
        data=db.session.query(books).filter(books.section==page).all()
    return render_template(x,data=data,client=name,name=page,sect_id=sect_id)
#funtion to add books in the books table in LIb.db (only ADMIN)
@app.route('/add_books',methods=["GET","POST"])
def book():
    sect=request.args.get('section')
    row=section.query.filter_by(title=sect).first()
    sect_id=int(row.section_id)
    client=request.args.get('client')
    Title=request.form['title']
    Author=request.form['Author']
    file=request.form['file']
    Content=request.form['description']
    Image=request.form['image']
    print(Image)
    
    new_item=books(file=file,section=sect,user_issued='NONE',Title=Title,Author=Author,Content=Content,Image=Image,sec_id=sect_id)
    db.session.add(new_item)
    db.session.commit()
    togo="/section_books?page="+ sect + "&who="+client
    return redirect(togo)
#function to issue a book to a user (only ADMIN)
@app.route('/issued',methods=["GET","POST"])
def accepted():
    bookid=request.args.get('bookid')
    reqid=request.args.get('reqid')
    client=request.args.get('client')
    data=allotment.query.filter_by(req_id=reqid).first()
    #1st action, books detail will copied to book_issue
    add_data=book_issue(title=data.title,user_id=data.user_id,date_issue=date.today(),book_id=bookid,date_return=date.today()+timedelta(days=7),days_left=7)
    db.session.add(add_data)
    db.session.commit()
    #2nd action, status in request made is changed 
    row=allotment.query.filter_by(req_id=reqid).first()
    row.status='Accepted'
    db.session.commit()
    #3rd action, user's id is attached to the book for the admin
    update=books.query.filter_by(book_id=bookid).first()
    update.user_issued=data.user_id
    db.session.commit()
    #update total books issued to a user over acceptance
    data=allotment.query.filter_by(req_id=reqid).first()
    user_id=data.user_id
    limit=user.query.filter_by(user_id=user_id).first()
    limit.books_issued= int(limit.books_issued)+1
    db.session.commit()
    togo="/request?client="+client
    return redirect(togo)
#function to reject a request (only ADMIN)
@app.route('/rejected',methods=["GET","POST"])
def rejected():
        reqid=request.args.get('reqid')
        client=request.args.get('client')
        row=allotment.query.filter_by(req_id=reqid).first()
        row.status='Rejected'
        db.session.commit()
        
        togo="/request?client="+client
        return redirect(togo)
#function to see requests for a book (Admin/ only user requested)
@app.route('/request',methods=['GET','POST'])
def request_page():
    client=request.args.get('client')
    if client=='ADMIN':
        data=allotment.query.filter_by(status="UnderProcess" ).all()
    else:
        data=allotment.query.filter_by(user_id=id).all()
    return render_template("request.html",data=data,client=client,id=id)
#function to request (only user)
@app.route('/user_requested')
def requested():
    client=request.args.get("client")
    user_id=request.args.get("user_id")
    title=request.args.get("title")
    book_id=request.args.get('bookid')
    
    add_data=allotment(book_id=book_id,user_id=id,title=title,status='UnderProcess',date=date.today())
    db.session.add(add_data)
    db.session.commit()
    togo="/request?client="+client
    return redirect(togo)
#function to see issued book to a user (indiviual user)
@app.route('/user_book')
def user_lib():
    client=request.args.get("client")
    user_id=id
    data=book_issue.query.filter_by(user_id=user_id).all()
    return render_template("user_book_show.html",data=data,name=client) 
#funtion to visit page to see books (only admin)
@app.route('/action')
def action():
    rows=book_issue.query.all()
    for row in rows:
        row.days_left=(row.date_return - datetime.now().date()).days
        db.session.commit()
    data=book_issue.query.all()
    return render_template("action.html",data=data,client='ADMIN')
#funtion to revoke any issued book (only Admin and similar protocol to return book)
@app.route('/revoke')
def revoke():
    client=request.args.get('who')
    issue_id=request.args.get('issid')
    book=book_issue.query.filter_by(issue_id=issue_id).first()
    bookid=book.book_id
    user_id=book.user_id
    book_issue.query.filter_by(issue_id=issue_id).delete()
    db.session.commit()
    row=books.query.filter_by(book_id=bookid).first()
    row.user_issued='NONE'
    db.session.commit()
    limit=user.query.filter_by(user_id=user_id).first()
    limit.books_issued= int(limit.books_issued)-1
    db.session.commit()
    if client=='ADMIN':
        togo='/action'
        return  redirect(togo)
    else:
        togo='/user_book?client='+client
        return redirect(togo)
@app.route('/stat',methods=["GET","POST"])
def stat():
    client=request.args.get('client')
    data=graph()
    return render_template("stat.html",name=client,data=data)
def graph():
    path=r'static'
    query=text('SELECT section.title ,count(books.Title)from section LEFT JOIN books ON books.sec_id=section.section_id GROUP BY section.title')
    data=db.session.execute(query).all()
    section,count=zip(*data)

    query2=text("SELECT section.title ,count(books.Title)from section LEFT JOIN books ON books.sec_id=section.section_id and books.user_issued!='NONE' GROUP BY section.title")
    data2=db.session.execute(query2).all()
    a,b=zip(*data2)

    plt.bar(section,count,width=1, edgecolor="white", linewidth=0.7)
    plt.bar(section,b,width=1, edgecolor="white", linewidth=0.7)
    plt.xlabel("SECTIONS")
    plt.ylabel("COUNT")
    plt.savefig(os.path.join(path,'image.png'))
    plt.close()
    plt.pie(count,labels=section)
    plt.legend(data,loc='best')
    donut=plt.Circle((0,0), 0.7, color='white')
    p=plt.gcf()
    p.gca().add_artist(donut)
    plt.savefig(os.path.join(path,'image2.png'))
    plt.close()
    return data
@app.route('/search',methods=["GET","POST"])
def search():
    client=request.args.get('client')
    x=request.form['what']
    data=section.query.filter_by(title=x).all()
    return render_template("admin_dashboard.html",data=data,name=client,id=id)
@app.route('/search_book',methods=["GET","POST"])
def search_book():
    client=request.args.get('client')
    x=request.form['what']
    which=request.args.get('which')
    page=which+".html"
    data=books.query.filter_by(Title=x).all()
    return render_template(page,data=data,client=client,name=which)
@app.route('/view')
def view():
    book_id=request.args.get('bookid')
    link=books.query.filter_by(book_id=book_id).first()
    file=link.file
    return redirect(file)
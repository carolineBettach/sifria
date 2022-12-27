import json
from flask import Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from models import db,Loans,Books

books = Blueprint('/books', __name__, url_prefix='/books/')
 # Books

@books.route('/<id>', methods = ['GET',"DELETE","PUT"])
@books.route('', methods = ['GET', 'POST'])
def get_all_books(id=-1):
    if request.method == "GET": #read- get all books
        res=[]
        for book in Books.query.order_by(Books.name.asc()).all():
            res.append({"id":book.id,"name":book.name,"author":book.author,"yearPublished":book.yearPublished,"booktypeId":book.booktypeId,"booktypeName":book.booktype.description})
        return  (json.dumps(res))
    if request.method == "POST": #create book
        request_data = request.get_json()
        name= request_data["name"]
        author= request_data["author"]
        yearPublished= request_data["yearPublished"]
        booktypeId= request_data["booktypeId"]
        newBook= Books(name,author,yearPublished,booktypeId)
        db.session.add (newBook)
        db.session.commit()
        return "a new book was created"
    if request.method == "DELETE": #DELETE book
        if(len(Loans.query.filter(Loans.bookId==id).all())>0):#check if book exists in loan 
            return("Can not delete books that have loans!")
        db.session.delete(Books.query.get(id))
        db.session.commit()
        return  ("the book was deleted")
    if request.method == "PUT": #update book
        book= Books.query.get(id)
        request_data = request.get_json()
        name= request_data["name"]
        author= request_data["author"]
        yearPublished= request_data["yearPublished"]
        booktypeId= request_data["booktypeId"]
        book.name=name
        book.author=author
        book.yearPublished=yearPublished
        book.booktypeId=booktypeId
       
        db.session.commit()
        return  ("the book was updated")

 #///////////GET AVAILABLE BOOKS/////////       
@books.route('/availablebooks/', methods = ['GET'])
def get_available_books():
    if request.method == "GET": #read
        res=[]
        bookLoans=set()
        for loan in Loans.query.filter(Loans.returndate==None).all():  
            bookLoans.add(loan.bookId)

        for book in Books.query.filter(Books.id.not_in(bookLoans)).order_by(Books.name.asc()).all():
            res.append({"id":book.id,"name":book.name,"author":book.author,"yearPublished":book.yearPublished,"booktypeId":book.booktypeId,"booktypeName":book.booktype.description})
        return  (json.dumps(res))
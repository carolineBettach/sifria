import json
from flask import Flask, request,Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from models import db,BookType

booktypes = Blueprint('/booktypes/', __name__, url_prefix='/booktypes/')
 # BookType
@booktypes.route('/<id>', methods = ['GET'])
@booktypes.route('', methods = ['GET'])
def get_all_booktypes(id=-1):
    if request.method == "GET": #read get booktypes
        res=[]
        if(id!=-1):# if send booktype id get book type by id
            booktype=BookType.query.get(id)
            res.append({"id":booktype.id,"description":booktype.description,"maxDay":booktype.maxDay})
        else:# if not send booktype id get all book types 
            for booktype in BookType.query.all():
                res.append({"id":booktype.id,"description":booktype.description,"maxDay":booktype.maxDay})
        return  (json.dumps(res))
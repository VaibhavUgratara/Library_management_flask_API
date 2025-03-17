from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from dateutil import parser

app=Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Library.db'

db=SQLAlchemy(app)

# Books and members Classes


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    author = db.Column(db.String(50),nullable=False)
    published_year = db.Column(db.Integer,nullable=False)

    def format(self):
        return{
            'id':self.id,
            'title':self.title,
            'author':self.author,
            'published_year':self.published_year
        }

class Members(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    contact = db.Column(db.Integer,nullable=False)
    date_of_birth = db.Column(db.DateTime,nullable=False)

    def format(self):
        return{
            'id':self.id,
            'name':self.name,
            'address':self.address,
            'contact,':self.contact,
            'date_of_birth':self.date_of_birth
        }



def fetch_members():
    members_data=[]
    MembersData=db.session.query(Members).all()
    for i in MembersData:
        info={
            'id':i.id,
            'name':i.name,
            'address':i.address,
            'contact':i.contact,
            'date_of_birth':i.date_of_birth
        }
        members_data.append(info)
    return members_data

@app.route('/',methods=['GET'])
def api_intro():
    return jsonify({'library_management_api':'create, add, update, delete books and members, also search for different books'})


# Route for adding and fetching books
@app.route('/books',methods=['GET','POST'])
def library_books():
    if request.method == 'POST':
        max_id=Books.query.order_by(Books.id.desc()).first()
        if max_id is None:
            crr_id=1
        else:
            crr_id=max_id.id+1
        status_code=201
        book_info=request.get_json()
        if ( not book_info.get('title') or not(book_info.get('author')) or not(book_info.get('published_year')) ):
            return jsonify({'error':'fill title, author and published_year.'}),400
        
        allowed_fields=['title','author','published_year']
        for k in book_info.keys():
            if k not in allowed_fields:
                return jsonify({'error':f'invalid field {k}'}), 400
        if (book_info['published_year']<0) or (book_info['published_year']>datetime.today().year):
            return jsonify({'error':f'published_year invalid'}), 400
        
        book_info['id']=crr_id
        BookObj=Books(
            id=book_info['id'],
            title=book_info['title'],
            author=book_info['author'],
            published_year=book_info['published_year']
        )
        db.session.add(BookObj)
        db.session.commit()
        json_message=jsonify({'created':book_info})

    else:
        page=request.args.get('page',default=1)
        per_page=5
        try:
            page=int(page)
        except:
            return {'error':'invalid input'}, 400
        BooksList=Books.query.paginate(page=page, per_page=per_page, error_out=False)
        books_data=[book.format() for book in BooksList.items]
        status_code=200
        json_message=jsonify(books_data)

    return json_message, status_code



#Route for updating and deleting book information
@app.route('/books/<int:book_id>',methods=['PUT','DELETE'])
def make_changes_in_books_data(book_id):
    Book=Books.query.filter_by(id=book_id).first()
    Book={'title':Book.title,'author':Book.author,'published_year':Book.published_year}
    if(Book is None):
        return jsonify({'error':'book not found'}), 404
    
    if request.method=="PUT":
        update_info=request.get_json()
        allowed_fields=['title','author','published_year']

        for k in update_info.keys():
            if k not in allowed_fields:
                return jsonify({'error':f'invalid field {k}'}), 400

        if 'published_year' in update_info.keys():    
            if (update_info['published_year']<0) or (update_info['published_year']>datetime.today().year):
                return jsonify({'error':f'published_year invalid'}), 400
        
        

        for i in update_info.keys():
            Book[i]=update_info[i]

        Books.query.filter_by(id=book_id).update({
            'title':Book['title'],
            'author':Book['author'],
            'published_year':Book['published_year']
        })
        db.session.commit()
        json_message=jsonify({'updated':Book})

    else:
        Books.query.filter_by(id=book_id).delete()
        db.session.commit()
        json_message=jsonify({'deleted':Book})

    return json_message


@app.route('/books/search/')
def search_books():
    author=request.args.get('author')
    title=request.args.get('title')
    status_code=200
    if(author is not None):
        BookObj=Books.query.filter_by(author=author).all()

    elif(title is not None):
        BookObj=Books.query.filter_by(title=title).all()

    if(BookObj is None or len(BookObj)==0):
        json_message={'error':'book not found'}
        status_code = 404
    else:
        search_results=[]
        for i in BookObj:
            tempDict=dict()
            tempDict['id']=i.id
            tempDict['title']=i.title
            tempDict['author']=i.author
            tempDict['published_year']=i.published_year
            search_results.append(tempDict)
        json_message=jsonify(search_results)

    return json_message , status_code


#Route for adding and fetching members
@app.route('/members',methods=['GET','POST'])
def library_members():
    if request.method == 'POST':
        max_id=Members.query.order_by(Members.id.desc()).first()
        if(max_id is None):
            crr_id=1
        else:
            crr_id=max_id.id+1
        status_code=201
        member_info=request.get_json()
        if ( not(member_info.get('name')) or not(member_info.get('address')) or not(member_info.get('contact')) or not(member_info.get('date_of_birth')) ):
            return jsonify({'error':'fill name, address, contact and date_of_birth.'}),400
        
        allowed_fields=['name','address','contact','date_of_birth']
        for k in member_info.keys():
            if k not in allowed_fields:
                return jsonify({'error':f'invalid field {k}'})
            
        member_info['id']=crr_id

        x=str(member_info['contact'])
        if(len(x)!=10):
            return {"error":"invalid phone number"}, 400

        try:
            member_info['date_of_birth']=parser.parse(member_info['date_of_birth'],dayfirst=True)
        except:
            return {"error":"date_of_birth not a valid parameter"}, 400
        else:
            if (member_info['date_of_birth'].year<datetime.today().year-80) or (member_info['date_of_birth'].year>datetime.today().year-15):
                return jsonify({'error':f'date_of_birth is not in valid range (Members must have age between 15 and 80)'}), 400

        db.session.add(Members(
            id=member_info['id'],
            name=member_info['name'],
            address=member_info['address'],
            contact=member_info['contact'],
            date_of_birth=member_info['date_of_birth']
        ))
        db.session.commit()

        json_message=jsonify({'created':member_info})

    else:
        page=request.args.get('page',default=1)
        per_page=5
        try:
            page=int(page)
        except:
            return {'error':'invalid input'}, 400
        MembersList=Members.query.paginate(page=page, per_page=per_page, error_out=False)
        members_data=[member.format() for member in MembersList.items]
        json_message=jsonify(members_data)
        status_code=200

    return json_message, status_code


#Route for updating and deleting member information
@app.route('/members/<int:member_id>',methods=['PUT','DELETE'])
def make_changes_in_members_data(member_id):
    Member= Members.query.filter_by(id=member_id).first()
    if(Member is None):
        return jsonify({'error':'member not found'}), 404
    Member={
        'id':Member.id,
        'name':Member.name,
        'address':Member.address,
        'contact':Member.contact,
        'date_of_birth':Member.date_of_birth
    }

    if request.method=="PUT":
        update_info=request.get_json()
        allowed_fields=['name','address','contact','date_of_birth']
        for k in update_info.keys():
            if k not in allowed_fields:
                return jsonify({'error':f'invalid field {k}'}), 400
            
        if('contact' in update_info.keys()):
            x=str(update_info['contact'])
            if(len(x)!=10):
                return {"error":"invalid phone number"}, 400
            
        if('date_of_birth' in update_info.keys()):
            try:
                update_info['date_of_birth']=parser.parse(update_info['date_of_birth'],dayfirst=True)
            except:
                return {"error":"date_of_birth not a valid parameter"}, 400
            else:
                if (update_info['date_of_birth'].year<datetime.today().year-80) or (update_info['date_of_birth'].year>datetime.today().year-15):
                    return jsonify({'error':f'date_of_birth is not in valid range (Members must have age between 15 and 80)'}), 400
        
        for i in update_info.keys():
            Member[i]=update_info[i]
        
        Members.query.filter_by(id=member_id).update({
            'name':Member['name'],
            'contact':Member['contact'],
            'address':Member['address'],
            'date_of_birth':Member['date_of_birth'],
        })

        db.session.commit()

        json_message=jsonify({'updated':Member})

    else:
        Members.query.filter_by(id=member_id).delete()
        db.session.commit()
        json_message=jsonify({'deleted':Member})

    return json_message




if __name__ == '__main__':
    app.run(debug=True)

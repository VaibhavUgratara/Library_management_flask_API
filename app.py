from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app=Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Library.db'

db=SQLAlchemy(app)

# Books and members Classes


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    author = db.Column(db.String(50),nullable=False)
    published_year = db.Column(db.Integer,nullable=False)

class Members(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),unique=True,nullable=False)
    address = db.Column(db.String(50),nullable=False)
    contact = db.Column(db.Integer,nullable=False)
    date_of_birth = db.Column(db.DateTime,nullable=False)


def fetch_books():
    books_data=[]
    BooksData=db.session.query(Books).all()
    for i in BooksData:
            info={
                'id':i.id,
                'title':i.title,
                'author':i.author,
                'published_year':i.published_year
            }
            books_data.append(info)
    return books_data



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
        books_data=fetch_books()
        status_code=200
        json_message=jsonify(books_data)

    return json_message, status_code

#Route for updating and deleting book information
@app.route('/books/<int:book_id>',methods=['PUT','DELETE'])
def make_changes_in_books_data(book_id):
    Book=Books.query.filter_by(id=book_id).first()
    if(Book is None):
        return jsonify({'error':'book not found'}), 404
    
    if request.method=="PUT":
        update_info=request.get_json()
        allowed_fields=['title','author','published_year']

        for k in update_info.keys():
            if k not in allowed_fields:
                return jsonify({'error':f'invalid field {k}'}), 400
            
        if (update_info['published_year']<0) or (update_info['published_year']>datetime.today().year):
            return jsonify({'error':f'published_year invalid'}), 400
        
        Book={'title':Book.title,'author':Book.author,'published_year':Book.published_year}

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
        deleted_data = Books.query.filter_by(id=book_id).first()
        Books.query.filter_by(id=book_id).delete()
        json_message=jsonify({'deleted':deleted_data.title})
        db.session.commit()

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
    global members_data
    if request.method == 'POST':
        status_code=201
        member_info=request.get_json()
        if ( not(member_info.get('name')) or not(member_info.get('address')) or not(member_info.get('contact')) or not(member_info.get('date_of_birth')) ):
            return jsonify({'error':'fill name, address, contact and date_of_birth.'}),400
        
        allowed_fields=['name','address','contact','date_of_birth']
        for k in member_info.keys():
            if k not in allowed_fields:
                return jsonify({'error':f'invalid field {k}'})
            
        member_info['id']=(1 if len(members_data)==0 else members_data[-1]['id']+1)
        members_data.append(member_info)

        json_message=jsonify({'created':member_info})

    else:
        json_message=jsonify(members_data)
        status_code=200

    return json_message, status_code


#Route for updating and deleting member information
@app.route('/members/<int:member_id>',methods=['PUT','DELETE'])
def make_changes_in_members_data(member_id):
    global members_data

    Member=next((m for m in members_data if m['id']==member_id),None)

    if(Member is None):
        return jsonify({'error':'member not found'}), 404
    
    data_index=members_data.index(Member)

    if request.method=="PUT":
        update_info=request.get_json()

        allowed_fields=['name','address','contact','date_of_birth']
        for k in update_info.keys():
            if k not in allowed_fields:
                return jsonify({'error':f'invalid field {k}'}), 400
        
        for i in update_info.keys():
            Member[i]=update_info[i]
        
        members_data[data_index]=Member

        json_message=jsonify({'updated':Member})

    else:
        deleted_data=members_data.pop(data_index)
        json_message=jsonify({'deleted':deleted_data})

    return json_message




if __name__ == '__main__':
    app.run(debug=True)

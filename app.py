from flask import Flask, request, jsonify

app=Flask(__name__)


# Books and members list
books_data=[]
members_data=[]


@app.route('/',methods=['GET'])
def api_intro():
    return jsonify({'library_management_api':'create, add, update, delete books and members, also search for different books'})


# Route for adding and fetching books
@app.route('/books',methods=['GET','POST'])
def library_books():
    global books_data
    if request.method == 'POST':
        status_code=201
        book_info=request.get_json()
        if ( not book_info.get('title') or not(book_info.get('author')) or not(book_info.get('published_year')) ):
            return jsonify({'error':'fill title, author and published_year.'}),400
        
        allowed_fields=['title','author','published_year']
        for k in book_info.keys():
            if k not in allowed_fields:
                return jsonify({'error':f'invalid field {k}'}), 400
        
        book_info['id']=(1 if len(books_data)==0 else books_data[-1]['id']+1)
        books_data.append(book_info)
        json_message=jsonify({'created':book_info})

    else:
        status_code=200
        json_message=jsonify(books_data)

    return json_message, status_code

#Route for updating and deleting book information
@app.route('/books/<int:book_id>',methods=['PUT','DELETE'])
def make_changes_in_books_data(book_id):
    global books_data

    Book=next((b for b in books_data if b['id']==book_id),None)
    if(Book is None):
        return jsonify({'error':'book not found'}), 404
    
    data_index=books_data.index(Book)
    
    if request.method=="PUT":
        update_info=request.get_json()

        allowed_fields=['title','author','published_year']
        for k in update_info.keys():
            if k not in allowed_fields:
                return jsonify({'error':f'invalid field {k}'}), 400
        
        for i in update_info.keys():
            Book[i]=update_info[i]
        
        books_data[data_index]=Book

        json_message=jsonify({'updated':Book})

    else:
        deleted_data = books_data.pop(data_index)
        json_message=jsonify({'deleted':deleted_data})

    return json_message


@app.route('/books/search',methods=['POST'])
def search_books():
    global books_data
    info=request.get_json()

    allowed_fields=['author','title']
    for i in info.keys():
        if(i not in allowed_fields):
            return jsonify({'error':f'invalid field {i}'}), 400
    
    search_results=[]

    if ('author' in info.keys() and 'title' in info.keys()):
        for i in books_data:
            if(info['author']==i['author'] and info['title']==i['title']):
                search_results.append(i)

    elif 'author' in info.keys():
        for i in books_data:
            if(info['author']==i['author']):
                search_results.append(i)

    else:
        for i in books_data:
            if(info['title']==i['title']):
                search_results.append(i)

    return jsonify(search_results)



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

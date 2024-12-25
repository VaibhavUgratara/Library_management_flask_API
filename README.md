# Library_management_flask_API
A simple Library Management System API built using Flask that allows CRUD operations for books and members.

<hr>
Steps to run the project:<br>
<pre>
  <b>Step 1:</b> First install the libraries by running the following command:<br>
      <b> pip install -r requirements.txt </b> <br>
  <b>Step 2:</b> Now you're good to go just run <b> python app.py </b> command in the terminal to start it.
</pre>
<hr>
Key Points of design:
<ol>
  <li>The route <b> /books </b>  on GET request shows the list of available books in JSON format, user can send a page number through the query parameter (e.g. /books?page=2) also data of only 5 books are present in a page.</li>
  <li>POST request on <b> /books </b> adds a new book (post a raw json object). e.g. {"title":"[book_title]","author":"[book_author]","published_year":[YEAR]} </li>
  <li>Similarly, the route <b> /members </b>  on GET request shows the list of members in JSON format, it also accepts a query parameter 'page' (e.g. /members?page=2)  and on POST request a new member is added. e.g {"name":"[member_name]","contact":[phone_bumber],"address":"[address]","date_of_birth":"[DD-MM-YYYY]"} </li>
  <li>In the route <b> /books/book_id </b>  user sends an integer of the book id to update or delete the book. This route works on PUT and DELETE requests.</li>
  <li>Similar to <b> /books/book_id </b> another route <b> /members/member_id </b>  user sends an integer of the member id to update or delete a member. This route also works on PUT and DELETE requests.</li>
  <li>The route <b> /books/search/ </b>  only accepts GET request where a user can send the author name or book title through the query parameter (e.g. /books/search/?author=Author name)</li>
  <li>The POST method on success gives the status code 201 while GET, PUT and DELETE gives 200.</li>
  <li>During POST request in case of any invalid field(s) the status code is 400 and in case of missing field(s) the status code is 404.</li>
</ol>
<hr>
Limitations:
<ol>
  <li>This API does not implement token-based authentication.</li>
</ol>

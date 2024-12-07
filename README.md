# Library_management_flask_API
A simple Library Management System API built using Flask that allows CRUD operations for books and members.

<hr>
Steps to run the project:<br>
<pre>
  <b>Step 1:</b> First install the Flask library by running the following command:<br>
      <b> pip install flask </b> <br>
  <b>Step 2:</b> Now you're good to go just run <b> python app.py </b>  command in the terminal to start it.
</pre>
<hr>
Key Points of design:
<ol>
  <li>The route <b> /books </b>  on GET request shows the list of available books in JSON format and on POST request a new book is added. </li>
  <li>Similarly, the route <b> /members </b>  on GET request shows the list of members in JSON format and on POST request a new member is added.</li>
  <li>In the route <b> /books/book_id </b>  user sends an integer of the book id to update or delete the book. This route works on PUT and DELETE requests.</li>
  <li>Similar to <b> /books/book_id </b>  another route <b> /members/member_id </b>  user sends an integer of the member id to update or delete a member. This route also works on PUT and DELETE requests.</li>
  <li>The route <b> /books/search </b>  only accepts POST request where a user can send the author name or book title or both to get the details of that book.</li>
  <li>The POST method on success gives the status code 201 while GET, PUT and DELETE gives 200.</li>
  <li>During POST request in case of any invalid field(s) the status code is 400 and in case of missing field(s) the status code is 404.</li>
</ol>
<hr>
Limitations:
<ol>
  <li>This API does not implement pagination and token-based authentication.</li>
  <li>Absence of a database.</li>
</ol>

import cgi

# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields
first_name = form.getvalue('email')
last_name = form.getvalue('password')
print(first_name)

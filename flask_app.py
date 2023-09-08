from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# In-memory storage for the submitted data (replace with a database in a real app)
data_storage = []

db_config = {
    'user': 'prakasolanki',
    'password': 'Solanki@2003',
    'host': 'prakasolanki.mysql.pythonanywhere-services.com',
    'database': 'prakasolanki$college',
}

conn = mysql.connector.connect(**db_config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        cursor = conn.cursor()
        insert_query = "INSERT INTO student (name, email) VALUES (%s, %s)"
        # Save the data (you can store it in a database in a real app)
        cursor.execute(insert_query, (name, email))
        conn.commit()
        cursor.close()
        data_storage.append({'name': name, 'email': email})
        return redirect(url_for('index'))

    return render_template('index.html', data=data_storage)


@app.route('/students', methods=['GET'])
def getData():
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM student")
    students = [{'name': name, 'email': email} for (name, email) in cursor]
    cursor.close()
    return render_template('students.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)

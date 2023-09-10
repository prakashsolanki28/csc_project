from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mycscapplication2023'

# In-memory storage for the submitted data (replace with a database in a real app)
data_storage = []

db_config = {
    'user': 'prakasolanki',
    'password': 'Solanki@2003',
    'host': 'prakasolanki.mysql.pythonanywhere-services.com',
    'database': 'prakasolanki$college',
}

conn = mysql.connector.connect(**db_config)

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        dob = request.form['dob']
        classname = request.form['class']

        try:
            cursor = conn.cursor()
            insert_query = "INSERT INTO student (name, gender, dob, class, email) VALUES (%s, %s, %s, %s, %s)"
            # Save the data (you can store it in a database in a real app)
            cursor.execute(insert_query, (name, gender, dob, classname, email))
            conn.commit()
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f'Error: {err}', 'error')  # Error message
        finally:
            cursor.close()

        #data_storage.append({'name': name, 'email': email})
        return redirect(url_for('index'))

    return render_template('index.html', data=data_storage)


@app.route('/students', methods=['GET'])
def getData():
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM student")
    students = [{'id': id, 'name': name, 'email': email} for (id, name, email) in cursor]
    cursor.close()
    return render_template('students.html', students=students)

@app.route('/admin', methods=['GET'])
def AdminLoginView():
    return render_template('login.html')

@app.route('/deletestudent/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    cursor = conn.cursor()

    try:
        # Check if the student with the specified ID exists
        check_query = "SELECT id FROM student WHERE id = %s"
        cursor.execute(check_query, (student_id,))
        student = cursor.fetchone()

        if student:
            # Student exists, proceed with deletion
            delete_query = "DELETE FROM student WHERE id = %s"
            cursor.execute(delete_query, (student_id,))
            conn.commit()
            flash('Student deleted successfully', 'success')
        else:
            # Student with the specified ID does not exist
            flash(f'Student with ID {student_id} not found', 'error')

    except mysql.connector.Error as err:
        conn.rollback()
        flash(f'Error: {err}', 'error')  # Error message
    finally:
        cursor.close()

    # Redirect to the '/students' route
    return redirect('/students')

if __name__ == '__main__':
    app.run(debug=True)

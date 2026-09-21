from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bhavana",
    database="surgi1"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        cursor.execute("SELECT * FROM users1 WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('signup.html', error="Email already registered.")

        # Hash the password and insert
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users1 (email, password) VALUES (%s, %s)", (email, hashed_password))
        db.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users1 WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user'] = email
            return redirect(url_for('surgery_list'))
        else:
            return render_template('login.html', error="Invalid email or password.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/surgery_list')
def surgery_list():
    if 'user' not in session:
        return redirect(url_for('login'))

    surgeries = [
        "Coronary Artery Bypass Grafting", "Laparoscopic Cholecystectomy", "Total Knee Replacement",
        "Hip Replacement Surgery", "Cataract Surgery", "Spinal Fusion Surgery", "Angioplasty",
        "Knee Arthroscopy", "Liver Transplant", "Kidney Transplant", "Gallbladder Removal Surgery",
        "Thyroidectomy", "Hemorrhoidectomy", "Prostatectomy", "Hysterectomy",
        "Cesarean Section (C-Section)", "Dental Implant Surgery", "Rhinoplasty (Nose Surgery)",
        "Bariatric Surgery", "Varicose Veins Surgery"
    ]
    return render_template('surgery_list.html', surgeries=surgeries)

@app.route('/surgery/<name>')
def surgery_details(name):
    if 'user' not in session:
        return redirect(url_for('login'))

    # Get filter parameters from query string
    min_cost = request.args.get('min_cost', type=int)
    max_cost = request.args.get('max_cost', type=int)
    scheme_filter = request.args.get('scheme_filter', default='')

    # Base query
    query = """
        SELECT 
            h.name AS hospital_name,
            h.contact,
            h.address,
            h.website,
            h.location_link,
            po.cost_min,
            po.cost_max,
            s.name AS scheme_name,
            sc.reduced_cost_min,
            sc.reduced_cost_max
        FROM procedures p
        JOIN procedure_offerings po ON p.procedure_id = po.procedure_id
        JOIN hospitals h ON po.hospital_id = h.hospital_id
        LEFT JOIN scheme_coverage sc ON sc.offering_id = po.offering_id
        LEFT JOIN schemes s ON sc.scheme_id = s.scheme_id
        WHERE p.procedure_name = %s
    """

    params = [name]

    # Apply cost filters if provided
    if min_cost is not None:
        query += " AND po.cost_min >= %s"
        params.append(min_cost)
    if max_cost is not None:
        query += " AND po.cost_max <= %s"
        params.append(max_cost)

    # Apply scheme coverage filter
    if scheme_filter == "covered":
        query += " AND s.name IS NOT NULL"
    elif scheme_filter == "not_covered":
        query += " AND s.name IS NULL"

    # Execute query
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    # Format results
    details = []
    for row in results:
        reduced_cost = (
            f"{row['reduced_cost_min']} - {row['reduced_cost_max']}"
            if row['reduced_cost_min'] is not None and row['reduced_cost_max'] is not None
            else "N/A"
        )

        details.append({
            'hospital_name': row['hospital_name'],
            'contact': row['contact'],
            'address': row['address'],
            'website': row['website'],
            'location_link': row['location_link'],
            'cost_min': row['cost_min'],
            'cost_max': row['cost_max'],
            'scheme_name': row['scheme_name'],
            'reduced_cost': reduced_cost
        })

    return render_template('surgery_details.html', name=name, details=details)
    
if __name__ == '__main__':
    app.run(debug=True)

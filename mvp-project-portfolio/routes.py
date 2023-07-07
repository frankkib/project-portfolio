from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from models import db, User, House
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename
from forms import HouseForm, LoginForm
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint('user', __name__)
house_bp = Blueprint('house', __name__)

@user_bp.route('/')
def home():
    return render_template('landingpage.html')
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password_option = request.form['password']
        password = generate_password_hash(password_option)
        new_user = User(username, email, password)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('Registration successful')
            return redirect(url_for('user.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Registration failed')
            return redirect(url_for('user.register'))
    return render_template('Registration.html' , form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('user.dashboard'))
    user = None
    form = HouseForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful', 'success')
            return redirect(url_for('user.dashboard'))  # Redirect to the dashboard route
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('user.login'))  # Redirect back to the login page if login fails
    return render_template('login.html', user=user , form=form)

@user_bp.route('/dashboard' )
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    user_id = session['user_id']
    user = User.query.filter_by(id=session['user_id']).first()
    houses = House.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', user=user, houses=houses)

@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('user.login'))

@house_bp.route('/houses', methods=['GET'])
def index():
    houses = House.query.all()
    form = HouseForm()
    return render_template('home.html', houses=houses, form=form)

@house_bp.route('/houses', methods=['POST'])
def add_house():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    form = HouseForm(request.form)
    if form.validate():
        location = form.location.data
        price = form.price.data
        description = form.description.data
        is_available = form.is_available.data
        created_at = datetime.now()
        user_id = session['user_id']

        # Handle file upload
        photo = form.photo.data
        if photo:
            filename = secure_filename(photo.filename)
            photo.save('static/uploads/' + filename)
        else:
            filename = None

        new_house = House(location=location, price=price, description=description,
                          is_available=is_available, created_at=created_at,
                          user_id=user_id, photo_filename=filename)

        db.session.add(new_house)
        db.session.commit()

        flash('New house added!', 'success')
        return redirect(url_for('house.index'))
    
    flash('Invalid form data', 'error')
    return redirect(url_for('house.index'))

@house_bp.route('/houses/<int:house_id>', methods=['GET'])
def get_house(house_id):
    house = House.query.get(house_id)
    if not house:
        return jsonify({'message': 'House not found'})
    
    house_data = {
        'id': house.id,
        'location': house.location,
        'price': house.price,
        'description': house.description,
        'is_available': house.is_available,
        'created_at': house.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'photo_filename': house.photo_filename
    }
    
    return jsonify({'house': house_data})

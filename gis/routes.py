import os.path
from csv import DictReader
from os import path, remove

from flask import redirect, render_template, request, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from gis import app, db
from gis.forms import RegisterForm
from gis.helpers import coords_calc, coords_calc_new, login_required
from gis.models import User, Samples, Settlements


@app.route('/')
@login_required
def home():
    return render_template('layout.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    # Creating object of a class
    form = RegisterForm()
    if request.method == 'POST':

        # performing validations
        if form.validate_on_submit():
            create_user = User(username=form.username.data,
                               first_name=form.first_name.data,
                               last_name=form.last_name.data,
                               email=form.email.data,
                               affiliation=form.affiliation.data,
                               password_hash=generate_password_hash(form.passwd.data))
            db.session.add(create_user)
            db.session.commit()

            # getting user id for newly created user to assign it to session id
            user = create_user.username
            users_query = [obj.as_dict() for obj in User.query.filter_by(username=f'{user}').all()]
            session["user_id"] = users_query[0]["id"]
            return redirect(url_for('home'))

        # flash errors to the screen, if any
        if form.errors != {}:
            for err_msg in form.errors.values():
                if err_msg[0] == 'Field must be equal to passwd.':
                    flash("Password confirmation doesn't match!", category='danger')
                else:
                    flash(f'{err_msg[0]}', category='danger')

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Ensure username and password were submitted
        if not request.form.get("username"):
            flash("Please provide username!", category='danger')
        elif not request.form.get("password"):
            flash("Please provide your password!", category='danger')

        # Query database for username
        user_try = request.form.get("username")
        user = User.query.filter_by(username=f'{user_try}').first()

        # Check if username and password are correct
        if not user or not check_password_hash(user.password_hash, request.form.get("password")):
            flash("Incorrect credentials!", category='danger')
            # return redirect(url_for('login'))
        else:

            # Remember which user has logged in
            session["user_id"] = user.id
            return redirect(url_for('home'))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for('login'))


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if request.method == 'POST':

        """Handling all the errors using try... except. Unfortunately error handling is very general, because there is
        a lot of cases possible"""
        try:

            # Get all the data from the forms and submit new row to the database
            name = request.form['name']
            long = request.form['long']
            lat = request.form['lat']
            sr = request.form['sr']
            sample_type = request.form['sample']
            number = request.form['sample_point']
            points = Samples(name, long, lat, sr, sample_type, number, session['user_id'])
            db.session.add(points)
            db.session.commit()
            flash('Data submitted successfully!', category='success')
        except BaseException:
            flash('Incorrect data!')
        finally:
            return redirect(url_for('submit'))
    return render_template('submit.html')


@app.route('/conversion', methods=['GET', 'POST'])
@login_required
def conversion():
    if request.method == 'POST':

        """Handling all the errors using try... except. Unfortunately error handling is very general, because there is
        a lot of cases possible"""
        try:

            # Get all the data from the forms and submit new row to the database. Conversion from dd.mm.ss format
            name = request.form['name']
            long_dd, long_mm, long_ss, lat_dd, lat_mm, lat_ss = \
                request.form['long-dd'], request.form['long-mm'], request.form['long-ss'], \
                request.form['lat-dd'], request.form['lat-mm'], request.form['lat-ss']
            long = coords_calc(long_dd, long_mm, long_ss)
            lat = coords_calc(lat_dd, lat_mm, lat_ss)
            sr = request.form['sr']
            sample_type = request.form['sample']
            number = request.form['sample_point']
            points = Samples(name, long, lat, sr, sample_type, number, session['user_id'])
            db.session.add(points)
            db.session.commit()
            flash('Data submitted successfully!', category='success')
        except BaseException:
            flash('Incorrect data!')
        finally:
            return redirect(url_for('conversion'))

    return render_template('submit.html')


@app.route('/conversion_02', methods=['GET', 'POST'])
@login_required
def conversion_02():
    if request.method == 'POST':

        """Handling all the errors using try... except. Unfortunately error handling is very general, because there is
        a lot of cases possible"""
        try:
            # Get all the data from the forms and submit new row to the database. Conversion from dd.mm.mmmm format
            name = request.form['name']
            long_dd, long_mm_mmmm, lat_dd, lat_mm_mmmm = request.form['long-dd'],\
                                                         request.form['long-mm.mmmm'], \
                                                         request.form['lat-dd'], \
                                                         request.form['lat-mm.mmmm']
            long = coords_calc_new(long_dd, long_mm_mmmm)
            lat = coords_calc_new(lat_dd, lat_mm_mmmm)
            sr = request.form['sr']
            sample_type = request.form['sample']
            number = request.form['sample_point']
            points = Samples(name, long, lat, sr, sample_type, number, session['user_id'])
            db.session.add(points)
            db.session.commit()
        except BaseException:
            flash('Incorrect data!')
        finally:
            return redirect(url_for('conversion_02'))

    return render_template('submit.html')


@app.route('/file', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':

        # function to upload file with sr data
        file = request.files['file']

        # Secure filename tool from werkzeug util
        filename = secure_filename(file.filename)

        # Getting file extension
        file_ext = os.path.splitext(filename)[1]

        # Check if there is file and extension is allowed
        if filename != '' and file_ext in app.config['UPLOAD_EXTENSIONS']:
            file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
            try:

                # Converting data to the sqlalchemy class. If file format isn't correct - raise error
                with open(f"{app.config['UPLOAD_FOLDER']}/{filename}") as file:
                    reader = DictReader(file, delimiter=';')
                    for i in reader:
                        name, long, lat, sr, sample_type, number, = i['name'], \
                                                                    i['long'], i['lat'], i['sr'], \
                                                                    i['sample_type'], i['number']
                        points = Samples(name, long, lat, sr, sample_type, number, session['user_id'])
                        db.session.add(points)
                        db.session.commit()
                flash(f'Your file "{filename}" was uploaded successfully!', category='success')
            except BaseException:
                flash(f"Format of the file is not correct!", category='danger')
            finally:

                # Remove uploaded file
                remove(f"{app.config['UPLOAD_FOLDER']}/{filename}")
                return redirect(url_for('upload_file'))
        else:

            # if file isn't csv - flash this message
            flash("Please select correct file", category='danger')
    return render_template("file.html")


@app.route('/submit_settlements', methods=['GET', 'POST'])
@login_required
def submit_settlements():
    if request.method == 'POST':

        """Handling all the errors using try... except. Unfortunately error handling is very general, because there is
        a lot of cases possible"""
        try:

            # Get all the data from the forms about settlements and submit new row to the database.
            name = request.form['name']
            location = request.form['location']
            long = request.form['long']
            lat = request.form['lat']
            points = Settlements(name, location, long, lat, session['user_id'])
            db.session.add(points)
            db.session.commit()
        except BaseException:
            flash('Incorrect data!')
        finally:
            return redirect(url_for('submit_settlements'))

    return render_template('submit_settlements.html')


@app.route('/settlements_conversion', methods=['GET', 'POST'])
@login_required
def settlements_conversion():
    if request.method == 'POST':

        """Handling all the errors using try... except. Unfortunately error handling is very general, because there is
        a lot of cases possible"""
        try:

            # Get all the data from the forms and submit new row to the database. Convert dd.mm.ss format
            name = request.form['name']
            location = request.form['location']
            long_dd, long_mm, long_ss, lat_dd, lat_mm, lat_ss = \
                request.form['long-dd'], request.form['long-mm'], request.form['long-ss'], \
                request.form['lat-dd'], request.form['lat-mm'], request.form['lat-ss']
            long = coords_calc(long_dd, long_mm, long_ss)
            lat = coords_calc(lat_dd, lat_mm, lat_ss)
            points = Settlements(name, location, long, lat, session['user_id'])
            db.session.add(points)
            db.session.commit()
        except BaseException:
            flash('Incorrect data!')
        finally:
            return redirect(url_for('settlements_conversion'))
    return render_template('submit_settlements.html')


@app.route('/settlements_conversion_02', methods=['GET', 'POST'])
@login_required
def settlements_conversion_02():
    if request.method == 'POST':

        """Handling all the errors using try... except. Unfortunately error handling is very general, because there is
        a lot of cases possible"""
        try:

            # Get all the data from the forms and submit new row to the database. Convert dd.mm.mmmm format
            name = request.form['name']
            location = request.form['location']
            long_dd, long_mm_mmmm, lat_dd, lat_mm_mmmm = request.form['long-dd'], request.form['long-mm.mmmm'], \
                                                         request.form['lat-dd'], \
                                                         request.form['lat-mm.mmmm']

            long = coords_calc_new(long_dd, long_mm_mmmm)
            lat = coords_calc_new(lat_dd, lat_mm_mmmm)
            points = Settlements(name, location, long, lat, session['user_id'])
            db.session.add(points)
            db.session.commit()
        except BaseException:
            flash('Incorrect data!')
        finally:
            return redirect(url_for('settlements_conversion_02'))
    return render_template('submit_settlements.html')


@app.route('/settlements_file', methods=['GET', 'POST'])
@login_required
def settlements_file():
    if request.method == 'POST':
        file = request.files['file']

        # Secure filename tool from werkzeug util
        filename = secure_filename(file.filename)

        # Getting file extension
        file_ext = os.path.splitext(filename)[1]

        # Check if there is file and extension is allowed
        if filename != '' and file_ext in app.config['UPLOAD_EXTENSIONS']:
            file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
            try:

                # Converting data to the sqlalchemy class. If file format isn't correct - raise error
                with open(f"{app.config['UPLOAD_FOLDER']}/{filename}") as file:
                    reader = DictReader(file, delimiter=';')
                    for i in reader:
                        name, location, long, lat, user_id = i['name'], i['location'], \
                                                             i['long'], i['lat'], session['user_id']
                        points = Settlements(name, location, long, lat, user_id)
                        db.session.add(points)
                        db.session.commit()
                flash(f'Your file "{filename}" was uploaded successfully!', category='success')
            except BaseException:
                flash(f"Format of the file is not correct!", category='danger')
            finally:
                remove(f"{app.config['UPLOAD_FOLDER']}/{filename}")
                return redirect(url_for('settlements_file'))
        else:

            # if file isn't csv - flash this message
            flash("Please select correct file", category='danger')
    return render_template("file.html")


@app.route('/table', methods=['GET', 'POST'])
@login_required
def table():
    # Function to render a table of data from database

    # Get groups of data according to the sample type
    options = [r for (r,) in db.session.query(Samples.sample_type).group_by(Samples.sample_type).all()]
    settlements = Settlements.query.all()
    if not options and not settlements:

        # If db is empty - flash this message
        flash("There is no data to show!", category='danger')
        return render_template('choose_sample.html')
    else:
        if request.method == 'POST':
            choice = request.form.get('select')

            # To show all strontium data
            if choice == 'all strontium data':
                samples = Samples.query.all()
                return render_template('table.html', samples=samples)

            # To show all settlements data
            elif choice == 'settlements':
                if settlements:
                    return render_template('table.html', settlements=settlements)
                else:
                    flash("There is no data to show!", category='danger')

            # Show data based on the sample type
            else:
                samples = Samples.query.filter_by(sample_type=f'{choice}').all()
                return render_template('table.html', samples=samples)

        return render_template('choose_sample.html', options=options)


@app.route('/map', methods=['GET', 'POST'])
@login_required
def render_map():

    # Function to render data on a map

    if request.method == 'POST':
        choice = request.form.get('select')

        # To show all strontium data
        if choice == 'all strontium data':
            samples = Samples.query.all()

        # To show all settlements data
        elif choice == 'settlements':
            samples = Settlements.query.all()

        # To show strontium data based on the type of sample
        else:
            samples = Samples.query.filter_by(sample_type=f'{choice}').all()
        return render_template('map.html', samples=samples)

    options = [r for (r,) in db.session.query(Samples.sample_type).group_by(Samples.sample_type).all()]
    return render_template('choose_sample.html', options=options)

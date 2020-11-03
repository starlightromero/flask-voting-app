"""Import libraries."""
from flask import Flask, render_template

# TODO: import WTForms
from flask_wtf import FlaskForm

# TODO: import needed fields from WTForms
from wtforms import FileField, SubmitField, StringField

# TODO: import needed validators from WTForms
from wtforms.validators import DataRequired, Length

# TODO: import Flask SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# TODO: import Flask SocketIO
from flask_socketio import SocketIO, emit

# TODO: import Flask Uploads
from flask_uploads import configure_uploads, IMAGES, UploadSet

app = Flask(__name__)
# TODO: create a SECRET_KEY config
app.config["SECRET_KEY"] = "secret"

app.config["UPLOADED_IMAGES_DEST"] = "static/images"

#  TODO: instantiate UploadSet
images = UploadSet("images", IMAGES)
# TODO: configure uploads
configure_uploads(app, images)
# TODO: initalize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")
# TODO: create a SQLALCHEMY_DATABASE_URI config with a SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# TODO: initalize SQLAlchemy
db = SQLAlchemy(app)


class Candidate(db.Model):
    # TODO: create an id as a primary key
    id = db.Column(db.Integer, primary_key=True)
    # TODO: create "name" as an integer
    name = db.Column(db.String(30), nullable=False, unique=True)
    # TODO: create a "image" as a string
    image = db.Column(db.String(30), nullable=False, unique=True)

    # OPTIONAL: create a repr function that returns the candidate's name
    def __repr__(self):
        """Return name."""
        return f"Candidate('{self.name}')"


class Results(db.Model):
    # TODO: create an id as a primary key
    id = db.Column(db.Integer, primary_key=True)
    # TODO: create "vote" as an integer
    vote = db.Column(db.Integer)


# TODO: create a CandidateForm using WTForms. it should have a name, image,
#  and submit field
class CandidateForm(FlaskForm):
    name = StringField(
        "Candidate Name", validators=[DataRequired(), Length(max=30)]
    )
    image = FileField("Candidate Image")
    submit = SubmitField("Upload")


# TODO: create a "calculate_results" function. This function should return a
# dictionary of the count of the two results
# HINT: make a query to each "vote", calculate the total count for each
# vote total, and save it in a variable.
def calculate_results():
    """Return a count of Results 1 and Results 2"""
    results1 = Results.query.filter_by(vote=1).count()
    results2 = Results.query.filter_by(vote=2).count()
    return {"results1": results1, "results2": results2}


# TODO: create a socketio on "vote" event
@socketio.on("vote")
def handleVote(ballot):
    """Handle vote on incoming socket request."""
    # This function will create a new db object and add it to the db.
    vote = Results(vote=ballot)
    db.session.add(vote)
    db.session.commit()
    # TODO: emit "vote_results" and pass in a dict of each vote result
    # TODO: remember to send this event to all clients
    emit("vote_results", calculate_results(), broadcast=True)


# TODO: create a route that returns index.html
# TODO: pass in CandidateForm
# TODO: on valid form submission save the image
# TODO: on valid form submission add the candidate to the db
# TODO: make sure you also return the form
@app.route("/", methods=["GET", "POST"])
def home():
    """Return homepage."""
    form = CandidateForm()
    if form.validate_on_submit():
        name = form.name.data
        filename = images.save(form.image.data)
        candidate = Candidate(name=name, image=filename)
        db.session.add(candidate)
        db.session.commit()
    return render_template("index.html", form=form)


# TODO: create a route "/results" the route should return the results from
# the calculate_results function
@app.route("/results")
def get_results():
    """Return a json object of the results."""
    return calculate_results()


# TODO: create a route "/candidates" the route should get a query of all
# the candidates but return a dict of the last two candidates
# HINT: use if statements to check the length of candidates so that the terminal
# won't throw IndexErrors
@app.route("/candidates")
def get_candidates():
    """Return a json object of all candidates."""
    candidates = Candidate.query.all()
    candidate1 = None
    candidate2 = None
    if len(candidates) > 0:
        candidate2 = candidates[-1]
        if len(candidates) > 1:
            candidate1 = candidates[-2]
            return {
                "candidate1_name": candidate1.name,
                "candidate1_image": candidate1.image,
                "candidate2_name": candidate2.name,
                "candidate2_image": candidate2.image,
            }
        return {
            "candidate2_name": candidate2.name,
            "candidate2_image": candidate2.image,
        }
    return {"none": 0}


if __name__ == "__main__":
    # TODO: create the database
    with app.app_context():
        db.create_all()
    # TODO: run the app
    socketio.run(app)

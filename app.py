"""Import libraries."""
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_uploads import configure_uploads, IMAGES, UploadSet

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["UPLOADED_IMAGES_DEST"] = "static/images"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

images = UploadSet("images", IMAGES)
configure_uploads(app, images)
socketio = SocketIO(app, cors_allowed_origins="*")
db = SQLAlchemy(app)


class Candidate(db.Model):
    """Candidate database model class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    image = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        """Return name."""
        return f"Candidate('{self.name}')"


class Results(db.Model):
    """Results database model class."""

    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer)


class CandidateForm(FlaskForm):
    """Candidate Form."""

    name = StringField(
        "Candidate Name", validators=[DataRequired(), Length(max=30)]
    )
    image = FileField("Candidate Image")
    submit = SubmitField("Upload")


def calculate_results():
    """Return a count of Results 1 and Results 2."""
    results1 = Results.query.filter_by(vote=1).count()
    results2 = Results.query.filter_by(vote=2).count()
    return {"results1": results1, "results2": results2}


@socketio.on("vote")
def handleVote(ballot):
    """Handle vote on incoming socket request."""
    vote = Results(vote=ballot)
    db.session.add(vote)
    db.session.commit()
    emit("vote_results", calculate_results(), broadcast=True)


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


@app.route("/results")
def get_results():
    """Return a json object of the results."""
    return calculate_results()


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
    with app.app_context():
        db.create_all()
    socketio.run(app)

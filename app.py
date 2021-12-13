from types import MethodDescriptorType
from flask import Flask, render_template, flash, redirect, render_template
from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

from forms import AddPetForm
from forms import UserForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def homepage():
    """Show Pet listing."""
    pets = Pet.query.all()
    return render_template("pet_listing.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_snack():
    """form for adding pets."""

    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} addeds.")
        return redirect('/')

    else:
        return render_template("pet_add_form.html", form=form)
 

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """edit pet"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect("/")

    else:
        return render_template("pet_edit_form.html", form=form, pet=pet)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about the pet in JSON"""
    
    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}
    
    return jsonify(info)
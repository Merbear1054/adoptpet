from flask import Flask, render_template, redirect, request, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///adopt.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "shhh"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    available_pets = Pet.query.filter_by(available=True).all()
    unavailable_pets = Pet.query.filter_by(available=False).all()
    return render_template("home.html", available_pets=available_pets, unavailable_pets=unavailable_pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        photo_url = form.photo_url.data
        photo_file = form.photo_file.data

        if photo_file:
            filename = secure_filename(photo_file.filename)
            photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            photo_file.save(photo_path)
            photo_url = f"/{photo_path}"

        data = {k: v for k, v in form.data.items() if k not in ["csrf_token", "photo_file"]}
        data["photo_url"] = photo_url

        pet = Pet(**data)
        db.session.add(pet)
        db.session.commit()
        flash(f"{pet.name} added successfully!", "success")
        return redirect(url_for('home'))

    return render_template("add_pet.html", form=form)


@app.route("/pets/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        photo_file = form.photo_file.data

        if photo_file:
            filename = secure_filename(photo_file.filename)
            photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            photo_file.save(photo_path)
            pet.photo_url = f"/{photo_path}"

        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash(f"{pet.name} updated!", "info")
        return redirect(url_for("home"))

    return render_template("edit_pet.html", pet=pet, form=form)


if __name__ == "__main__":
    app.run(debug=True)

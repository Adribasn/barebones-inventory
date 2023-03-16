from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Item
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        itemName = request.form.get('itemName')
        units = request.form.get('units')
        price = request.form.get('price')
        value = float(units) * float(price)
        value = round(value, 2)

        if len(itemName) < 2:
            flash("Item name is too short.", category="error")
        else:
            new_item = Item(itemName=itemName, units=units, price=price, value=value, user_id=current_user.id)
            db.session.add(new_item)
            db.session.commit()
            flash("Added new item!", category="success")

    return render_template("home.html", user=current_user)

@views.route("/delete-item", methods=["POST"])
def delete_item():
    data = json.loads(request.data)
    itemId = data['itemId']
    item = Item.query.get(itemId)
    if item:
        if item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
    
    return jsonify({})

@views.route("/edit-item/<int:id>", methods=["GET", "POST"])
def edit_item(id):
    if request.method == "POST":
        itemName = request.form.get('itemName')
        units = request.form.get('units')
        price = request.form.get('price')
        
        item = Item.query.filter_by(id=id).first()

        if len(itemName) < 2:
            flash("Item name is too short.", category="error")
        else:
            item.itemName = itemName
            item.units = units
            item.price = price
            value = float(units) * float(price)
            item.value = round(value, 2)
            db.session.commit()
            flash("Updated item!", category="success")

        return redirect(url_for('views.home'))

    return render_template("edit_item.html", user=current_user, id=id)
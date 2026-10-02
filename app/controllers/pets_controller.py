from flask import Bluesprint, render_template, request, flash, redirect, url_for

city_bp = Bluesprint('pets',__name__)

@city_bp.route('/pets', methods=['GET', 'POST'])
def city():
    return render_template('pets/pets.html')
import os
from app import app, db, lm
from flask import render_template

# ##############################################################################
# ERROR HANDLING
# ##############################################################################
@app.errorhandler(404)
def not_found_error(error):
    print('heelllloooo')
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/accessDenied')
def not_found_error():
    return render_template('accessDenied.html')

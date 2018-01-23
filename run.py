#!flask/bin/python
from app import app, scheduler
scheduler.start()

app.run(debug=True)

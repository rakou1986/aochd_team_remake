#!/home/feeeed/.pyenv/versions/3.4.2-flask/bin/python
 
from wsgiref.handlers import CGIHandler

from application import app

CGIHandler().run(app)

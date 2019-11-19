from bluep import app
import logging
from logging.handlers import RotatingFileHandler
import datetime


if __name__ == '__main__':
    '''
    now = datetime.datetime.now()
    filename = now.strftime("%m-%d-%Y")+"-api.log"
    handler = RotatingFileHandler('%s'%filename, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    '''
    app.run(debug=True)




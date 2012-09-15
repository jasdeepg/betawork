#flask imports
from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#class imports
import Panel
import State

#google imports
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis

#python imports
import os
import sqlite3
from contextlib import closing

#config vars
DATABASE = '/tmp/98lumens.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

#satisfy app requirements for opening and closing a request
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request():
    g.db.close()

#add fake entries to database ...
#can make this dynamic for user or tie into backend when available
def addto_db():
    g.db.execute('insert into entries (title, timeDay, power) values (?, ?, ?)',
                 ['Jim', 9, 1])
    g.db.execute('insert into entries (title, timeDay, power) values (?, ?, ?)',
                 ['Jim', 10, 1.2])
    g.db.execute('insert into entries (title, timeDay, power) values (?, ?, ?)',
                 ['Jim', 12, 2])
    g.db.execute('insert into entries (title, timeDay, power) values (?, ?, ?)',
                 ['Jim', 13, 2.3])
    g.db.commit()

def makeChart():
    # Set the vertical range from 0 to 100
    max_y = 100
    
    # Chart size of 200x125 pixels and specifying the range for the Y axis
    chart = SimpleLineChart(400, 250, y_range=[0, max_y])
    
    # Add the chart data
    # Aggregate data into array before adding to chart
    data = [
        32, 34, 34, 32, 34, 34, 32, 32, 32, 34, 34, 32, 29, 29, 34, 34, 34, 37,
        37, 39, 42, 47, 50, 54, 57, 60, 60, 60, 60, 60, 60, 60, 62, 62, 60, 55,
        55, 52, 47, 44, 44, 40, 40, 37, 34, 34, 32, 32, 32, 31, 32
    ]
    #for i in data:
    #    chart.add_data(i)
    chart.add_data(data)
    
    # Set the line colour to blue
    chart.set_colours(['0000FF'])
    
    # Set the vertical stripes
    chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.2, 'FFFFFF', 0.2)
    
    # Set the horizontal dotted lines
    chart.set_grid(0, 25, 5, 5)
    
    # The Y axis labels contains 0 to 100 skipping every 25, but remove the
    # first number because it's obvious and gets in the way of the first X
    # label.
    left_axis = range(0, max_y + 1, 25)
    left_axis[0] = ''
    chart.set_axis_labels(Axis.LEFT, left_axis)
    
    # X axis labels
    chart.set_axis_labels(Axis.BOTTOM, \
        ['9 am', '6 pm', '12 am'])
        
    return chart

@app.route('/')
def content():
    cur = g.db.execute('select id, title, timeDay, power from entries order by id desc')
    entries = [dict(id=row[0],title=row[1],timeDay=row[2], power=row[3]) for row in cur.fetchall()]
    for entry in entries:
        print entry
    return render_template('content.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
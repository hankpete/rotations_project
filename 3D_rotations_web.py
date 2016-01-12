from numpy import *   # for user input
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import time    # for new file names
import os
from bottle import run, template, get, post, request
import json

# different name each time
file = str(int(time.time()))

# grab username and key from config/data file
with open('data.json') as config_file:
    config_data = json.load(config_file)
username = config_data["user"]
key = config_data["key"]

py.sign_in(username, key)


@get('/input')
def form():
    return template('html1', title='3D Rotations Graph')


@post('/input')
def submit():
    # grab data from form
    function_a = request.forms.get('function_a')
    function_b = request.forms.get('function_b')
    MIN = request.forms.get('MIN')
    MAX = request.forms.get('MAX')

    # set up domain
    MIN = float(MIN)
    MAX = float(MAX)
    NUM = 100
    xvals = np.linspace(MIN, MAX, NUM)

    # set up original curves by populating lists with eval() outputs
    a_yvals = []
    b_yvals = []
    for x in xvals:
        a_yvals.append(eval(function_a))
        b_yvals.append(eval(function_b))

    # get what we have so far into the data
    zvals = xvals*0
    line_a = go.Scatter3d(
        x = xvals,
        y = a_yvals,
        z = zvals,
        mode='lines',
        line=dict(
            color='red',
            width=4
        )
    )

    line_b = go.Scatter3d(
        x = xvals,
        y = b_yvals,
        z = zvals,
        mode='lines',
        line=dict(
            color='blue',
            width=4
        )
    )
    data = [line_a, line_b]

    # take each point on curve B, approximate tangent line to it, make perpendicular line to the tangent,
    # find point on curve A that it intersects, draw a circle with this point around B:
    for i in range(len(xvals)):

        b_x = xvals[i]
        b_y = b_yvals[i]

        # dont make a circle of radius 0...
        if a_yvals[i] == b_y:
            continue

        # get perpendicular slope to reflection point on curve B 
        # use approx of slope 
        if i>=1:
            tan_slope = (b_yvals[i]-b_yvals[i-1])/(xvals[i]-xvals[i-1])
        else:
            tan_slope = (b_yvals[i]-b_yvals[i+1])/(xvals[i]-xvals[i+1])

        # find approx where perp_line and rotating line intersect
        solutions = []
        if tan_slope == 0:    # must make it so that flat lines work too
            solutions.append(b_x)
        else:
            # perpendicular is neg recip
            slope = tan_slope**(-1)
            slope = -slope
            perp_line = slope*(xvals - b_x) + b_y

            # check when difference in yvals changes sign, approx intersection
            positive = None
            for j in range(len(xvals)):
                diff = perp_line[j]-a_yvals[j]
                old_positive = positive
                if diff>0:
                    positive = True
                elif diff==0:
                    solutions.append(xvals[j])
                else:
                    positive = False

                if old_positive != None:
                    if old_positive != positive:
                        solutions.append(xvals[j])

        # make a circle for every solution
        for a_x in solutions:

            # for eval() to work it must be an 'x'
            x = a_x
            a_y = eval(function_a)

            # calc radius, plot line of circle diameter otherwise 
            if tan_slope == 0:    # again, making sure it works for vertical lines
                radius = np.abs(a_y - b_y)
                circle_xs = [a_x]*50
                circle_ys = np.linspace(b_y-radius, b_y+radius, 50)
            else:
                # radius of circle is dist btwn point on line A and point on line B
                delta_x = np.abs(float(b_x-a_x))
                delta_y = np.abs(float(b_y-a_y))
                radius = np.sqrt((delta_x)**2 + (delta_y)**2)

                # make a line segment on xy plane that is circle's diameter
                circle_xs = np.linspace(b_x-delta_x, b_x+delta_x, 50) 
                circle_ys = slope*(circle_xs - b_x) + b_y

            # z points are a function of x and y, make a circle
            circle_zs = []
            for k in range(len(circle_xs)):
                # solve for z in distance formula
                magnitude = np.sqrt(radius**2 - (circle_xs[k]-b_x)**2 - (circle_ys[k]-b_y)**2)

                # bottom and top of circle
                circle_zs.append(magnitude)
                circle_zs.append(-magnitude)

            # double all the points on the x and y axes to account for top and bottom of circle
            circle_xs = np.repeat(circle_xs, 2)
            circle_ys = np.repeat(circle_ys, 2)


            # add this circle too the data list and do the next one
            circle = go.Scatter3d(
                x = circle_xs,
                y = circle_ys,
                z = circle_zs,
                mode='lines',
                opacity = .1,
                line=go.Line(
                    color='green',
                    width=2
                 )
            )

            data.append(circle)
            
    ### make sure it's not distorted
    diff = MAX - MIN + 4    # length of one side of cubic graph
    diff = diff/2.0         # half so we can start from midpoint
    # determine where the middle of the graph is on the y axis 
    a_yvalsMIN = min(a_yvals)
    a_yvalsMAX = max(a_yvals)
    b_yvalsMIN = min(b_yvals)
    b_yvalsMAX = max(b_yvals)
    YMAX = max(a_yvalsMIN, b_yvalsMIN)
    YMIN = min(a_yvalsMAX, b_yvalsMAX)
    ymiddle = YMIN + (YMAX - YMIN)/2.0
    
    # set the axis limits to be a nice cube
    layout = go.Layout(
        title="Rotated Functions",
        
        scene=go.Scene(
            xaxis=dict(
                autorange=False,
                showspikes=False,
                range=[MIN-2, MAX+2]  # set axis range
            ),
            yaxis=dict(
                autorange=False,
                showspikes=False,
                range=[ymiddle-diff, ymiddle+diff]
            ),
            zaxis=dict(
                autorange=False,
                showspikes=False,
                range=[-diff, diff]
            )
        ),
        
        showlegend=False,
        hovermode=False
    )

    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename=file, auto_open=False)
    
    return template('html2', plot_url=str(plot_url)+".embed")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)

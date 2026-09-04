import TraceGUI
import time

# Testing Vars

# Trace by including in a dict
x=10
name="Something"
series=[1,2,3,4,5]

traceDict={
    "name":name,
    "x":x,
    "series":series
}

# Control, must be included in a dict
con1=1
con2=2
string="test"

control_var={
    "con1":con1,    # name as the same as the variable
    "con2":con2,
    "string":string
}

# Trace by passing directly
string1="test1"
string2="test2"


# Slider: [
#           init value and also the output value,
#           (min, max),
#           step <normaly=1\optional>
# ]
# Must include in a dict
Volume=[50, (0, 100)]
Brightness=[100, [0, 200], 5]

slider = {
    "Volume": Volume,
    "Brightness": Brightness
}
"""
1.Start threading the gui before any looping (example: your ros program) via "TraceGUI.create_gui(caller_globals=globals(), *argu, **kwags)" 
2.Can thread only one gui so don't try running both at the same time
3.You can either pass the tracing variables via "tracked_dict=YOUR_DICT" or by passing the kwags "string1=string1"
4.When passing the kwags they must be the same name
5.MUST PASS THE "caller_globals=globals()" for the gui to work proberly
"""
TraceGUI.create_gui(caller_globals=globals(), controled_dict=control_var, slider=slider, tracked_dict=traceDict)
# TraceGUI.create_gui(caller_globals=globals(), controled_dict=book, slider=slider, string1=string1, string2=string2)

# YOUR ROS PROGRAM HERE
while TraceGUI.flag:
    x+=1
    print(x)
    print(Volume)
    print(Volume[0])
    print(type(con1))
    print(con2)
    print(string1)
    time.sleep(1)
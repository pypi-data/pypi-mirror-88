class DraggablePoint:

    # http://stackoverflow.com/questions/21654008/matplotlib-drag-overlapping-points-interactively
    # https://stackoverflow.com/questions/28001655/draggable-line-with-draggable-points
    
    lock = None #  only one can be animated at a time
    size=0.01

    # ======================================================================= #
    def __init__(self, parent, updatefn, x, y, setx=True, sety=True, color=None, marker='s'):
        """
            parent: parent object
            updatefn: funtion which updates the line in the correct way
                updatefn(xdata, ydata)
            x, y: initial point position
            setx, sety: if true, allow setting this parameter
            color: point color
        """
        self.parent = parent
        self.point = parent.ax.plot(x, y, zorder=25, color=color, alpha=0.5, 
                                 marker=marker, markersize=8)[0]
        
        self.point.set_pickradius(8)
        self.updatefn = updatefn
        self.setx = setx
        self.sety = sety
        self.press = None
        self.background = None
        self.connect()
        
    # ======================================================================= #
    def connect(self):
        """connect to all the events we need"""
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    # ======================================================================= #
    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        if DraggablePoint.lock is not None: return
        contains, attrd = self.point.contains(event)
        if not contains: return
        DraggablePoint.lock = self
        
    # ======================================================================= #
    def on_motion(self, event):

        if DraggablePoint.lock is not self: return
        if event.inaxes != self.point.axes: return
        
        # get data
        x = event.xdata
        y = event.ydata
        
        # move the point
        if self.setx:   self.point.set_xdata(x)
        if self.sety:   self.point.set_ydata(y)

        # update the line
        self.updatefn(x, y)        

    # ======================================================================= #
    def on_release(self, event):
        'on release we reset the press data'
        if DraggablePoint.lock is not self: return
        DraggablePoint.lock = None
        
    # ======================================================================= #
    def disconnect(self):

        'disconnect all the stored connection ids'

        self.point.figure.canvas.mpl_disconnect(self.cidpress)
        self.point.figure.canvas.mpl_disconnect(self.cidrelease)
        self.point.figure.canvas.mpl_disconnect(self.cidmotion)

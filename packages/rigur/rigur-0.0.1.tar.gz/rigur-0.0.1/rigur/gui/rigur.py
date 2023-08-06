# Main GUI
# Derek Fujimoto
# Dec 2020

import os, datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# set MPL backend
import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import numpy as np
import pandas as pd

from rigur import __version__
from rigur.backend.DraggablePoint import DraggablePoint

# interactive plotting
plt.ion()

# =========================================================================== #
class rigur(object):
    """
        ax:             mpl.Axes of fig
        
        button_scale:   tk.Button for scaling image
        
        data:           list of xy data points in linear scaling
        data_line:      mpl.Line, line with data points based on click
        drag_pts:       dict of DraggablePoints

        entry_xlow:     tk.Entry for image coord input
        entry_xupp:     tk.Entry for image coord input
        entry_ylow:     tk.Entry for image coord input
        entry_yupp:     tk.Entry for image coord input

        img:            np.ndarray with image data
        fig:            mpl.Figure with image
        fig_data:       mpl.Figure with collected data        
        filename:       string, current file drawn
        
        mainframe:      Frame, big frame for the whole window
        root:           tk.Tk object
        
        toolbar:        NavigationToolbar2Tk
        
        xl_img, xh_img,  tk.StringVar, input for real units axes values of image
        yl_img, yh_img
        
        xl_pix, xh_pix,  float, input for pixel values of image
        yl_pix, yh_pix
        
        x_slider_for_y  the x value the y draggable points have
        y_slider_for_x  the y value the x draggable points have
        
        x_scale         tk.StringVar, linear or log scale for x axis
        y_scale         tk.StringVar, linear or log scale for y axis
    """

    # ======================================================================= #
    def __init__(self):
        
        # init root
        self.root = tk.Tk()
        self.root.title('rigur: Rip data from image of figure (version %s)' % __version__)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # hotkeys
        self.root.bind('<Control-o>', self.open_file)
        self.root.bind('<Control-z>', self.delete_data)
        self.root.bind('<Return>', self.do_button_scale)
        self.root.bind('<KP_Enter>', self.do_button_scale)
        self.root.bind('<KeyRelease>', self.keyrelease)

        # minimum window size
        self.root.minsize(800, 600)

        # event bindings
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Menu bar options ----------------------------------------------------
        self.root.option_add('*tearOff', 'false')
        menubar = tk.Menu(self.root)
        self.root['menu'] = menubar
        
        # file menu
        menu_file = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Open image', command=self.open_file)
        
        # x axis menu 
        self.x_scale = tk.StringVar()
        self.x_scale.set("linear")
        menu_x = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_x, label='x-axis')
        menu_x.add_radiobutton(label="Linear", variable=self.x_scale, value='linear')
        menu_x.add_radiobutton(label="Log10", variable=self.x_scale, value='log10')
        menu_x.add_radiobutton(label="Ln", variable=self.x_scale, value='ln')
        
        # y axis menu 
        self.y_scale = tk.StringVar()
        self.y_scale.set("linear")
        menu_y = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_y, label='y-axis')
        menu_y.add_radiobutton(label="Linear", variable=self.y_scale, value='linear')
        menu_y.add_radiobutton(label="Log10", variable=self.y_scale, value='log10')
        menu_y.add_radiobutton(label="Ln", variable=self.y_scale, value='ln')
        
        # main frame
        self.mainframe = ttk.Frame(self.root, pad=5)
        self.mainframe.grid(column=0, row=0, sticky='nsew')
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        # layout frames
        left_frame = ttk.Frame(self.mainframe, pad=0)
        left_frame.grid(column=0, row=0, sticky='nsew')
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        right_frame = ttk.Frame(self.mainframe, pad=0)
        right_frame.grid(column=1, row=0, sticky='nsew')
        
        # embedded canvas
        self.fig = Figure(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(self.fig, master=left_frame)  
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        canvas.mpl_connect('button_press_event', self.get_data)
        canvas.mpl_connect('motion_notify_event', self.draw_crosshairs)
        
        # toolbar
        toolbar_frame = ttk.Frame(left_frame)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.grid(column=0, row=1, sticky='nsew')
        
        self.toolbar = toolbar
        
        # instructions
        label_instr = ttk.Label(right_frame, 
                    text='Instructions:\n\n'+\
                         '1. Open an image.\n'+\
                         '2. Drag lines to image ticks.\n'+\
                         '3. Enter image axis values.\n'+\
                         '4. Scale the axes.\n'+\
                         '5. Extract data with right mouse button.\n'+\
                         '6. Export data to csv.\n', 
                    justify='left')
        
        # buttons
        button_delete = ttk.Button(right_frame, text='Delete Last Data Point', command=self.delete_data, pad=5)
        button_export = ttk.Button(right_frame, text='Export Data', command=self.export_data, pad=5)
        
        r = 0
        label_instr.grid(column=0, row=r, pady=1, padx=5, sticky='ew'); r+=1
        button_delete.grid(column=0, row=r, pady=1, padx=5, sticky='ew'); r+=1
        button_export.grid(column=0, row=r, pady=1, padx=5, sticky='ew'); r+=1
        
        # axes scaling grid
        frame_scale = ttk.Frame(right_frame)
        frame_scale.grid(column=0, row=r, sticky='ew', pady=5); r+=1
        
        label_xl = ttk.Label(frame_scale, text='x (-)', justify='center')
        label_xh = ttk.Label(frame_scale, text='x (+)', justify='center')
        label_yl = ttk.Label(frame_scale, text='y (-)', justify='center')
        label_yh = ttk.Label(frame_scale, text='y (+)', justify='center')
        self.button_scale = ttk.Button(frame_scale, text='Scale Axes', command=self.do_button_scale, pad=5)
        
        self.xl_img = tk.StringVar()
        self.xh_img = tk.StringVar()
        self.yl_img = tk.StringVar()
        self.yh_img = tk.StringVar()
        
        self.entry_yupp = tk.Entry(frame_scale, textvariable=self.yh_img, width=10, justify='center')
        self.entry_ylow = tk.Entry(frame_scale, textvariable=self.yl_img, width=10, justify='center')
        self.entry_xlow = tk.Entry(frame_scale, textvariable=self.xl_img, width=10, justify='center')
        self.entry_xupp = tk.Entry(frame_scale, textvariable=self.xh_img, width=10, justify='center')
        
        label_yh.grid(column=0, row=0)
        label_yl.grid(column=0, row=1)
        
        self.entry_yupp.grid(column=1, row=0)
        self.entry_ylow.grid(column=1, row=1)
        
        self.button_scale.grid(column=2, row=0, columnspan=2, rowspan=2, padx=5, pady=5, sticky='nsew')
        
        self.entry_xlow.grid(column=2, row=2)
        self.entry_xupp.grid(column=3, row=2)
            
        label_xl.grid(column=2, row=3)
        label_xh.grid(column=3, row=3)
        
        # keyboard shortcuts
        label_keys = ttk.Label(right_frame, 
                    text='\nKeyboard Shortcuts:\n\n'+\
                         '<Ctrl+o>\tOpen file\n'+\
                         '<Ctrl+z>\t\tDelete last data point\n'+\
                         '<Enter>\t\t(Re-)Scale Axes\n'+\
                         '<o>\t\tToggle Zoom\n'+\
                         '<p>\t\tToggle Pan\n'+\
                         '<h>\t\tSet Home View\n'+\
                         '<right arrow>\tForward View\n'+\
                         '<left arrow>\tBack View\n',
                    justify='left')
        label_keys.grid(column=0, row=r, sticky='ew', pady=5); r+=1
        
        # runloop
        self.root.mainloop()

    # ======================================================================= #
    def clear_data(self):
        """
            Delete data points
        """
        
        if hasattr(self, 'data_line'):
            del self.data_line
            self.xdata = []
            self.ydata = []
        
    # ======================================================================= #
    def delete_data(self, *args):
        """
            Remove the last fetched data point
        """
        
        try:
            self.xdata.pop()
            self.ydata.pop()
        except IndexError:
            pass
        else:
            self.update_data()
        
    # ======================================================================= #
    def do_button_scale(self, *args):
        if self.button_scale['text'] == 'Scale Axes':
            try:
                self.scale_axes()
            except Exception:
                pass
            else:
                self.button_scale['text'] = 'Re-Scale'
        elif self.button_scale['text'] == 'Re-Scale':
            self.set_lines()
            self.button_scale['text'] = 'Scale Axes'
        
    # ======================================================================= #
    def draw_crosshairs(self, event):
        """
            Draw crosshairs on figure
        """
        
        if event.inaxes:
            try:
                self.crossx.set_xdata(event.xdata)
                self.crossy.set_ydata(event.ydata)
                self.fig.canvas.draw_idle()
            except AttributeError:
                pass
            
    # ======================================================================= #
    def export_data(self):
        """
            Write data to csv
        """
        
        # get filename
        filename = filedialog.asksaveasfilename(
                                            initialdir=os.path.dirname(self.filename), 
                                            title='Save Data', 
                                            filetypes=( ('csv','*.csv'), 
                                                        ('All', '*'))
                                            )
        if not filename: return
        
        # apply data transforms
        x = np.array(self.xdata)
        y = np.array(self.ydata)
        
        if self.x_scale.get() == 'log10':     x = 10**(x)
        elif self.x_scale.get() == 'ln':      x = np.exp(x)
        
        if self.y_scale.get() == 'log10':     y = 10**(y)
        elif self.y_scale.get() == 'ln':      y = np.exp(y)
        
        # write file header
        header = [  'rigur version %s' % __version__,
                    'Data stripped from %s' % self.filename, 
                    str(datetime.datetime.now()),
                    ''
                ]
                    
        with open(filename, 'w') as fid:
            for h in header:
                fid.write('# %s\n' % h)
        
        # write file body 
        dat = np.array([x, y]).T
        df = pd.DataFrame(dat, columns=['x', 'y'])
        df.to_csv(filename, index=False, mode='a')
        
    # ======================================================================= #
    def get_data(self, event):
        """
            Get data from mouse position
        """

        # check button
        if event.button != 3 or not event.inaxes:
            return
        
        # disable zoom and pan
        if self.toolbar.mode == 'pan/zoom':
            mode = 'pan/zoom'
            self.toolbar.pan()
        elif self.toolbar.mode == 'zoom rect':
            mode = 'zoom rect'
            self.toolbar.zoom()
        else:
            mode = ''
            
        # get the new data
        self.xdata.append(event.xdata)
        self.ydata.append(event.ydata)
        
        # draw
        self.update_data()
            
    # ======================================================================= #
    def open_file(self, event=None, filename=''):
        """
            Get the image
        """
        
        # ask for file
        if filename == '':
            filename = filedialog.askopenfilename(initialdir=os.getcwd(), 
                                            title='Select Image File', 
                                            filetypes=( ('All', '*'),
                                                        ('jpg', '*.jpg'), 
                                                        ('png', '*.png'), 
                                                        ('gif', '*.gif')))
        
        # get file as np array
        self.img = mpimg.imread(filename)
        self.img = self.img[::-1]
        
        # make axes
        if not hasattr(self, 'ax'):
            self.ax = self.fig.add_subplot(111)
            self.toolbar.ax = self.ax
            self.toolbar.fig = self.fig
        else:
            self.ax.clear()
            
        self.ax.tick_params(axis='both', labelsize='small')
        
        # draw basic image
        self.ax.imshow(self.img, origin='lower')
        self.ax.set_aspect(1)
        self.fig.canvas.draw_idle()
        
        self.filename = filename
        
        # get limits of image
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_xlim()
        
        xrng = xlim[1]-xlim[0]
        yrng = ylim[1]-ylim[0]
        
        self.xl_pix = xlim[0] + xrng*0.1
        self.xh_pix = xlim[1] - xrng*0.1
        self.yl_pix = ylim[0] + yrng*0.1
        self.yh_pix = ylim[1] - yrng*0.1
    
        self.x_slider_for_y = xlim[0] + xrng*0.05
        self.y_slider_for_x = ylim[0] + yrng*0.05
                
        # intialize
        self.xdata = []
        self.ydata = []
                
        # rescale axes for the first time 
        self.set_lines()
        self.xh_img.set('1')
        self.xl_img.set('0')
        self.yh_img.set('1')
        self.yl_img.set('0')
        self.scale_axes()
        self.xh_img.set('')
        self.xl_img.set('')
        self.yh_img.set('')
        self.yl_img.set('')
        self.set_lines()
        
        # clear data
        self.clear_data()
        
        # set home view
        self.toolbar.update()
        
        # make sure scale button is correct
        self.button_scale['text'] = 'Scale Axes'
        
    # ======================================================================= #
    def on_closing(self):
        """Excecute this when window is closed: destroy and close all plots."""
        self.root.destroy()

    # ======================================================================= #
    def keyrelease(self, event):
        """
            Do matplotlib actions on key release
        """
                
        if event.char in 'oph':
            if event.char == 'o':               self.toolbar.zoom()
            elif event.char == 'p':             self.toolbar.pan()
            elif event.char == 'h':             self.toolbar.home()
            elif str(event.keysym) == 'Right':  self.toolbar.forward()
            elif str(event.keysym) == 'Left':   self.toolbar.back()
            self.fig.canvas.draw_idle()
        
            # don't type in boxes
            entries = [self.entry_yupp, self.entry_ylow, self.entry_xlow, self.entry_xupp]
            focus = self.root.focus_get()
            if focus in entries:
                n = len(focus.get())
                focus.delete(n-1)
                
    # ======================================================================= #
    def set_lines(self):
        """
            Make lines and draggable points if needed, else move points to center of image
        """
        
        # make lines for draggable points
        xl = self.ax.axvline(self.xl_pix, ls='--', color='r')
        xh = self.ax.axvline(self.xh_pix, ls='--', color='r')
        yl = self.ax.axhline(self.yl_pix, ls='--', color='r')
        yh = self.ax.axhline(self.yh_pix, ls='--', color='r')
        
        self.drag_pts = {}
        
        # update functions
        def update_xl(x, _):
            xl.set_xdata([x, x])
            if x <= self.drag_pts['xh'].point.get_xdata():      self.xl_pix = x
            else:                                               self.xh_pix = x
            self.fig.canvas.draw_idle()
                
        def update_xh(x, _):
            xh.set_xdata([x, x])
            if x >= self.drag_pts['xl'].point.get_xdata():      self.xh_pix = x
            else:                                               self.xl_pix = x
            self.fig.canvas.draw_idle()
                
        def update_yl(_, x):
            yl.set_ydata([x, x])
            if x <= self.drag_pts['yh'].point.get_ydata():      self.yl_pix = x
            else:                                               self.yh_pix = x
            self.fig.canvas.draw_idle()
                
        def update_yh(_, x):
            yh.set_ydata([x, x])
            if x >= self.drag_pts['yl'].point.get_ydata():      self.yh_pix = x
            else:                                               self.yl_pix = x
            self.fig.canvas.draw_idle()
                        
        # make draggable points and lines for axis setting
        self.drag_pts['xl'] = DraggablePoint(self, update_xl, self.xl_pix, self.y_slider_for_x, sety=False, color='b')
        self.drag_pts['xh'] = DraggablePoint(self, update_xh, self.xh_pix, self.y_slider_for_x, sety=False, color='b')
        self.drag_pts['yl'] = DraggablePoint(self, update_yl, self.x_slider_for_y, self.yl_pix, setx=False, color='b')
        self.drag_pts['yh'] = DraggablePoint(self, update_yh, self.x_slider_for_y, self.yh_pix, setx=False, color='b')
        self.fig.canvas.draw_idle()
        
        # figure event handling
        self.ax.callbacks.connect('xlim_changed', self.update_drag_points)
        self.ax.callbacks.connect('ylim_changed', self.update_drag_points)
        
    # ======================================================================= #
    def scale_axes(self, event=None):
        """
            Rescale axes to match inputs
        """
        
        if not hasattr(self, 'drag_pts'):
            raise RuntimeError('No drag pts')
        
        # pixel values
        pxl = self.xl_pix
        pxh = self.xh_pix
        pyl = self.yl_pix
        pyh = self.yh_pix
        
        # units values
        uxl = float(self.xl_img.get())
        uxh = float(self.xh_img.get())
        uyl = float(self.yl_img.get())
        uyh = float(self.yh_img.get())
        
        # make sure units are ordered properly
        if uxl > uxh:   uxl, uxh = uxh, uxl
        if uyl > uyh:   uyl, uyh = uyh, uyl
    
        # transform input to linear scale
        if self.x_scale.get() == 'log10':
            uxl = np.log10(uxl)
            uxh = np.log10(uxh)
        elif self.x_scale.get() == 'ln':
            uxl = np.log(uxl)
            uxh = np.log(uxh)

        if self.y_scale.get() == 'log10':
            uyl = np.log10(uyl)
            uyh = np.log10(uyh)
        elif self.y_scale.get() == 'ln':
            uyl = np.log(uyl)
            uyh = np.log(uyh)
        
        # aspect ratios
        aspect_pix = (pxh-pxl)/(pyh-pyl)
        aspect_unt = (uxh-uxl)/(uyh-uyl)
        
        # convert
        aspect = self.ax.get_aspect()*aspect_unt/aspect_pix
        
        # linear transform for axes, pixel to units
        xtransform = lambda pix : (uxh-uxl)/(pxh-pxl) * pix + uxh - (uxh-uxl)/(pxh-pxl) * pxh
        ytransform = lambda pix : (uyh-uyl)/(pyh-pyl) * pix + uyh - (uyh-uyl)/(pyh-pyl) * pyh
        
        # get limits on axes
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        extent = [xtransform(xlim[0]), xtransform(xlim[1]), 
                  ytransform(ylim[0]), ytransform(ylim[1])]
        
        # redraw with new limit
        self.ax.clear()
        self.ax.imshow(self.img, extent=extent, origin='lower')
        self.ax.set_aspect(aspect)
        
        # set home view
        self.toolbar.update()
        
        # hide lines and points
        del self.drag_pts
        self.ax.lines = []
        
        # draw crosshairs
        self.crossx = self.ax.axvline(0.5, color='r', ls=':', lw=1)
        self.crossy = self.ax.axhline(0.5, color='r', ls=':', lw=1)
        
        # disconnect axis update
        self.ax.callbacks.disconnect('xlim_changed')
        self.ax.callbacks.disconnect('ylim_changed')
        
        # draw figure
        self.fig.canvas.draw_idle()
        
        # scale positions of lines
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        self.xl_pix = xtransform(self.xl_pix)
        self.xh_pix = xtransform(self.xh_pix)
        self.yl_pix = ytransform(self.yl_pix)
        self.yh_pix = ytransform(self.yh_pix)
        self.x_slider_for_y = xtransform(self.x_slider_for_y)
        self.y_slider_for_x = ytransform(self.y_slider_for_x)
        
        # scale data
        self.xdata = list(xtransform(np.array(self.xdata)))
        self.ydata = list(ytransform(np.array(self.ydata)))
        try:    
            del self.data_line
        except AttributeError:
            pass    
        
        self.update_data()
        
    # ======================================================================= #
    def update_data(self):
        """
            Update data points on plot
        """
        
        # first point: draw data on figure 
        if not hasattr(self, 'data_line'):
            self.ax.autoscale(False)
            self.data_line = self.ax.plot(self.xdata, self.ydata, marker='o', 
                                          ls='none', fillstyle='none', color='r')[0]
            self.ax.autoscale(True)
        else:
            self.data_line.set_xdata(self.xdata)
            self.data_line.set_ydata(self.ydata)

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
        
    # ======================================================================= #
    def update_drag_points(self, event):
        """
            Make sure the draggable points are all on screen
        """
        
        # check that draggable points exist
        if not hasattr(self, 'drag_pts'):
            return 
        
        # get limits of image
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        xrng = xlim[1]-xlim[0]
        yrng = ylim[1]-ylim[0]
        
        # get slider positions
        self.x_slider_for_y = xlim[0] + xrng*0.05
        self.y_slider_for_x = ylim[0] + yrng*0.05
        
        # set values of draggable points
        for k in ('xl', 'xh'):
            self.drag_pts[k].point.set_ydata(self.y_slider_for_x)
        for k in ('yl', 'yh'):
            self.drag_pts[k].point.set_xdata(self.x_slider_for_y)
        

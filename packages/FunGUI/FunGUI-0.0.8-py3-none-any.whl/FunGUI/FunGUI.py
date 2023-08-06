from os.path import dirname, basename, isfile, join
import os,sys
import glob
import inspect
import re
from shutil import copyfile
# from FunGUI_widgets import *
import pickle
import tkinter.filedialog as tkf
from tkinter import simpledialog
import _thread
from multiprocessing import Process
import copy

# import tkinter
import tkinter.messagebox
import traceback
import tkinter as tk
import re
import _thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np

class QGUI_widget(object):
    def __init__(self,root):
        self.display_info = {'relwidth':0,'relheight':0,'relx':0,'rely':0}
        self.root = root
        self.frame = tk.Frame(root, width=125, height=200)
        # self.frame.config(borderwidth = 3,highlightbackground="black",highlightthickness=1)
        self.widgets = []

        self.create_widgets_inside_frame()
        self.creat_menu()
        self.bind_event()
        self.style()
        self.layout()
        # self.zoom_on()

    def destroy(self):
        for w in self.widgets:
            w.destroy()
    def create_widgets_inside_frame(self):
        pass
        self.widgets = []

    def bind_event(self):
        pass

    def style(self):
        pass

    def layout(self):
        pass

    def bind(self,*arg,**kwargs):
        self.frame.bind(*arg,**kwargs)
    def grid(self,*arg,**kwargs):
        self.frame.grid(*arg,**kwargs)
    def pack(self,*arg,**kwargs):
        self.frame.pack(*arg,**kwargs)
    def place(self,*arg,**kwargs):
        self.frame.place(*arg,**kwargs)

    def creat_menu(self):
        self.m = tk.Menu(self.root, tearoff=0)
        # self.m.add_command(label="Drag and drop",command=self.drag_and_drop)
        self.m.add_command(label="Drag & Zoom on",command = self.zoom_on)
        self.m.add_command(label="Drag & Zoom off",command = self.zoom_off)
        # self.m.add_command(label="Disable",command=self.disable_widget)
        # self.m.add_command(label="Enable",command=self.enable_widget)
        for widget in self.widgets:
            widget.bind("<Button-3>", self.do_popup)
    def zoom_on(self):
        self.disable_widget()
        self.drag_and_drop()
        self.frame.config(borderwidth = 1,highlightbackground="black",highlightthickness=1)
        self.frame.bind("<Button-1>", self.zoom_out_start)
        self.frame.bind("<ButtonRelease-1>", self.release_stop_movement_zoom)



    def zoom_out_start(self,event):
        widget = event.widget
        widget._widget_start_x = widget.winfo_x()
        widget._widget_start_width = widget.winfo_width()
        widget._widget_start_height = widget.winfo_height()
        widget._widget_start_y = widget.winfo_y()
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

        border_judge = self.if_on_border_or_corner_or_corner(event)
        # #print(widget._drag_start_y)

            # widget.config(borderwidth = 3,highlightbackground="black",highlightthickness=1)
        if border_judge == 'L':
            self.frame.config(cursor="left_side")
            widget.bind("<B1-Motion>", self.zoom_out_L_motion)
        elif border_judge == 'R':
            self.frame.config(cursor="right_side")
            widget.bind("<B1-Motion>", self.zoom_out_R_motion)
        elif border_judge == 'T':
            self.frame.config(cursor="top_side")
            widget.bind("<B1-Motion>", self.zoom_out_T_motion)
        elif border_judge == 'B':
            self.frame.config(cursor="bottom_side")
            widget.bind("<B1-Motion>", self.zoom_out_B_motion)
        elif border_judge =='TL':
            self.frame.config(cursor="top_left_corner")
            widget.bind("<B1-Motion>", self.zoom_out_TL_motion)
        elif border_judge =='TR':
            self.frame.config(cursor="top_right_corner")
            widget.bind("<B1-Motion>", self.zoom_out_TR_motion)
        elif border_judge =='BL':
            self.frame.config(cursor="bottom_left_corner")
            widget.bind("<B1-Motion>", self.zoom_out_BL_motion)
        elif border_judge =='BR':
            self.frame.config(cursor="bottom_right_corner")
            widget.bind("<B1-Motion>", self.zoom_out_BR_motion)
        elif border_judge==None:
            self.frame.config(cursor="fleur")
            self.drag_and_drop()
            #print('work')

    def zoom_out_TL_motion(self,event):
        widget = event.widget
        x = self.root.winfo_pointerx()-self.root.winfo_rootx()
        zoom_out_x = widget._widget_start_x - x
        y = self.root.winfo_pointery()-self.root.winfo_rooty()
        zoom_out_y = widget._widget_start_y - y
        if x<5 or widget._widget_start_width+zoom_out_x<5or y<5 or widget._widget_start_height+zoom_out_y<5:
            pass
        else:
            widget.place(x=x,width = widget._widget_start_width+zoom_out_x,relwidth=0,
            y=y,height = widget._widget_start_height+zoom_out_y,relheight=0,relx=0.0, rely=0.0)

    def zoom_out_TR_motion(self,event):
        widget = event.widget
        x = self.root.winfo_pointerx()-self.root.winfo_rootx()
        y = self.root.winfo_pointery()-self.root.winfo_rooty()
        zoom_out_y = widget._widget_start_y - y
        zoom_out_x = x-widget._widget_start_x -widget._widget_start_width
        if widget._widget_start_width + zoom_out_x<4 or x>self.root.winfo_width()-4:
            pass
        elif x<4 or widget._widget_start_width+zoom_out_x<4:
            pass
        else:
            widget.place(x = widget._widget_start_x,width = widget._widget_start_width+zoom_out_x,relwidth=0,
            y=y,height = widget._widget_start_height+zoom_out_y,relheight=0,
            relx=0.0, rely=0.0)

    def zoom_out_BL_motion(self,event):
        widget = event.widget
        x = self.root.winfo_pointerx()-self.root.winfo_rootx()
        zoom_out_x = widget._widget_start_x - x
        y = self.root.winfo_pointery()-self.root.winfo_rooty()
        zoom_out_y = y-widget._widget_start_y -widget._widget_start_height
        if widget._widget_start_height + zoom_out_y<4 or y>self.root.winfo_height()-4:
            pass
        elif x<4 or widget._widget_start_width+zoom_out_x<4:
            pass
        else:
            widget.place(x=x,
            width = widget._widget_start_width+zoom_out_x,
            relwidth=0,
            y = widget._widget_start_y,
            height = widget._widget_start_height+zoom_out_y,
            relheight=0,
            relx=0.0, rely=0.0)

    def zoom_out_BR_motion(self,event):
        widget = event.widget
        x = self.root.winfo_pointerx()-self.root.winfo_rootx()
        zoom_out_x = x-widget._widget_start_x -widget._widget_start_width
        y = self.root.winfo_pointery()-self.root.winfo_rooty()
        zoom_out_y = y-widget._widget_start_y -widget._widget_start_height
        if widget._widget_start_height + zoom_out_y<4 or y>self.root.winfo_height()-4:
            pass
        elif widget._widget_start_width + zoom_out_x<4 or x>self.root.winfo_width()-4:
            pass
        else:
            widget.place(x = widget._widget_start_x,
            width = widget._widget_start_width+zoom_out_x,
            y = widget._widget_start_y,
            height = widget._widget_start_height+zoom_out_y,
            relx=0.0, rely=0.0,
            relwidth=0,relheight=0,
            )

    # def zoom_out_motion(self,event):
    #     pass
    def get_display_info(self):
        #print('coodinate of frame')
        #print(self.frame.winfo_x())
        #print(self.frame.winfo_y())
        #print(self.frame.winfo_width())
        #print(self.frame.winfo_height())
        self.display_info['class_name'] = self.class_name
        self.display_info['name'] = self.name
        self.display_info['input'] = self.input
        self.display_info['x'] = self.frame.winfo_x()
        self.display_info['y'] = self.frame.winfo_y()
        self.display_info['width'] = self.frame.winfo_width()
        self.display_info['height'] = self.frame.winfo_height()
        return self.display_info
    def zoom_off(self):
        self.enable_widget()
        self.get_display_info()
        self.ubind_event()
        self.frame.config(borderwidth = 3,highlightbackground="black",highlightthickness=0)
        self.frame.config(cursor="arrow")
        self.frame.unbind("<B1-Motion>")
        self.frame.unbind("<B1-Motion>")


    def release_stop_movement_zoom(self,event):
        widget = event.widget
        widget.config(borderwidth = 3,highlightbackground="black",highlightthickness=1)
        self.frame.config(cursor="fleur")

    def zoom_out_L_motion(self,event):
        widget = event.widget
        x = self.root.winfo_pointerx()-self.root.winfo_rootx()
        zoom_out_x = widget._widget_start_x - x
        if x<4 or widget._widget_start_width+zoom_out_x<4:
            pass
        else:
            widget.place(x=x,
            width = widget._widget_start_width+zoom_out_x,
            height= widget._widget_start_height,relwidth=0,relheight=0,
            relx=0.0, rely=0.0)

    def zoom_out_R_motion(self,event):
        widget = event.widget
        y = self.root.winfo_pointery()-self.root.winfo_rooty()
        x = self.root.winfo_pointerx()-self.root.winfo_rootx()
        zoom_out_x = x-widget._widget_start_x -widget._widget_start_width
        if widget._widget_start_width + zoom_out_x<4 or x>self.root.winfo_width()-4:
            pass
        else:
            widget.place(x = widget._widget_start_x,
            width = widget._widget_start_width+zoom_out_x,
            height= widget._widget_start_height,relx=0.0, rely=0.0,
            relwidth=0,relheight=0,
            )

    def zoom_out_T_motion(self,event):
        widget = event.widget
        y = self.root.winfo_pointery()-self.root.winfo_rooty()
        x = self.root.winfo_pointerx()-self.root.winfo_rootx()
        zoom_out_y = widget._widget_start_y - y
        if y<4 or widget._widget_start_height+zoom_out_y<4:
            pass
        else:
            widget.place(y=y,
            height = widget._widget_start_height+zoom_out_y,
            width = widget._widget_start_width,relx=0.0, rely=0.0,
            relwidth=0,relheight=0,)

    def zoom_out_B_motion(self,event):
        widget = event.widget
        y = self.root.winfo_pointery()-self.root.winfo_rooty()
        zoom_out_y = y-widget._widget_start_y -widget._widget_start_height
        if widget._widget_start_height + zoom_out_y<4 or y>self.root.winfo_height()-4:
            pass
        else:
            widget.place(y = widget._widget_start_y,
            height = widget._widget_start_height+zoom_out_y,
            width = widget._widget_start_width,relx=0.0, rely=0.0,
            relwidth=0,relheight=0)


    def if_on_border_or_corner_or_corner(self,event):
        widget = event.widget
        x = event.x
        y = event.y
        range =10
        x0,y0 = 0,0
        w,h = widget.winfo_width(),widget.winfo_height()

        if_on_left_border = x<x0+range and y>y0+range and y<h-range
        if_on_top_border =  y<y0+range and x>x0+range and x<w-range
        if_on_right_border = x>w-range and y>y0+range and y<h-range
        if_on_bottom_border = y>h-range and x>x0+range and x<w-range
        if_on_tl_corner = y < range and x<range
        if_on_tr_corner = y < range and x>w-range
        if_on_bl_corner = y>h-range and x<range
        if_on_br_corner = y>h-range and x>w-range
        if if_on_left_border:
            #print('L')
            widget.config(borderwidth = 3,highlightbackground="black",highlightthickness=1.5)
            return 'L'
        elif if_on_top_border:
            #print('T')
            widget.config(borderwidth = 3,highlightbackground="black",highlightthickness=1.5)
            return 'T'
        elif if_on_right_border:
            #print('R')
            return 'R'
        elif if_on_bottom_border:
            #print('B')
            return 'B'
        elif if_on_tl_corner:
            #print('TL')
            return('TL')
        elif if_on_tr_corner:
            #print('TR')
            return('TR')
        elif if_on_bl_corner:
            #print('BL')
            return('BL')
        elif if_on_br_corner:
            #print('BR')
            return('BR')

        return None

    def do_popup(self,event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def disable_widget(self):
        for widget in self.widgets:
            try:
                widget.configure(state=tk.DISABLED)
            except:
                print(widget)

    def enable_widget(self):
        for widget in self.widgets:
            try:
                widget.configure(state=tk.NORMAL)
            except:
                print(widget)

    def drag_and_drop(self):
        self.frame.focus()
        self.make_draggable(self.widgets)


    def make_draggable(self,widgets):
        for widget in widgets:
            self.frame.config(cursor="fleur")
            widget.bind("<Button-1>", lambda event: self.on_drag_start(event))
            widget.bind("<B1-Motion>", self.on_drag_motion)
            widget.bind("<ButtonRelease-1>", self.release_stop_movement)


    def on_drag_start(self,event):
        # widget = event.widget
        widget = self.frame
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(self,event):
        # widget = event.widget
        self.frame.config(borderwidth = 3,highlightbackground="black",highlightthickness=1)
        widget = self.frame
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        # #print(widget._drag_start_y,event.y)
        if x<0: x=0
        if y<0: y=0
        if x>self.root.winfo_width()-widget.winfo_width():x = self.root.winfo_width()-widget.winfo_width()
        if y>self.root.winfo_height()-widget.winfo_height():y = self.root.winfo_height()-widget.winfo_height()
        widget.place(x=x, y=y,relx=0.0, rely=0.0)

    def ubind_event(self):
        # self.frame.config(cursor="arrow")
        for widget in self.widgets:
            self.frame.config(cursor="arrow")
            widget.unbind("<Button-1>")
            widget.unbind("<B1-Motion>")
            widget.unbind("<ButtonRelease-1>")

    def release_stop_movement(self,event):
        widget=self.frame
        widget._widget_start_x = widget.winfo_x()
        widget._widget_start_width = widget.winfo_width()
        widget._widget_start_height = widget.winfo_height()
        widget._widget_start_y = widget.winfo_y()
        # self.frame.config(borderwidth = 3,highlightbackground="black",highlightthickness=0)
        # self.ubind_event()

    def isfloat(self,s):
        try:
            return float(s)<float('inf')
        except:
            return False

    def isInt(self,s):
        try:
            return int(s)<float('inf')
        except:
            return False


class changable_listbox(QGUI_widget):
    def __init__(self,root,input= [*range(15)],name = 'list'):
        self.class_name = 'changable_listbox'
        self.input = input
        self.name = name
        QGUI_widget.__init__(self, root)


    def create_widgets_inside_frame(self):
        self.L = tk.Label(self.frame,text = self.name)
        self.sb = tk.Scrollbar(self.frame)
        self.E1 = tk.Entry(self.frame)
        self.v = tk.StringVar(value=self.input)
        self.b1=tk.Listbox(self.frame,activestyle='dotbox',yscrollcommand=self.sb.set,
        listvariable=self.v,selectmode='SINGLE')
        self.sb.config(command=self.b1.yview)
        self.widgets = [self.sb,self.E1,self.b1,self.L]

    def layout(self):
        self.sb.pack(side=tk.RIGHT,fill=tk.Y)
        self.L.pack(fill=tk.BOTH, expand=True)
        self.E1.pack(fill=tk.BOTH, expand=True)

        self.b1.pack(fill=tk.BOTH, expand=True)

    def style(self):
        self.style1 = {}
        # self.style1['activestyle']="dotbox"
        self.style1['background']="#9DC3E6"
        # self.style1['cursor']="arrow"
        # self.style1['activestyle']="dotbox"
        self.style1['foreground']="#404040"
        self.b1.configure(**self.style1)
        self.E1.configure(**self.style1)
        self.E1.configure(background = '#faeec9')
        self.sb.configure(troughcolor = '#9DC3E6')
        self.sb.configure(background = '#9DC3E6')
        # self.frame.configure(background = '#9DC3E6')

    def bind_event(self):
        self.b1.bind('<Double-1>', self.edit_item)
        self.E1.bind('<Return>',self.set_item)

    def edit_item(self,event):
        text = self.E1.selection_get()
        # set_entry_text(text)
        self.E1.focus()

    def set_item(self,event):
        text = self.E1.get()
        self.E1.delete(0,tk.END)
        # #print(len(text))
        if len(text)>4 and text[:4]=='cmd:':
            text = text.replace('list','self.input')
            cmd = text[4:].lstrip()
        else:
            if self.b1.curselection():
                index = self.b1.curselection()[0]
                if text=='del'or text == 'delete'or text=='d':
                    del self.input[index]
                elif 'insert' in text or 'i' in text:
                    if 'insert' in text:
                        text=text[6:].strip()
                    else:
                        text=text[1:].strip()
                    cmd = 'self.input.insert(index,'+text+')'
                    exec(cmd)
                else:
                    cmd = 'self.input[index] ='+text
                    exec(cmd)

            else:
                cmd = 'self.input.append('+text+')'
                exec(cmd)


        self.v.set(self.input)

class changable_slide(QGUI_widget):
    def __init__(self,root,input=15.569,name = 'variable'):
        self.class_name = 'changable_slide'
        self.input = input
        self.name = name
        QGUI_widget.__init__(self,root)

    def create_widgets_inside_frame(self):
        self.var = tk.DoubleVar()
        self.var.set(self.input)
        self.slide_conf = {}
        self.slide_conf['from_'] = self.input - abs(self.input)
        self.slide_conf['to']    = self.input + abs(self.input)
        self.slide_conf['resolution'] = self.get_precision(self.input)
        self.slide_conf['label'] = self.name
        self.slide_conf['orient'] = "horizontal"
        self.slide_conf['variable'] = self.var
        self.slide_conf['length']=120

        # self.l_name = tk.Label(self.frame,text = self.name)
        self.S = tk.Scale(self.frame, **self.slide_conf)
        self.frame_1 = tk.Frame(self.frame)
        self.frame_2 = tk.Frame(self.frame)

        self.l_max = tk.Label(self.frame_1,text = 'Max')
        self.l_min = tk.Label(self.frame_1,text = 'Min')
        self.l_step = tk.Label(self.frame_1,text = 'Step')
        self.l_value = tk.Label(self.frame_1,text = 'Value')
        self.E_max = tk.Entry(self.frame_2)
        self.E_min = tk.Entry(self.frame_2)
        self.E_step = tk.Entry(self.frame_2)
        self.E_value = tk.Entry(self.frame_2)
        self.set_entry_text(self.E_max,self.slide_conf['to'])
        self.set_entry_text(self.E_min,self.slide_conf['from_'])
        self.set_entry_text(self.E_step,self.slide_conf['resolution'])
        self.set_entry_text(self.E_value,self.slide_conf['variable'].get())
        self.S.set(self.input)

        self.widgets = [self.frame_1,self.frame_2,self.frame,self.S,self.l_max,
        self.l_min,self.l_step,self.E_max,self.E_min,self.E_step,self.E_value,self.l_value]

    def bind_event(self):
        pass
        self.S.config(command=self.slide_callback)
        self.E_max.bind('<Return>',self.set_slide_config)
        self.E_min.bind('<Return>',self.set_slide_config)
        self.E_step.bind('<Return>',self.set_slide_config)
        self.E_value.bind('<Return>',self.set_slide_config)


    def slide_callback(self,event):
        self.input = self.var.get()
        self.set_entry_text(self.E_value,self.input)

        # #print(self.input)
    def update_entry(self,widget,item):
        text = widget.get()
        # print(item,self.slide_conf['variable'],type(self.slide_conf[item]) == type(self.var))
        if type(self.slide_conf[item]) == type(self.var):
            self.set_entry_text(widget,float(text))
            self.var.set(float(text))
            self.input = float(text)
            # self.slide_conf[item] = self.var.get()
        elif self.isfloat(text):
            self.set_entry_text(widget,float(text))
            self.slide_conf[item] = float(text)
        else:
            self.set_entry_text(widget,self.slide_conf[item])


    def set_slide_config(self,event):
        self.update_entry(self.E_max,'to')
        self.update_entry(self.E_min,'from_')
        self.update_entry(self.E_step,'resolution')
        self.update_entry(self.E_value,'variable')
        self.S.config(**self.slide_conf)
        # print(self.slide_conf['variable'])
        # self.S.set(self.slide_conf['variable'].get())
        # self



    def style(self):
        pass

    def layout(self):
        # self.S.pack(fill=tk.BOTH, expand=True)
        # self.S.grid(row=0, column=0,sticky=tk.NSEW,columnspan=3)
        # self.l_min.grid(row=1, column=0,sticky=tk.NSEW)
        # self.E_min.grid(row=1, column=1,sticky=tk.NSEW)
        # self.l_max.grid(row=2, column=0,sticky=tk.NSEW)
        # self.E_max.grid(row=2, column=1,sticky=tk.NSEW)
        # self.l_step.grid(row=3, column=0,sticky=tk.NSEW)
        # self.E_step.grid(row=3, column=1,sticky=tk.NSEW)
        # self.l_value.grid(row=4, column=0,sticky=tk.NSEW)
        # self.E_value.grid(row=4, column=1,sticky=tk.NSEW)

        self.S.pack(side=tk.TOP, expand=True,fill=tk.BOTH)
        self.frame_1.pack(side=tk.LEFT,expand=True,fill=tk.Y)
        self.frame_2.pack(side=tk.LEFT,expand=True,fill=tk.Y)
        self.l_min.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.l_max.pack(side=tk.TOP,fill=tk.BOTH, expand=True)
        self.l_step.pack(side=tk.TOP,fill=tk.BOTH, expand=True)
        self.l_value.pack(side=tk.TOP,fill=tk.BOTH, expand=True)

        # l = tk.Label(self.frame)
        # l.pack(side=tk.TOP,fill=tk.X)
        self.E_min.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.E_max.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.E_step.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.E_value.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        #
        #
        #
        # s
        #
    def set_entry_text(self,Entry,text):
        Entry.delete(0,tk.END)
        Entry.insert(0,text)

    def get_precision(self,value):
        s = str(value)
        if s.find('.')>-1:
            s = s.strip('0')
            s = s[s.find('.')+1:]
            return 10**(-len(s))
        else:
            return 1

class changable_checkboxes(QGUI_widget):
    def __init__(self,root,input = {'test1':True,'test2':False},name = 'check box'):
        self.class_name = 'changable_checkboxes'
        self.dict = {}
        self.input = input
        for i in self.input:
            self.dict[i] = tk.BooleanVar()
            if self.input[i] == True:
                self.dict[i].set(True)
            else:
                self.dict[i].set(False)

        self.name = name
        QGUI_widget.__init__(self, root)
        # #print(self.changing_item_text)
    def checkboxes_widget_call_back(self,v):
        self.input = self.get_input()
        pass
        # self.input[self.changing_item_text] = v.get()
        # #print(v.get())

    def create_widgets_inside_frame(self):
        self.L = tk.Label(self.frame,text = self.name)
        self.widgets = [self.L]
        for i in self.dict:
            var = self.dict[i]
            checkboxes_widget = tk.Checkbutton(self.frame, text=i, variable=var,
            command = lambda: self.checkboxes_widget_call_back(var))
            self.widgets.append(checkboxes_widget)
        # #print(self.widgets)

    def layout(self):
        # self.L.pack()
        for i in self.widgets:
            i.pack(fill=tk.BOTH, expand=True)

    def bind_event(self):
        #
        for widget in self.widgets:
            widget.bind('<Double-1>', self.edit_text)


    def edit_text(self,event):
        # #print('start')
        self.temp_text = ''
        self.changing_item_text = ''
        widget = event.widget
        self.changing_item_text = widget.cget('text')
        widget.focus_set()
        widget.bind("<Key>", self.key_input)
        # event.widget.config(text = )
    def key_input(self,event):
        widget = event.widget
        self.temp_widget = widget
        # #print(event.char)
        if event.char =='\r':
            widget.unbind("<Key>")
            self.dict[self.temp_text] = self.dict.pop(self.changing_item_text)
            self.input[self.temp_text] = self.input.pop(self.changing_item_text)
            #print(self.input)
        elif event.char =='\b':
            # #print('what is the ')
            l = len(self.temp_text)
            if l>0:
                self.temp_text = self.temp_text[:l-1]
                widget.config(text = self.temp_text)

        else:
            self.temp_text+= event.char
            widget.config(text = self.temp_text)

        # #print("pressed", repr(event.char))

    def get_input(self):
        dict = {}
        for i in self.dict:
            dict[i] = self.dict[i].get()
        return dict

class changable_text(QGUI_widget):
    def __init__(self,root,name = 'text_display',input = 'Test'):
        self.class_name = 'changable_text'
        self.name = name
        self.input = input
        QGUI_widget.__init__(self, root)

    def create_widgets_inside_frame(self):
        # self.L = tk.Label(self.frame,text = self.name)
        self.w = tk.Text(self.frame, wrap='word')
        self.b = tk.Button(self.frame,text = 'Input '+self.name,command=self.getTextInput)
        self.w.config(width=20,height=7)

        # self.sb1=tk.Scrollbar(self.frame, orient='horizontal' )
        # self.w.config( yscrollcommand=self.sb1.set )
        # self.sb1.config( command=self.w.xview )
        self.sb=tk.Scrollbar(self.frame, orient='vertical' )
        self.w.config( yscrollcommand=self.sb.set )
        self.sb.config( command=self.w.yview )
        # self.w.insert(font='Arial 12 italic')
        self.w.insert(1.0, self.input )
        # self.w.config(state=tk.DISABLED)
        # self.w.config(state=tk.DISABLED)

        # self.l = tk.Label(self.frame,text = self.input)
        self.widgets = [self.b,self.w,self.sb,self.frame]
    def layout(self):
        # self.L.pack(side=tk.TOP,fill=tk.X)
        self.b.pack(side=tk.TOP,fill=tk.BOTH)
        # self.sb1.pack(side=tk.TOP,fill=tk.X,expand = True)
        self.sb.pack(side=tk.RIGHT,fill=tk.Y)
        self.w.pack(fill=tk.BOTH,expand = True)

        # self.frame.place(width = 100,height=100,relheight=0,relx=0.0, rely=0.0,relwidth=0)

    def style(self):
        # self.w.config(bg=self.b.cget('bg'))
        pass
        # self.frame.place(width = 10,height=10,relheight=0,relx=0.0, rely=0.0,relwidth=0)

    def getTextInput(self):
        self.input=self.w.get("1.0","end")
        self.input= self.input[:-1]

class changable_button(QGUI_widget):
    def __init__(self,root,name = 'hao',input = lambda : 2 + 1):
        self.class_name = 'changable_button'
        self.name = name
        self.input = input
        QGUI_widget.__init__(self, root)

    def create_widgets_inside_frame(self):
        self.Button = tk.Button(self.frame,text =self.name,command=self.button_call_back,font=("SimSun", 10))
        self.Button.config(width=5,height=1)
        self.widgets = [self.frame,self.Button]
    def layout(self):
        self.Button.pack(side=tk.TOP,expand=True,fill=tk.BOTH)

    def button_call_back(self):
        _thread.start_new_thread(self.call_back,())

    def call_back(self):
        self.input()
        pass


class plot_display(QGUI_widget):
    def __init__(self,root,input=[np.arange(0, 3, .01),[i*2 for i in range(300)],[i*2+30 for i in range(300)]],name='',labels=''):
        self.class_name = 'plot_display'
        # self.input = value
        self.input = input
        self.name = name
        self.labels = labels
        QGUI_widget.__init__(self,root)
        self.update()
    def update(self):
        self.axes1.cla()
        for i in self.input[1:]:
            self.axes1.plot(self.input[0],i)
        self.style()
        self.canvas.draw()

    # def update(self):
    #     self.axes1.cla()
    #     self.style()
    def create_widgets_inside_frame(self):
        self.fig = Figure(figsize=(5, 3), dpi=80,facecolor = 'k')
        self.axes1 =self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        self.toolbar.update()
        self.canvas_widget = self.canvas.get_tk_widget()
        self.widgets = [self.canvas_widget,self.toolbar]
        self.fig.tight_layout()

    def bind_event(self):
        pass

    def style(self):
        pass
        self.set_black_and_white_style1()

    def layout(self):
        self.fig.tight_layout()
        # self.canvas.get_tk_widget().pack()
        # self.fig.tight_layout()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        pass

    def set_X_Y_label(self):
        if len(self.labels) ==2:
            self.axes1.set_xlabel(self.labels[0])
            self.axes1.set_ylabel(self.labels[1])
            self.fig.tight_layout()

    def set_black_and_white_style1(self):
        self.axes1.set_facecolor('k')
        self.axes1.grid(color = 'w')
        self.axes1.autoscale(enable=True, axis='y', tight=True)
        self.axes1.yaxis.grid(color='w',linewidth=1)
        self.axes1.xaxis.label.set_color('w')
        self.axes1.yaxis.label.set_color('w')
        self.axes1.xaxis.grid(color='w',linewidth=1)
        self.axes1.spines['bottom'].set_color('white')
        self.axes1.spines['top'].set_color('white')
        self.axes1.spines['left'].set_color('white')
        self.axes1.spines['right'].set_color('white')
        # self.fig.tight_layout()
        for label in self.axes1.xaxis.get_ticklabels():
                    # label is a Text instance
            label.set_color('w')
        for label in self.axes1.yaxis.get_ticklabels():
            # label is a Text instance
            label.set_color('w')
            # label.set_rotation(45)
            # label.set_fontsize(1)
        for line in self.axes1.yaxis.get_ticklines():
            # line is a Line2D instance
            line.set_color('w')
        for line in self.axes1.xaxis.get_ticklines():
            # line is a Line2D instance
            line.set_color('w')
            # line.set_markersize(25)
            # line.set_markeredgewidth(3)
        for line in self.axes1.xaxis.get_gridlines():
            line.set_color('w')

        for line in self.axes1.yaxis.get_gridlines():
            line.set_color('w')
            line.set_markeredgewidth(8)

class text_display(QGUI_widget):
    def __init__(self,root,name='name1',input = 'Test'):
        self.class_name = 'text_display'
        self.name = name
        self.input = input
        QGUI_widget.__init__(self, root)
    def update(self):
        self.w.config(state=tk.NORMAL)
        self.w.delete(1.0, tk.END)
        self.w.insert(1.0, self.input)
        self.w.config(state=tk.DISABLED)
    def create_widgets_inside_frame(self):
        self.l = tk.Label(self.frame,text = self.name)
        self.w = tk.Text(self.frame, wrap='word')
        # self.w.config(width=17,height=11)
        # self.sb1=tk.Scrollbar(self.frame, orient='horizontal' )
        # self.w.config( yscrollcommand=self.sb1.set )
        # self.sb1.config( command=self.w.xview )

        self.sb=tk.Scrollbar(self.frame, orient='vertical' )
        self.w.config( yscrollcommand=self.sb.set )
        self.sb.config( command=self.w.yview )
        # self.w.insert(font='Arial 12 italic')
        self.w.insert(1.0, self.input )
        self.w.config(state=tk.DISABLED)
        # self.w.config(state=tk.DISABLED)

        # self.l = tk.Label(self.frame,text = self.input_text)
        self.widgets = [self.w,self.sb,self.l,self.frame]
    def style(self):
        self.w.config(bg=self.l.cget('bg'))
    def layout(self):
        self.l.pack()
        self.sb.pack(side=tk.RIGHT,fill=tk.Y)
        self.w.pack(fill=tk.BOTH,expand = True)
        # self.sb1.pack(side=tk.BOTTOM,fill=tk.X)

class list_display(QGUI_widget):
    def __init__(self,root,name = 'list',input = [*range(15)]):
        self.class_name = 'list_display'
        self.name = name
        self.input = input
        QGUI_widget.__init__(self, root)

    def update(self):
        self.v.set(self.input)
    def create_widgets_inside_frame(self):
        self.L = tk.Label(self.frame,text = self.name)
        self.sb = tk.Scrollbar(self.frame)
        # self.E1 = tk.Entry(self.frame)
        self.v = tk.StringVar(value=self.input)
        self.b1=tk.Listbox(self.frame,activestyle='dotbox',yscrollcommand=self.sb.set,
        listvariable=self.v,selectmode='SINGLE')
        self.sb.config(command=self.b1.yview)
        self.widgets = [self.sb,self.b1,self.L,self.frame]

    def layout(self):
        self.L.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.sb.pack(side=tk.RIGHT,fill=tk.Y)
        # self.E1.pack()
        self.b1.pack()

    def style(self):
        self.style1 = {}
        # self.style1['activestyle']="dotbox"
        self.style1['background']="#9DC3E6"
        self.style1['cursor']="arrow"
        # self.style1['activestyle']="dotbox"
        self.style1['foreground']="#404040"
        self.b1.configure(**self.style1)
        self.sb.configure(troughcolor = '#9DC3E6')
        self.sb.configure(background = '#9DC3E6')
        self.frame.configure(background = '#9DC3E6')

class num_display(QGUI_widget):
    def __init__(self,root,name = 'num',input = 10.0):
        self.class_name = 'num_display'
        self.name = name
        self.input = input
        self.var = tk.StringVar()
        self.var.set(str(self.input))
        QGUI_widget.__init__(self, root)

    def update(self):
        self.var.set(str(self.input))
        # self.l.config(text = )

    def create_widgets_inside_frame(self):
        self.l_name = tk.Label(self.frame,text=self.name)
        self.l = tk.Label(self.frame,textvariable=self.var)
        self.l.config(width=20,height=9)
        self.widgets = [self.l_name,self.l,self.frame]
    def layout(self):
        self.l_name.pack(side=tk.TOP,expand=True,fill=tk.BOTH)
        self.l.pack(side=tk.TOP,expand=True,fill=tk.BOTH)


class get_fun_info(object):
    def __init__(self,file_name,fun_name):
        self.input_dict = {}
        self.module = self.file_name2module_name(file_name)
        copyfile(file_name, self.module +'_for_GUI.py')
        file_name = self.module +'_for_GUI'

        self.fun_name = fun_name
        self.file_name = file_name
        self.check_display_value()
        self.get_main_fun()
        self.output_dict = self.get_output_dict()
        if inspect.isfunction(self.main_fun):
            para = inspect.getargspec(self.main_fun)
            self.fun_agrs=para[0]
            # print(self.fun_agrs)
            self.fun_defaults = para[3]
            # print(self.fun_defaults)

        if self.check_if_all_has_default_value():
            self.get_input_dict()
            self.generate_the_GUI()
        else:
            print('Please provide default value for all arguments in the funciton')
    def get_main_fun(self):
        self.module = self.file_name2module_name(self.file_name)
        if self.check_fun_exist():
            cmd = 'main_fun ='+self.module+'.'+self.fun_name
            # print(cmd)
            exec(cmd,globals())
        self.main_fun = main_fun

    def check_display_value(self):
        with open(self.file_name+'.py','r') as py_file:
            lines = py_file.readlines()
        lines.append('# end')
        lines.insert(0,'output_dict = {}\n')
        # line = [i.lstrip() for i in line]

        re_string = '.*=.*#.*@'
        display_lines = [i for i, word in enumerate(lines) if re.search(re_string, word)]
        # print(display_lines)
        insert_times = 0


        # display_lines = [i for i, word in enumerate(lines) if re.search(re_string, word)]
        for i in display_lines:
            i+=insert_times
            space_count = len(lines[i]) - len(lines[i].lstrip())
            str1 = lines[i].lstrip()
            ind = str1.find('=')
            variable2show = str1[:ind].rstrip()
            insert_str2 = ' '*space_count + 'output_dict' +'[\''+variable2show+'\']'+ ' = '+variable2show+'\n'

            lines.insert(i+1,insert_str2)

            # print(len(lines))
            insert_times += 1

        if len(display_lines) > 0:
            re_string = 'def '+self.fun_name+'(.*)'
            fun_def_line = [i for i, word in enumerate(lines) if re.search(re_string, word)]
            fun_end_line = [i for i, word in enumerate(lines) if word.find('):')>-1]
            num = [i-fun_def_line[0] for i in fun_end_line if i-fun_def_line[0]>0]
            i =min(num)+fun_def_line[0]+1
            j = fun_def_line[0]
            # print(i)
            space_count = len(lines[j]) - len(lines[j].lstrip())+4
            insert_str1 = ' '*space_count + 'global output_dict'+'\n'
            lines.insert(i,insert_str1)

        with open(self.file_name+'.py', 'w') as out_file:
            out_file.writelines(lines)

    def get_output_dict(self):
        cmd = 'output_dict = '+self.module+'.output_dict'
        exec(cmd,globals())
        self.output_dict = output_dict
        # print(output_dict)
        return output_dict

        # print(self.main_fun)
    def check_if_all_has_default_value(self):
        # print(len(self.fun_agrs))
        # print(len(self.fun_defaults))
        if len(self.fun_agrs) == len(self.fun_defaults):
            print('All parameters have the default value!')
            return True
        else:
            print('Some parameters have no default value!')
            return False
    def get_input_dict(self):
        for i in range(len(self.fun_agrs)):
            self.input_dict[self.fun_agrs[i]]=self.fun_defaults[i]
            if type(self.fun_defaults[i]) == type([]):
                self.input_dict[self.fun_agrs[i]]= copy.deepcopy(self.fun_defaults[i])

    def generate_the_GUI(self):
        pass

    def file_name2module_name(self,file_name):
        from os.path import basename
        if file_name[-3:] == '.py':
            return basename(file_name)[:-3]
        else:
            return file_name

    def check_fun_exist(self):
        file_name = self.module
        fun_name = self.fun_name
        cmd = 'import '+file_name
        try:
            exec(cmd,globals())
            print('Find '+file_name)
        except:
            print('No such file or module')
            return False
        cmd = 'main_fun = '+file_name+'.'+fun_name
        # exec(cmd)
        try:
            exec(cmd,globals())
            print('Find '+fun_name)
            return True
        except:
            print('No such function in the file')
            return False

class auto_generate_GUI(get_fun_info):
    def __init__(self,file_name='',fun_name='',pickle_name = ''):
        tk.Tk.report_callback_exception = self.callback_error
        self.if_main_fun_run = False
        self.cycle_start = False
        self.creat_root()
        self.creat_menu()
        if pickle_name == '' and file_name == '' and fun_name=='':
            pass
        elif pickle_name.find('.fgui')>-1:
            path, filename = os.path.split(pickle_name)
            self.load_pickle_file(pickle_name)
        elif file_name.find('.py')>-1 and fun_name == '' and file_name[-4].find('.py')>-1:
            self.load_py_file()
        elif pickle_name[-3:] == '' and file_name != '' and fun_name !='':
            get_fun_info.__init__(self, file_name,fun_name)
            if not self.check_if_all_has_default_value():
                print('Error! the target function has some arguments without default value')
                return None
            self.main_fun(**self.input_dict)
            self.creat_widgets_from_input_dict()
            self.creat_widgets_from_output_dict()
            self.creat_main_fun_widgets()
            self.layout_widgets()
        self.update_display_widgets()
        self.display()

        # print('next')
    def creat_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file = tk.Menu(menu,tearoff=0)
        file.add_command(label="Save",command=self.save_GUI)
        file.add_command(label="Load",command=self.load_GUI)
        menu.add_cascade(label="File", menu=file)
        operate = tk.Menu(menu,tearoff=0)
        operate.add_command(label="Zoom on all",command=self.zoom_on_all)
        operate.add_command(label="Zoom off all",command=self.zoom_off_all)
        menu.add_cascade(label="Layout", menu=operate)
        cycle = tk.Menu(menu,tearoff = 0)
        cycle.add_command(label = 'Start cycle',command = self.start_cycle)
        cycle.add_command(label = 'Break cycle',command = self.stop_cycle)
        menu.add_cascade(label="Cycle", menu=cycle)

    def start_cycle(self):
        self.if_main_fun_run = True
        # print('self.if_main_fun_run',self.if_main_fun_run)
        self.cycle_start = True


    def stop_cycle(self):
        self.cycle_start = False
        self.if_main_fun_run == False

    def zoom_on_all(self):
        for w in self.input_widgets:
            w.zoom_on()
        for w in self.output_widgets:
            w.zoom_on()
        self.main_fun_btn.zoom_on()

    def zoom_off_all(self):
        for w in self.input_widgets:
            w.zoom_off()
        for w in self.output_widgets:
            w.zoom_off()
        self.main_fun_btn.zoom_off()

    def save_GUI(self):
        self.GUI_variables = {}
        self.GUI_variables['self.input_widgets'] = self.input_widgets
        self.GUI_variables['self.output_widgets'] = self.output_widgets
        self.GUI_variables['self.main_fun_btn'] = [self.main_fun_btn]

        self.widgets_info = {}
        tempt = []
        for name in self.GUI_variables:
            tempt = []
            for w in self.GUI_variables[name]:
                tempt.append(w.get_display_info())
            self.widgets_info[name] = tempt
        self.widgets_info['widgets'] = self.widgets_info
        self.widgets_info['root_geometry'] = self.root.winfo_geometry()
        self.widgets_info['fun'] = {'file_name':self.file_name,'fun_name':self.fun_name}

                # self.widgets_info = w.get_display_info()
        # print(self.widgets_info['self.main_fun_btn'])
        del self.widgets_info['widgets']['self.main_fun_btn'][0]['input']
        # self.widgets_info['self.main_fun_btn'][0]['input'] = lambda : 2 + 1

        files = [('Fun GUI Files', '*.fgui'),
                 ('All Files', '*.*'),]
        file = tkf.asksaveasfile(filetypes = files, defaultextension = files,mode = 'wb')
        pickle.dump(self.widgets_info, file,protocol=pickle.HIGHEST_PROTOCOL)
        file.close()

        # # tkf.SaveAs()
        # print(file)

    def load_GUI(self):
        try:
            self.destroy_widgets_for_load()
        except:
            pass

        file_name = self.get_filename_for_load()


        path, filename = os.path.split(file_name)
        sys.path.append(path)
        if filename.find('.fgui')>-1:
            self.load_pickle_file(file_name)

        elif filename.find('.py')>-1:
            self.load_py_file(path,filename)


    def load_py_file(self,path,filename):
        sys.path.append(path)
        file_name = path+'/'+filename
        fun_name = simpledialog.askstring(title="function",
                              prompt="Please input the function name for the GUI?")
        get_fun_info.__init__(self, file_name,fun_name)
        if not self.check_if_all_has_default_value():
            print('Error! the target function has some arguments without default value')
            return None
        self.main_fun(**self.input_dict)
        self.creat_widgets_from_input_dict()
        self.creat_widgets_from_output_dict()
        self.creat_main_fun_widgets()
        self.layout_widgets()

    def load_pickle_file(self,filename):
        with open(filename, 'rb') as handle:
            self.widgets_info = pickle.load(handle)
        # print(self.widgets_info)
        self.file_name = self.widgets_info['fun']['file_name']
        self.fun_name = self.widgets_info['fun']['fun_name']
        self.get_main_fun()
        self.creat_widgets_for_load()
        self.creat_arguments_for_load()
        # self.root.quit()
        # self.update_display_widgets()
        # self.display() head, tail = os.path.split("/tmp/d/a.dat")
    def get_filename_for_load(self):
        files = [('Fun GUI Files', '*.fgui'),
                 ('Python script','*.py'),
                 ('All Files', '*.*'),]
        filename  = tkf.askopenfilename(filetypes = files,title = "choose your file")
        return filename

    def destroy_widgets_for_load(self):
        for i in self.output_widgets:
            i.destroy()
            del i
        for i in self.input_widgets:
            i.destroy()
            del i
        self.main_fun_btn.destroy()
        del self.main_fun_btn
            # print(i.name)
    def creat_widgets_for_load(self):
        self.input_widgets,self.output_widgets = [],[]
        for name in self.widgets_info['widgets']:
            for dic in self.widgets_info['widgets'][name]:
                if name == 'self.input_widgets':
                    self.input_widgets.append(self.creat_widget_for_load(dic))
                elif name == 'self.output_widgets':
                    self.output_widgets.append(self.creat_widget_for_load(dic))
                elif name == 'self.main_fun_btn':
                    self.main_fun_btn = self.creat_widget_for_load(dic)
        self.seperate_plot_widgets()
        self.root.geometry(self.widgets_info['root_geometry'])
    def creat_arguments_for_load(self):
        self.output_dict,self.input_dict = {},{}
        for w in self.input_widgets:
            self.input_dict[w.name] = w.input
            if type(w.input) == type([]):
                self.input_dict[w.name] = copy.deepcopy(w.input)
        for w in self.output_widgets:
            self.output_dict[w.name] = w.input

    def creat_widget_for_load(self,display_info):
        try:
            input = display_info['input']
        except:
            input = self.main
        class_name = display_info['class_name']
        name = display_info['name']
        x = display_info['x']
        y = display_info['y']
        width = display_info['width']
        height = display_info['height']
        cmd = 'w = '+class_name+'(self.root,name = name,input=input)'
        exec(cmd,locals(),globals())
        w.place(x=x,y=y,width=width,height=height,relwidth=0,relheight=0,relx=0.0, rely=0.0)
        return w
    def creat_root(self):
        self.root=tk.Tk()
        self.root.geometry("1000x800")
        this_dir, this_filename = os.path.split(__file__)
        DATA_PATH = os.path.join(this_dir, "title.png")
        print(DATA_PATH)
        p1 = tk.PhotoImage(file = DATA_PATH)

        self.root.title("FunGUI")
        # self.root.iconbitmap(p1)

# Setting icon of master window
        self.root.iconphoto(False, p1)
        self.root.iconwindow()

    def update_input(self):
        res = False
        for w in self.input_widgets:
            # print(self.input_dict[w.name])
            # print(w.input)
            if self.input_dict[w.name] != w.input:
                res = True
                self.input_dict[w.name] = w.input
                if type(w.input) == type([]):
                    self.input_dict[w.name] = copy.deepcopy(w.input)
        # print(res)
        return res

    def update_output(self):
        for w in self.other_widgets:
            w.input = self.output_dict[w.name]
            # print(w.class_name)
            w.update()

    def update_plot(self):
        for w in self.plot_widgets:
            w.input = self.output_dict[w.name]
            w.update()

    def update_display_widgets(self):
        if self.if_main_fun_run == True:
            if self.update_input():
                self.main_fun(**self.input_dict)
                self.get_output_dict()
                self.update_output()
                self.update_plot()

            if self.cycle_start == False:
                self.if_main_fun_run = False
        else:
            pass
        self.root.after(300,self.update_display_widgets)


    def main(self):
        self.if_main_fun_run = True
        # if self.update_input():
        #     self.main_fun(**self.input_dict)
        #     self.get_output_dict()
        #     self.update_output()
        # else:
        #     self.if_main_fun_run = False







    def creat_main_fun_widgets(self):
        self.main_fun_btn = changable_button(root=self.root,name = self.fun_name,input=self.main)
        # self.update_output()

    def creat_widgets_from_input_dict(self):

        self.input_widgets = []
        for name in self.input_dict:
            # print(name)
            w = None
            def_value = self.input_dict[name]
            if type(def_value) == type(1.0) or type(def_value) == type(0):
                w = changable_slide(root=self.root,name = name,input=def_value)
            elif type(def_value) == type(''):
                w = changable_text(root=self.root,name = name,input=def_value)
            elif type(def_value) == type([]):
                w = changable_listbox(root=self.root,name = name,input=def_value)
            elif type(def_value) == type({}):
                type_judge = True
                for i in def_value:
                    if type(def_value[i]) != type(True):
                        type_judge = False
                if type_judge:
                    w = changable_checkboxes(root=self.root,name = name,input=def_value)
            if w != None:
                self.input_widgets.append(w)

    def seperate_plot_widgets(self):
        self.plot_widgets,self.other_widgets = [],[]
        for w in self.output_widgets:
            if w.class_name == 'plot_display':
                self.plot_widgets.append(w)
            else:
                self.other_widgets.append(w)

    def layout_widgets(self):
        id = 0
        for w in self.input_widgets:
            col,row = id%5,id//5
            # print(col,row)
            w.place(relx=0.2*col, rely=0.25*row, relheight=0.25, relwidth=0.2)
            id+=1
        # print('input_widgets')
        # print(len(self.input_widgets))
        self.seperate_plot_widgets()
        for w in  self.other_widgets:
            col,row = id%5,id//5
            w.place(relx=0.2*col, rely=0.25*row, relheight=0.25, relwidth=0.2)
            id+=1
        # print('id',id)
        for w in self.plot_widgets:
            if (id+3)//5>row:
                row+=1
                col = 0
                id = row*5+1
            else:
                col = 1
                id = (row+1)*5
            w.place(relx=0.5*col, rely=0.25*row, relheight=0.25, relwidth=0.5)
            # print('id',id,'row',row,col)
        self.main_fun_btn.pack(side=tk.BOTTOM)
        # test_l = tk.Button(self.root,command = self.test)
        # test_l.pack(side=tk.BOTTOM)

    # def test(self):
    #     print('test')
    #     self.update_output()
    #     self.plot_widgets[0].axes1.cla()
    #     self.plot_widgets[0].update()
        # self.plot_widgets[0].canvas.draw()

    def creat_widgets_from_output_dict(self):
        w = None
        self.output_widgets = []
        for name in self.output_dict:
            # print('name:',name)
            def_value = self.output_dict[name]
            if type(def_value) == type(0.0) or type(def_value) == type(0):
                w = num_display(root=self.root,name = name,input=def_value)
            elif type(def_value) == type(''):
                w = text_display(root=self.root,name = name,input=def_value)
            elif type(def_value) == type([]):
                if self.if_plotable(def_value):
                    for ar in def_value:
                        if type(ar) == type(np.arange(0, 3)):
                            ar.tolist()

                    w = plot_display(root=self.root,name = name,input=def_value)
                else:
                    w = list_display(root=self.root,name = name,input=def_value)
            if w != None:
                self.output_widgets.append(w)

    # def layout_output_widgets(self):
    #     id = 0


    def if_plotable(self,i_list):
        res0 = len(i_list)>1
        res1 = all(type(item) == type([]) or type(item) == type(np.arange(0, 3)) for item in i_list)
        res2 = all(len(item) == len(i_list[0]) and len(i_list[0])>0 for item in i_list)

        # res3 = ==True for item in i_list)
        # for i in i_list[0]:
        #     print(type(i))
        res3 = all(all(type(n)== type(0.0) or type(n)== type(0) or type(n) == type(np.float64(0.0)) for n in item) for item in i_list)
        # print('res3',res3)
        return res0 and res1 and res2 and res3

    def display(self):
        self.root.mainloop()
    def callback_error(self, *args):
        # Build the error message
        message = 'Generic error:\n\n'
        message += traceback.format_exc()
        self.if_main_fun_run == False
        tkinter.messagebox.showerror('Error', message)


    # def defind_input_widgets_type(self,default_value):
    #     if type(default_value) == type(1.0) or type(default_value) == type(0):






if __name__ == '__main__':
     # a = auto_generate_GUI('test.py','fun1')
     # a.main_fun(30,'f')
     # print(a.output_dict)
     # print(a.input_dict)
     # a = auto_generate_GUI('test.py','fun1')
     # a = auto_generate_GUI(pickle_name = 'just.fgui')
    l = len(sys.argv)
    # print(l)
    arg = sys.argv
    print(arg)
    for i in arg:
        print(i)
    if l == 2:
        if arg[1].find('.fgui')>-1:
            path, filename = os.path.split(arg[1])
            sys.path.append(path)
            # print()
            auto_generate_GUI(pickle_name = arg[1])
        elif arg[1].find('.py')>-1:
            path, filename = os.path.split(arg[1])
            sys.path.append(path)
            auto_generate_GUI(file_name = arg[1])
    elif l == 3:
        if arg[2].find('.py')>-1:
            path, filename = os.path.split(arg[2])
            sys.path.append(path)
            auto_generate_GUI(file_name = arg[1],fun_name = arg[2])
    else:
        auto_generate_GUI()
     # print ('Argument List:', str(sys.argv))
     #
     #

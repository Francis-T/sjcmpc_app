from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from time import time, ctime, localtime

# from kivy.core.image import Image as CoreImage

class ImageButton(Image, Button):
    def on_press(self):
        return

class SJCMPCGuiApp(App):
    def build(self):
        Window.clearcolor = (0.9529, 0.9725, 0.9843, 1)
        main_layout = GridLayout(cols=2)
        # main_layout.add_widget(Label(text='SJCMPC', 
        #                              size_hint_y=None, 
        #                              height=100,
        #                              color=[0,0,0,1],
        #                              font_size='30sp'))
        main_layout.add_widget(Image(source='Logo.png', 
                                     size_hint_y=None, 
                                     height=100))
        main_layout.add_widget(Label(text='Time Attendance', 
                                     size_hint_y=None, 
                                     height=100, 
                                     color=[0,0,0,1],
                                     font_size='50sp'))

        # Set up GUI elements on the left side of the screen
        scan_btn = ImageButton(source='Scan.png',
                               background_color=[1,1,1,1],
                               background_normal='')
        scan_btn.bind(on_press=self.scan_pressed)

        self.left_panel = BoxLayout(orientation='vertical')
        self.left_panel.add_widget(scan_btn)

        main_layout.add_widget(self.left_panel)


        # Set up GUI elements on the right side of the screen
        self.lbl_current_time = Label(text='October 28 2017,\n09:00 AM', 
                                      color=[0,0,0,1],
                                      font_size='40sp',
                                      halign='center') 
        self.right_panel = BoxLayout(orientation='vertical')
        self.right_panel.add_widget(self.lbl_current_time)

        main_layout.add_widget(self.right_panel)

        Clock.schedule_interval(self.update_clock_time, 1)

        return main_layout

    def update_clock_time(self, src):
        ct = localtime()
        # time_str = str(ct.tm_mon) + "/" + str(ct.tm_mday) + "/" + str(ct.tm_year) + "\n"
        # time_str += str(ct.tm_hour) + ":" + str(ct.tm_min) + ":" + str(ct.tm_sec)

        month_str = [ "????", "January", "February", "March", "April", "May", "June", "July", "August",
                      "September", "October", "November", "December" ]

        tod_str = "--"
        if ct.tm_hour == 0:
            tod_str = "MN"
        elif ct.tm_hour < 12:
            tod_str = "AM"
        elif ct.tm_hour == 12:
            tod_str = "NN"
        else:
            tod_str = "PM"
            

        time_str = ( "{} {}, {}\n{:02}:{:02}:{:02} {}".format(month_str[ct.tm_mon], ct.tm_mday, ct.tm_year,
                                                  ct.tm_hour, ct.tm_min, ct.tm_sec, tod_str))
        self.lbl_current_time.text = str(time_str)
        return

    def scan_pressed(self, src):
        self.left_panel.clear_widgets()
        avatar_btn = ImageButton(source='avatar.png',
                                 background_color=[1,1,1,1],
                                 background_normal='')
        avatar_btn.bind(on_press=self.avatar_pressed)
        self.left_panel.add_widget(avatar_btn)

        return

    def avatar_pressed(self, src):
        self.left_panel.clear_widgets()
        scan_btn = ImageButton(source='Scan.png',
                               background_color=[1,1,1,1],
                               background_normal='')
        scan_btn.bind(on_press=self.scan_pressed)
        self.left_panel.add_widget(scan_btn)

        return


SJCMPCGuiApp().run()



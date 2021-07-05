from logging import disable
from kivy.core import text
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
import os
import can

class TouCAN(App):
    def build(self):
        self.window = GridLayout()

        #add widgets to window
        self.window.cols = 3
        self.window.size_hint = (.9, .95)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        canRow = BoxLayout(orientation='vertical')
        
        # image widget
        canRow.add_widget(Image(source="toucan.png"))

        # initialize can button
        canRow.initializebutton=Button(
                            text="Initialize CAN",
                            size_hint = (1,None),
                            bold = True,
                            background_color = '#3437eb'                        
        )
        canRow.initializebutton.bind(on_press=self.OnInitializeButtonClick)
        canRow.add_widget(canRow.initializebutton)


        self.window.add_widget(canRow)
        

        # start engine button
        self.startengine = Button(
                            text="Start Engine",
                            size_hint = (1,None),
                            bold = True,
                            background_color = '#33ff00'
        )
        self.startengine.bind(on_press=self.OnStartButtonClick)
        self.window.add_widget(self.startengine)

        #shutdown engine button
        self.shutdownengne = Button(
                            text="Shutdown Engine",
                            size_hint = (1,None),
                            bold = True,
                            background_color='#ff0000',
                            disabled = True
        )
        self.shutdownengne.bind(on_press=self.OnShutdownButtonClick)
        self.window.add_widget(self.shutdownengne)

        # gas pedal position slider
        self.gaspedalslider = Slider(
                            min=0,
                            max = 100, 
                            value = 0,
                            orientation = 'vertical',
                            disabled = True
        )
        self.gaspedalslider.bind(value=self.OnGasPedalSliderValueChange)
        self.window.add_widget(self.gaspedalslider)

        # speed slider
        self.speedslider = Slider(
                            min=0,
                            max = 512,
                            value=0,
                            orientation = 'vertical',
                            disabled = True
        )
        self.speedslider.bind(value=self.OnSpeedSliderValueChange)
        self.window.add_widget(self.speedslider)

        # braking pedal button
        self.brakepedalbutton = Button(
                            text="BRAKE!",
                            size_hint = (1,None),
                            bold = True,
                            background_color='#ffd000',
                            disabled = True
        )
        self.brakepedalbutton.bind(on_press=self.OnBrakingPedalButtonClick)
        self.brakepedalbutton.bind(on_release=self.OnBrakingPedalButtonRelease)
        self.window.add_widget(self.brakepedalbutton)
        
        # gas pedal position label
        self.gaslabel = Label (
                        text = 'Gas pedal position: ' + str(int(self.gaspedalslider.value)),
                        font_size=20,
                        color = '#b4eb34'

                        )
        self.window.add_widget(self.gaslabel)

        # vehicle speed label
        self.speedlabel = Label (
                        text = 'Vehicle speed: ' + str(int(self.speedslider.value)),
                        font_size=20,
                        color = '#00aaff'
                        )
        self.window.add_widget(self.speedlabel)

        # braking level label
        self.brakelabel = Label (
                        text = 'Braking status: '+ str(self.brakepedalbutton.state),
                        font_size=20,
                        color = '#e600ff'
                        )
        self.window.add_widget (self.brakelabel)
        
        return self.window


    def OnGasPedalSliderValueChange(self,instance, value):
        self.gaslabel.text = 'Gas pedal position: ' + str(int(self.gaspedalslider.value))
    
    def OnSpeedSliderValueChange(self,instance, value):
        self.speedlabel.text = 'Vehicle speed: ' + str(int(self.speedslider.value))
    

    def OnBrakingPedalButtonClick(self, instance):
        self.brakelabel.text = 'Braking status: ' + str(self.brakepedalbutton.state)

    def OnBrakingPedalButtonRelease(self, instance):
        self.brakelabel.text = 'Braking status: ' + str(self.brakepedalbutton.state)



    def OnStartButtonClick(self, instance):
        self.shutdownengne.disabled=False
        self.speedslider.disabled=False
        self.brakepedalbutton.disabled=False
        self.gaspedalslider.disabled=False
        self.startengine.disabled=True

        # TO-DO: start the thread that will send the can msg flow

    def OnInitializeButtonClick(self, instance):
        os.system('sudo ip link set can0 type can bitrate 1000000')
        os.system('sudo ifconfig can0 up')
        can0=can.interface.Bus(channel='can0', bustype='socketcan')
        if(can0):
            instance.text = "CAN interface running"
            
    

    def OnShutdownButtonClick(self, instance):
        self.shutdownengne.disabled=True
        self.speedslider.disabled=True
        self.speedslider.value=0
        self.brakepedalbutton.disabled=True
        self.gaspedalslider.disabled=True
        self.gaspedalslider.value=0
        self.startengine.disabled=False
        
        # TO-DO: kill the thread 



if __name__ == "__main__":
    TouCAN().run()
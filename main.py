from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.taptargetview import MDTapTargetView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDSeparator, MDCardSwipe
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.pickers import MDTimePicker, MDDatePicker
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList, OneLineListItem, OneLineAvatarIconListItem
from kivymd.utils import asynckivy
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivymd.uix.snackbar import Snackbar
from datetime import datetime, date, time, timedelta

import math, smtplib, ssl, email, json, os
from os import path
from pathlib import Path

from matplotlib.mathtext import math_to_image

import logging

# Set Matplotlib's logger to only print warnings or more severe messages
logging.getLogger('matplotlib').setLevel(logging.WARNING)


KV = '''    
<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)


<ContentNavigationDrawer>:
    orientation: 'vertical'
    padding: "8dp"
    spacing: "8dp"

    ScrollView:

        MDList:
            OneLineListItem:
                text: 'Post Mortem Interval'
                on_press:
                    root.nav_drawer.set_state('close')
                    root.screen_manager.current = 'Post Mortem Interval'
            
            OneLineListItem:
                text: 'Andere Apps'
                on_press:
                    root.nav_drawer.set_state('close')
                    root.screen_manager.current = 'Andere Apps'


<Content>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "200dp"

    MDTextField:
        id: casenr
        hint_text: "Zaaknummer"

    
<SwipeToDeleteItem>:
    size_hint_y: None
    height: content.height

    MDCardSwipeLayerBox:
        padding: "8dp"

        MDIconButton:
            icon: "trash-can"
            pos_hint: {"center_y": .5}
            on_release: app.remove_item(root)
    
    MDCardSwipeFrontBox:
        OneLineListItem:
            id: content
            text: root.text
            _no_ripple_effect: True
            on_release: app.get_report(root)

<CasesList>: 
    IconRightWidget: 
        icon: "trash-can"
        on_release: app.remove_item(root)


Screen:
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            id: toolbar
            pos_hint: {'top': 1}
            elevation: 10
            title: screen_manager.current
            left_action_items: [['menu', lambda x: nav_drawer.set_state('open')]]
    
        MDNavigationLayout:
            x: toolbar.height

            ScreenManager:
                id: screen_manager

                Screen:
                    name: 'Post Mortem Interval'
                    spacing: dp(10)

                    MDBottomNavigation:     
                        id: panel

                        MDBottomNavigationItem:
                            name: 'pmi'
                            text: 'pmi'
                            icon: 'skull-crossbones-outline'

                            MDTabs:
                                id: tabs

                                Tab:
                                    text: 'Bereken PMI'
                                    
                                    ScrollView:
                                        size: self.size

                                        GridLayout:
                                            size_hint_y: None
                                            padding: dp(10)
                                            spacing: dp(10)
                                            cols: 1
                                            height: self.minimum_height                                        

                                            MDTextField:
                                                id: bodyTemp
                                                hint_text: "Lichaamstemperatuur"
                                                helper_text: "Rectale temperatuur in graden Celcius"
                                                helper_text_mode: 'persistent'

                                            MDTextField:
                                                id: surTemp
                                                hint_text: "Omgevingstemperatuur"
                                                helper_text: "Geschatte gemiddelde omgevingstemperatuur"
                                                helper_text_mode: 'persistent'

                                            MDTextField:   
                                                id: bodyWeight
                                                hint_text: "Lichaamsgewicht"
                                                helper_text: "Geschatte gemiddelde lichaamsgewicht"
                                                helper_text_mode: 'persistent'

                                            Widget:
                                                size_hint_y: None
                                                height: dp(5)

                                            MDDropDownItem:
                                                id: drop_item_cover
                                                pos_hint: {'center_x': .5}
                                                text: 'Lichaamsbedekking'
                                                on_press: app.menu_cover.open()

                                            MDDropDownItem:
                                                id: drop_item_surFact
                                                pos_hint: {'center_x': .5, 'center_y': .47}
                                                text: 'Omgevingsfactoren'
                                                on_press: app.menu_surFact.open()

                                            Widget:
                                                size_hint_y: None
                                                height: dp(10)

                                            MDLabel:
                                                text: "Datum en tijd van berekenen"
                                            
                                            MDSeparator:

                                            MDRaisedButton:
                                                id: date_button
                                                text: "Datum"
                                                pos_hint: {'center_x': 1, 'center_y': .35}
                                                on_press: app.show_date_picker()

                                            MDRaisedButton:
                                                id: time_button
                                                text: "Tijd"
                                                pos_hint: {'center_x': .5, 'center_y': .35}
                                                on_press: app.show_time_picker()

                                            MDSeparator:

                                            MDRaisedButton:
                                                id: button
                                                text: "Schat PMI"
                                                pos_hint: {"center_x": 0.5, "center_y": .25}
                                                on_press: app.show_alert_dialog()
                                            
                                            MDFlatButton:
                                                id: back
                                                on_release: app.dismiss_alert_dialog_pmi()

                                            MDFlatButton:
                                                id: save
                                                on_press: app.save_pmi_dialog()                                

                                Tab:
                                    text: "info"

                                    ScrollView:
                                        size: self.size

                                        GridLayout:
                                            adaptive_height: True
                                            padding: dp(10)
                                            spacing: dp(10)
                                            cols: 1                                            

                                            MDLabel:
                                                text: "Gebruikte formule voor een omgevingstemperatuur van onder de 23 graden:"

                                            Image:
                                                source: '23below.png'
                                                size: self.texture_size

                                            MDLabel:
                                                text: "Gebruikte formule voor een omgevingstemperatuur van boven de 23 graden:"

                                            Image:
                                                source: "23up.png"

                                            Image:
                                                source: "B.png"

                        MDBottomNavigationItem:
                            name: 'saved_pmi'
                            text: 'saved pmi'
                            icon: 'floppy'

                            MDScrollViewRefreshLayout:
                                id: refresh_layout
                                refresh_callback: app.refresh_callback
                                root_layout: root

                                MDList:
                                    id: container


                Screen:
                    name: 'Andere Apps'

                    MDLabel:
                        text: 'Andere Apps'
                        halign: 'center'

                Screen:
                    name: 'PMI Report'

                    BoxLayout:
                        id: report
                        orientation: 'vertical'
                        padding: '20dp'
                    

            MDNavigationDrawer:
                id: nav_drawer

                ContentNavigationDrawer:
                    id: content_drawer 
                    screen_manager: screen_manager
                    nav_drawer: nav_drawer
                
        '''


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class Tab(FloatLayout, MDTabsBase):
    pass


class Content(BoxLayout):
    pass


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()

class CasesList(OneLineAvatarIconListItem):
    text = StringProperty()


class PMIApp(MDApp):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.snackbar = None

        json_path = os.path.join(os.pardir, "pmi.json")
        self.store = JsonStore(json_path)
        
        self.screen = Builder.load_string(KV)

        menu_items_cover = [
            {"text": "Naakt", "viewclass": "OneLineListItem", "on_release": lambda x="Naakt": self.set_item_cover(x)}, 
            {"text": "Een of twee dunne lagen", "viewclass": "OneLineListItem", "on_release": lambda x="Een of twee dunne lagen": self.set_item_cover(x)},
            {"text": "Een of twee dikke lagen", "viewclass": "OneLineListItem", "on_release": lambda x="Een of twee dikke lagen": self.set_item_cover(x)},
            {"text": "Twee of drie lagen", "viewclass": "OneLineListItem", "on_release": lambda x="Twee of drie lagen": self.set_item_cover(x)},
            {"text": "Drie of vier lagen", "viewclass": "OneLineListItem", "on_release": lambda x="Drie of vier lagen": self.set_item_cover(x)},
            {"text": "Meer lagen", "viewclass": "OneLineListItem", "on_release": lambda x="Meer lagen": self.set_item_cover(x)},
            {"text": "Licht beddengoed", "viewclass": "OneLineListItem", "on_release": lambda x="Licht beddengoed": self.set_item_cover(x)},
            {"text": "Zwaar beddengoed", "viewclass": "OneLineListItem", "on_release": lambda x="Zwaar beddengoed": self.set_item_cover(x)},
        ]


        self.menu_cover = MDDropdownMenu(
            caller=self.screen.ids.drop_item_cover, 
            items=menu_items_cover, 
            position="auto", 
            width_mult=6
        )

        menu_items_surFact = [
            {"text": "Droog lichaam, binnen", "viewclass": "OneLineListItem", "on_release": lambda x="Droog lichaam, binnen": self.set_item_surFact(x)},
            {"text": "Droog lichaam, buiten", "viewclass": "OneLineListItem", "on_release": lambda x="Droog lichaam, buiten": self.set_item_surFact(x)},
            {"text": "Nat lichaam, binnen", "viewclass": "OneLineListItem", "on_release": lambda x="Nat lichaam, binnen": self.set_item_surFact(x)},
            {"text": "Nat lichaam, buiten", "viewclass": "OneLineListItem", "on_release": lambda x="Nat lichaam, buiten": self.set_item_surFact(x)},
            {"text": "Stilstaand water", "viewclass": "OneLineListItem", "on_release": lambda x="Stilstaand water": self.set_item_surFact(x)},
            {"text": "Stromend water", "viewclass": "OneLineListItem", "on_release": lambda x="Stromend water": self.set_item_surFact(x)},
        ]


        self.menu_surFact = MDDropdownMenu(
            caller=self.screen.ids.drop_item_surFact, 
            items=menu_items_surFact, 
            position="auto", 
            width_mult=4
        )


    def set_item_cover(self, text):
        self.menu_cover.dismiss()
        cover_button = self.root.ids.drop_item_cover
        cover_button.text = text

        self.cover_nl = text
        self.callback_cover(self.cover_nl)


    def set_item_surFact(self, text):
        self.menu_surFact.dismiss()  # Close the dropdown menu
        surFact_button = self.root.ids.drop_item_surFact
        surFact_button.text = text  # Update the button text

        self.surFact_nl = text  # Update any related variable or do further processing
        self.callback_surFact(self.surFact_nl)  # Perform any additional callbacks or actions

    
    def remove_item(self, instance):
        if self.store.exists(instance.text):
            self.store.delete(instance.text)
            self.screen.ids.container.remove_widget(instance)
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)), instance.text + '_formula.png'))
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)), instance.text + 'B.png'))
        else:
            pass


    def on_start(self):
        self.set_list()

        try:
            if path.exists('pmi.json') == True:
                move_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pmi.json')
                p = Path(move_path).absolute()
                parent_dir = p.parents[1]
                p.rename(parent_dir / p.name)
            else:
                pass
        except FileExistsError as e:
            print(e)
            pass

    def set_list(self):
        async def set_list():
            for casenr in self.store:
                await asynckivy.sleep(0)
                self.screen.ids.container.add_widget(
                    CasesList(text=casenr, on_release=self.get_report)
                )
        asynckivy.start(set_list())
        

    def refresh_callback(self, *args):
        def refresh_callback(interval):
            self.screen.ids.container.clear_widgets()
            self.set_list()
            self.screen.ids.refresh_layout.refresh_done()
            self.tick = 0
        
        Clock.schedule_once(refresh_callback, 1)


    def get_report(self, inst):
        self.root.ids.report.clear_widgets()
        self.root.ids.screen_manager.current = 'PMI Report'
        
        self.casenr = inst.text
        data = self.store.get(self.casenr)

        self.root.ids.report.add_widget(
            MDLabel(text="Zaaknummer:   " + str(self.casenr))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Lichaamstemperatuur:    ' + str(data['Lichaamstemperatuur']) + chr(176))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )
        self.root.ids.report.add_widget(
            MDLabel(text='Omgevingstemperatuur:    ' + str(data['Omgevingstemperatuur'])+ chr(176))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Lichaamsgewicht:    ' + str(data['Lichaamsgewicht']) + 'kg')
        )
        
        self.root.ids.report.add_widget(
            MDSeparator()
        )
        
        self.root.ids.report.add_widget(
            MDLabel(text='Lichaamsbedekking:    ' + str(data['Lichaamsbedekking']))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Omgevingsfactoren:    ' + str(data['Omgevingsfactoren']))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Datum en tijd van berekenen:    ' + str(data['datumtijd_berekenen']))
        )
        
        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Correctiefactor:    ' + str(data['f_waarde']))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Post Mortem Interval:    ' + str(data['pmi']))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Minimale PMI:    ' + str(data['min_pmi']))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Maximale PMI:    ' + str(data['max_pmi']))
        )  

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Gebruikte berekening:')
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            Image(source=data['formule'])
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Gebruikte berekening voor B:')
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            Image(source=data['formuleB'])
        )
        
        # self.root.ids.report.add_widget(
        #     MDRaisedButton(text='Copy to Clipboard', on_release=lambda *args: self.dialog_email(casenr, *args)) 
        # )

        self.root.ids.report.add_widget(
            MDRaisedButton(text='Kopiëer Rapport', on_release=self.copy_report) 
        )

    def callback_cover(self, cover):
        if self.cover_nl == "Naakt":
            self.cover = "Naked"
            return self.cover
        if self.cover_nl == "Een of twee dunne lagen":
            self.cover = "OneToTwoThin"
            return self.cover
        if self.cover_nl == "Een of twee dikke lagen":
            self.cover = "OneToTwoThicker"
            return self.cover
        if self.cover_nl == "Twee of drie lagen":
            self.cover = "TwoToThree"
            return self.cover
        if self.cover_nl == "Drie of vier lagen":
            self.cover = "ThreeToFour"
            return self.cover
        if self.cover_nl == "Meer lagen":
            self.cover = "MoreLayers"
            return self.cover
        if self.cover_nl == "Licht beddengoed":
            self.cover = "BedspreadLight"
            return self.cover
        if self.cover_nl == "Zwaar beddengoed":
            self.cover = "BedspreadFully"
            return self.cover    

    def callback_surFact(self, surFact):
        if self.surFact_nl == "Droog lichaam, binnen":
            self.surFact = "StillAirBodyDry"
            return self.surFact
        if self.surFact_nl == "Droog lichaam, buiten":
            self.surFact = "MovingAirBodyDry"
            return self.surFact
        if self.surFact_nl == "Nat lichaam, binnen":
            self.surFact = "StillAirBodySoaked"
            return self.surFact
        if self.surFact_nl == "Nat lichaam, buiten":
            self.surFact = "MovingAirBodySoaked"
            return self.surFact
        if self.surFact_nl == "Stilstaand water":
            self.surFact = "StillWater"
            return self.surFact
        if self.surFact_nl == "Stromend water":
            self.surFact = "FlowingWater"
            return self.surFact


    def calc_pmi(self):
        try: 
            self.t_rectum_c = self.screen.ids.bodyTemp.text.replace(',', '.')
            self.t_rectum_c = float(self.t_rectum_c)

            self.t_ambient_c = self.screen.ids.surTemp.text.replace(',', '.')
            self.t_ambient_c = float(self.t_ambient_c)

            self.body_wt_kg = self.screen.ids.bodyWeight.text.replace(',', '.')
            self.body_wt_kg = float(self.body_wt_kg)
        
        except ValueError:
            self.pmi = "Error: "
            self.longest_shortest_text = "Vul een geldige waarde in."
            return self.pmi, self.longest_shortest_text

        if self.t_ambient_c > self.t_rectum_c:
            self.pmi = "Error: "
            self.longest_shortest_text = "De lichaamstemperatuur is lager dan de omgevingstemperatuur"
            print(self.pmi, self.longest_shortest_text)
            return self.pmi, self.longest_shortest_text

        if int(self.body_wt_kg) < 11:
            self.pmi = "Let op: "
            self.longest_shortest_text = "Er is een hoge mate van onzekerheid."
            return self.pmi, self.longest_shortest_text

        # Retrieve the corrective Factor
        try:
            self.corrective_factor = self.get_corrective_factor(self.cover, self.surFact)
        except AttributeError:
            self.pmi = "Let op: "
            self.longest_shortest_text = "Vul de Lichaamsbedekking en/of Omgevingsfactoren in."
            return self.pmi, self.longest_shortest_text
        
        print(self.corrective_factor)

        # Get the left side and the 'B' from the Henssge formula
        left_side = (self.t_rectum_c - self.t_ambient_c) / (37.200000000000003 - self.t_ambient_c)
        bigB = (-1.2815000000000001 * math.pow(self.corrective_factor * self.body_wt_kg, -0.625) + 0.028400000000000002)
        
        best_time = 0.0
        proposed_time = 0.0

        # Propose a ToD (6 min interval), calculate 1000 times with the Henssge formula if the result of that time is the closest 
        # to the result with best time (i.e. just perform the Henssge calculation)
        while proposed_time < 100: 
            proposed_time = proposed_time + 0.1
            if math.fabs(left_side - self.get_right_side(self.t_ambient_c, bigB, proposed_time)) < math.fabs(left_side - self.get_right_side(self.t_ambient_c, bigB, best_time)):
                best_time = proposed_time
        
        self.best_time = (math.ceil(best_time * 10) / 10)

        # Format the time so that it is readable; no messing with the results here
        h = str(self.best_time).split('.')[0]

        m = str(self.best_time).split('.')[-1]
        m = (int(m) * 60) / 10
        m = str(m).replace('.0', '')

        try:
            alt_date = str(self.date).split("-")
        except AttributeError:
            self.pmi = "Let op: "
            self.longest_shortest_text = "Vul de datum van berekenen in."
            return self.pmi, self.longest_shortest_text

        try:
            alt_time = str(self.time).split(":")
        except AttributeError:
            self.pmi = "Let op: "
            self.longest_shortest_text = "Vul de tijd van berekenen in."
            return self.pmi, self.longest_shortest_text

        self.selected_datetime = datetime.combine(date(int(alt_date[0]), int(alt_date[1]), int(alt_date[2])), 
                                            time(int(alt_time[0]), int(alt_time[1])))

        d = self.selected_datetime - timedelta(hours=int(h), minutes=int(m))
        self.pmi = datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")
        print(self.pmi)
        
        self.pmi_text = "Geschatte tijd sinds overlijden is "+ str(h) + "h " + str(m) + "min ("+str(self.best_time) + " uur). Dat was op " + str(d)

        print(self.pmi_text)        

        # Get the uncertainty, longest time and shortest time and format it into readable text 
        uncertainty, longest_time, shortest_time = self.get_longest_shortest_time(self.t_ambient_c, self.body_wt_kg, best_time, self.cover, self.surFact)

        if uncertainty == 69:
            self.pmi = "Let op: "
            self.longest_shortest_text = "Er is een hoge mate van onzekerheid."
            return self.pmi, self.longest_shortest_text
        else:
            if shortest_time == 0.0:
                h = str(longest_time).split('.')[0]

                m = str(longest_time).split('.')[-1]
                m = (int(m) * 60) / 10
                m = str(m).replace('.0', '')

                self.min_pmi = self.selected_datetime - timedelta(hours=int(h), minutes=int(m))
                self.min_pmi = datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")

                self.longest_shortest_text = ". Het is voor 95% zeker dat de dood in de afgelopen " + str(h) + "h " + str(m) + "min ("+ str(longest_time) + " uur) is ingetreden. Dat was op " + str(d) + "."
            
            else:
                h = str(shortest_time).split('.')[0]

                m = str(shortest_time).split('.')[-1]
                m = (int(m) * 60) / 10
                m = str(m).replace('.0', '')
                
                h1 = str(longest_time).split('.')[0]

                m1 = str(longest_time).split('.')[-1]
                m1 = (int(m1) * 60) / 10
                m1 = str(m1).replace('.0', '')

                d = self.selected_datetime - timedelta(hours=int(h), minutes=int(m))
                self.min_pmi = datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")
                d1 = self.selected_datetime - timedelta(hours=int(h1), minutes=int(m1))
                self.max_pmi = datetime.strptime(str(d1), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")

                self.longest_shortest_text = ". Het is voor 95% zeker dat de dood tussen " + str(h) + "h " + str(m) + "min ("+ str(shortest_time)+" uur) en " + str(h1) + "h " + str(m1) + "min ("+ str(longest_time)+" uur) geleden is ingetreden. Dat is tussen " + str(d1) + " en " + str(d)

                print(self.longest_shortest_text)

            return self.pmi_text, self.longest_shortest_text


    # Calculate the right side of the Henssge formula
    def get_right_side(self, t_ambient_c, bigB, f):
        if self.t_ambient_c <= 23:
            return (1.25 * math.exp(bigB * f) - 0.25 * math.exp(5 * bigB * f))
        else:
            return (1.1100000000000001 * math.exp(bigB * f) - 0.11 * math.exp(10 * bigB * f))


    def get_longest_shortest_time(self, t_ambient_c, body_wt_kg, best_time, cover, surFact):
        uncertainty = self.get_uncertainty(self.t_ambient_c, self.body_wt_kg, best_time, cover, surFact)

        if uncertainty == 69:
            uncertainty == 69
            longest_time = 0
            shortest_time = 0
            return uncertainty, longest_time, shortest_time
        
        else:
            shortest_time = best_time - uncertainty
            longest_time = best_time + uncertainty
            shortest_time = math.ceil(shortest_time * 10) / 10
            if shortest_time <= 0.0:
                shortest_time = 0.0
            longest_time = math.ceil(longest_time * 10) / 10

            return uncertainty, longest_time, shortest_time

    
    def get_uncertainty(self, t_ambient_c, body_wt_kg, best_time, cover, surFact):
        uncertainty = 2.8
        if self.t_ambient_c > 23:
            if self.body_wt_kg <= 10:
                if best_time >= 3: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 15:
                if best_time >= 4: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 20: 
                if best_time >= 5: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 30:
                if best_time >= 6: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 40:
                if best_time >= 8: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 50:
                if best_time >= 9: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 60: 
                if best_time >= 11: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 70: 
                if best_time >= 13: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 80:
                if best_time >= 14: 
                    uncertainty = 69
                return uncertainty

            if self.body_wt_kg <= 90:
                if best_time >= 16: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 100:
                if best_time >= 18: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 110:
                if best_time >= 20: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 120:
                if best_time >= 20: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 140: 
                if best_time >= 20: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 160: 
                if best_time >= 20: 
                    uncertainty = 69
                return uncertainty
            
            if self.body_wt_kg <= 180:
                if best_time >= 20: 
                    uncertainty = 69
                return uncertainty
            
            if best_time >= 20: 
                uncertainty = 69
            return uncertainty
        
        if self.body_wt_kg <= 10: 
            if best_time >= 7: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 5: 
                uncertainty = self.Category4570(self, cover, surFact)
                return uncertainty
            
            if best_time >= 3.2000000000000002:
                uncertainty = self.Category3245(cover, surFact)
                return uncertainty
            
            else:
                uncertainty = 2.8
                return uncertainty
            
        if self.body_wt_kg <= 15: 
            if best_time >= 9: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 7:
                uncertainty = self.Category4570(cover, surFact)
                return uncertainty
            
            if best_time >= 4.2000000000000002:
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
            
        if self.body_wt_kg <= 20:
            if best_time >= 11: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 8.5:
                uncertainty = self.Category4570(cover, surFact)
                return uncertainty
            
            if best_time >= 5.5:
                uncertainty = self.Category3245(cover, surFact)
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
        
        if self.body_wt_kg <= 30:
            if best_time >= 15: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 11.5:
                uncertainty = self.Category4570(cover, surFact)
                return uncertainty
            
            if best_time >= 7.2000000000000002:
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
            
        if self.body_wt_kg <= 40: 
            if best_time >= 18: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 14: 
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 9: 
                uncertainty = self.Category3245(cover, surFact)
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
            
        if self.body_wt_kg <= 50:
            if best_time >= 22: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 17: 
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 11:
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
        
        if self.body_wt_kg <= 60: 
            if best_time >= 26: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 20: 
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 13: 
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
            
        if self.body_wt_kg <= 70: 
            if best_time >= 30: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 23: 
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 15: 
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
            
        if self.body_wt_kg <= 80: 
            if best_time >= 34: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 26: 
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 17: 
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
            
        if self.body_wt_kg <= 90: 
            if best_time >= 37: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 27: 
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 19: 
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else: 
                uncertainty = 2.8
                return uncertainty
        
        if self.body_wt_kg <= 100: 
            if best_time >= 42: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 33: 
                uncertainty = self.Category4570  
                return uncertainty
            
            if best_time >= 21: 
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
        
        if self.body_wt_kg <= 110: 
            if best_time >= 46: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 36:
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 23:
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
            
        if self.body_wt_kg <= 120: 
            if best_time >= 50: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 40:
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 25:
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
            
        if self.body_wt_kg <= 140: 
            if best_time >= 60:
                uncertainty = 69
                return uncertainty
            
            if best_time >= 47: 
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 30: 
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
        
        if self.body_wt_kg <= 160: 
            if best_time >= 72: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 56:
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 36: 
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
        
        if self.body_wt_kg <= 180: 
            if best_time >= 82: 
                uncertainty = 69
                return uncertainty
            
            if best_time >= 67: 
                uncertainty = self.Category4570(cover, surFact)  
                return uncertainty
            
            if best_time >= 42:
                uncertainty = self.Category3245(cover, surFact)  
                return uncertainty
            else:
                uncertainty = 2.8
                return uncertainty
            
        if best_time >= 90: 
            uncertainty = 69
            return uncertainty
        
        if best_time >= 78: 
            uncertainty = self.Category4570(cover, surFact)  
            return uncertainty
        
        if best_time >= 50:
            uncertainty = self.Category3245(cover, surFact)  
            return uncertainty
        else:
            uncertainty = 2.8
            return uncertainty 
        

    def Category4570(self, cover, surFact):
        if cover != 'Naked' and surFact == 'StillAirBodyDry':
            uncertainty = 7
        else:
            uncertainty = 4.5
        return uncertainty
        # return uncertainty !  Naked  &  StillAirBodyDry   ? 7 : 4.5
    

    def Category3245(self, cover, surFact):  
        if cover != 'Naked' and surFact == 'StillAirBodyDry':
            uncertainty = 4.5
        else:
            uncertainty = 3.2
        return uncertainty
        # return uncertainty !  Naked  &  StillAirBodyDry   ? 4.5 : 3.2

    
    def get_corrective_factor(self, cover, surFact):
        if surFact == 'StillAirBodyDry':
            if cover == 'Naked':
                return 1.0
            if cover == 'OneToTwoThin':
                return 1.1
            if cover == 'OneToTwoThicker':
                return 1.2
            if cover == 'TwoToThree':
                return 1.2
            if cover == 'ThreeToFour':
                return 1.3
            if cover == 'MoreLayers':
                return 1.4
            if cover == 'BedspreadLight':
                return 1.8
            if cover == 'BedspreadFully':
                return 2.4
        
        if surFact == 'MovingAirBodyDry':
            if cover == 'Naked':
                return 0.75
            if cover == 'OneToTwoThin':
                return 0.9
            if cover == 'OneToTwoThicker':
                return 0.9
            if cover == 'TwoToThree':
                return 1.2
            if cover == 'ThreeToFour':
                return 1.3
            if cover == 'MoreLayers':
                return 1.4
            if cover == 'BedspreadLight':
                return 1.8
            if cover == 'BedspreadFully':
                return 2.4
        
        if surFact == 'StillAirBodySoaked':
            if cover == 'Naked':
                return 0.5
            if cover == 'OneToTwoThin':
                return 0.8
            if cover == 'OneToTwoThicker':
                return 1.1
            if cover == 'TwoToThree':
                return 1.2
            if cover == 'ThreeToFour':
                return 1.2
            if cover == 'MoreLayers':
                return 1.2
            if cover == 'BedspreadLight':
                return 1.2
            if cover == 'BedspreadFully':
                return 1.2

        if surFact == 'MovingAirBodySoaked':
            if cover == 'Naked':
                return 0.7
            if cover == 'OneToTwoThin':
                return 0.7
            if cover == 'OneToTwoThicker':
                return 0.9
            if cover == 'TwoToThree':
                return 0.9
            if cover == 'ThreeToFour':
                return 0.9
            if cover == 'MoreLayers':
                return 0.9
            if cover == 'BedspreadLight':
                return 0.9
            if cover == 'BedspreadFully':
                return 0.9

        if surFact == 'StillWater':
            if cover == 'Naked':
                return 0.5
            if cover == 'OneToTwoThin':
                return 0.7
            if cover == 'OneToTwoThicker':
                return 0.8
            if cover == 'TwoToThree':
                return 0.9
            if cover == 'ThreeToFour':
                return 1.0
            if cover == 'MoreLayers':
                return 1.0
            if cover == 'BedspreadLight':
                return 1.0
            if cover == 'BedspreadFully':
                return 1.0

        if surFact == 'FlowingWater':
            if cover == 'Naked':
                return 0.35
            if cover == 'OneToTwoThin':
                return 0.5
            if cover == 'OneToTwoThicker':
                return 0.7
            if cover == 'TwoToThree':
                return 0.8
            if cover == 'ThreeToFour':
                return 0.9
            if cover == 'MoreLayers':
                return 1.0
            if cover == 'BedspreadLight':
                return 1.0
            if cover == 'BedspreadFully':
                return 1.0
        
        return 1.0


    def show_alert_dialog(self):
        pmi, longest_shortest_text = self.calc_pmi()
        
        if pmi == "Let op: ":
            self.dialog_pmi = MDDialog(text=pmi + longest_shortest_text, buttons=[
                MDFlatButton(text="BACK", text_color=self.theme_cls.primary_color, on_release=self.dismiss_alert_dialog_pmi),
            ])

        else:
            self.dialog_pmi = MDDialog(text=pmi + longest_shortest_text, buttons=[
                MDFlatButton(text="BACK", text_color=self.theme_cls.primary_color, on_release=self.dismiss_alert_dialog_pmi), 
                MDFlatButton(text="SAVE", text_color=self.theme_cls.primary_color, on_release=self.save_pmi_dialog),
                ],
            )
        
        self.dialog_pmi.open()


    def save_pmi_dialog(self, inst):
        self.dialog_save = MDDialog(title="PMI Opslaan", type="custom", content_cls=Content(), buttons=[
            MDFlatButton(text="BACK", text_color=self.theme_cls.primary_color, on_release=self.dismiss_alert_dialog_save),
            MDFlatButton(text="SAVE", text_color=self.theme_cls.primary_color, on_press=self.save, on_release=self.dismiss_alert_dialog_save),
            ],
        )

        self.dialog_save.open()

    
    def show_bodytemp_dialog(self):
        self.bodytemp_dialog = MDDialog(text="Testing", buttons=[
            MDFlatButton(text="BACK", text_color=self.theme_cls.primary_color, on_release=self.dismiss_bodytemp_dialog)
        ])
        
        self.bodytemp_dialog.open()

    def save(self, inst):
        casenr = self.dialog_save.content_cls.ids.casenr.text
        datetime_calc = self.selected_datetime
        f_value = self.corrective_factor
        best_time = self.best_time
        pmi_save = self.pmi
        min_pmi = self.min_pmi
        max_pmi = self.max_pmi
        bodyTemp = self.t_rectum_c
        surTemp = self.t_ambient_c
        bodyWeight = self.body_wt_kg
        cover = self.cover_nl
        surFact = self.surFact_nl

        formulaB = rf'$B = 1.2815 \times ({f_value} \times {bodyWeight})^{{-0.625}})+0.0284$'
        math_to_image(formulaB, casenr + "B.png", dpi=500, format='png')


        if surTemp < 23:    
            formula = rf'$\frac{{{bodyTemp} - {surTemp}}}{{37.2 - {surTemp}}} = 1.25e^{{B \times {best_time}}} - 0.25e^{{5 \times B \times {best_time}}}$'
        
        else:
            formula = rf'$\frac{{{bodyTemp} - {surTemp}}}{{37.2 - {surTemp}}} = 1.11e^{{B*{best_time}}} - 0.11e^{{10*B*{best_time}}}$'
        
        math_to_image(formula, casenr + "_formula.png", dpi=500, format='png')
        
        self.store.put(casenr, Zaaknummer=casenr, datumtijd_berekenen=str(datetime_calc), f_waarde=f_value, pmi=pmi_save, 
                        min_pmi=min_pmi, max_pmi=max_pmi, Lichaamstemperatuur=bodyTemp, Omgevingstemperatuur=surTemp, 
                        Lichaamsgewicht=bodyWeight, Lichaamsbedekking=cover, Omgevingsfactoren=surFact, 
                        formule=casenr + '_formula.png', formuleB=casenr + 'B.png')

    def dismiss_alert_dialog_pmi(self, inst):
        self.dialog_pmi.dismiss()


    def dismiss_alert_dialog_save(self, inst):
        self.dialog_save.dismiss()

    
    def dismiss_bodytemp_dialog(self, inst):
        self.bodytemp_dialog.dismiss()

    
    def show_time_picker(self):
        current_time = datetime.now().time()

        time_dialog = MDTimePicker()
        time_dialog.set_time(current_time)
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    
    def get_time(self, instance, time):
        self.time = time
        time_button = self.root.ids.time_button
        time_button.text = str(self.time)

        print(self.time)
        return self.time


    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.get_date(value)
        print(value)
    
    def on_cancel(self, instance, value):
        print("Cancelled")


    def get_date(self, *args):
        date_button = self.root.ids.date_button
        date_button.text = str(args[0])
        self.date = args[0]
        print(self.date)
        return self.date


    def copy_report(self, inst):
        data = self.store.get(self.casenr)
        Clipboard.copy(str(data))

    def switch_tab(self, instance):
        self.screen.ids.panel.switch_tab('saved_pmi')


    def change_theme(self, checkbox, value):
        if value:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "BlueGray"
        else:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Blue"

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = "Blue"

        return self.screen


if __name__ == "__main__":
    PMIApp().run()

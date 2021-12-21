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
from kivymd.uix.picker import MDTimePicker, MDDatePicker
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
from datetime import datetime, date, time, timedelta

import math, os, smtplib, ssl, email, json

# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

from matplotlib.mathtext import math_to_image
# from fpdf import FPDF


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


# <ContentEmail>:
#     orientation: "vertical"
#     spacing: "12dp"
#     size_hint_y: None
#     height: "200dp"

#     MDTextField:
#         id: email
#         hint_text: "Email"


    
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

        MDToolbar:
            id: toolbar
            pos_hint: {'top': 1}
            elevation: 10
            title: screen_manager.current
            left_action_items: [['menu', lambda x: nav_drawer.set_state('open')]]
    
        NavigationLayout:
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
                                    text: "Info"

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


# class ContentEmail(BoxLayout):
#     pass


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()

class CasesList(OneLineAvatarIconListItem):
    text = StringProperty()


class PMIApp(MDApp):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.store = JsonStore('pmi.json')
        
        self.screen = Builder.load_string(KV)

        menu_items_cover = [{"text": "Naakt"}, 
                        {"text": "Een of twee dunne lagen"},
                        {"text": "Een of twee dikke lagen"},
                        {"text": "Twee of drie lagen"},
                        {"text": "Drie of vier lagen"},
                        {"text": "Meer lagen"},
                        {"text": "Licht beddengoed"},
                        {"text": "Zwaar beddengoed"},
                        ]

        self.menu_cover = MDDropdownMenu(caller=self.screen.ids.drop_item_cover, items=menu_items_cover, position="auto", width_mult=6)
        self.menu_cover.bind(on_release=self.set_item_cover)

        menu_items_surFact = [{"text": "Droog lichaam, binnen"}, 
                        {"text": "Droog lichaam, buiten"},
                        {"text": "Nat lichaam, binnen"},
                        {"text": "Nat lichaam, buiten"},
                        {"text": "Stilstaand water"},
                        {"text": "Stromend water"},
                        ]

        self.menu_surFact = MDDropdownMenu(caller=self.screen.ids.drop_item_surFact, items=menu_items_surFact, position="auto", width_mult=4)
        self.menu_surFact.bind(on_release=self.set_item_surFact)


    def set_item_cover(self, instance_menu, instance_menu_item):
        instance_menu.dismiss()
        cover_button = self.root.ids.drop_item_cover
        cover_button.text = str(instance_menu_item.text)

        self.cover_nl = instance_menu_item.text
        self.callback_cover(self.cover_nl)


    def set_item_surFact(self, instance_menu, instance_menu_item):
        instance_menu.dismiss()
        surFact_button = self.root.ids.drop_item_surFact
        surFact_button.text = str(instance_menu_item.text)

        self.surFact_nl = instance_menu_item.text
        self.callback_surFact(self.surFact_nl)

    
    def remove_item(self, instance):
        if self.store.exists(instance.text):
            self.store.delete(instance.text)
            self.screen.ids.container.remove_widget(instance)
        else:
            pass


    def on_start(self):
        self.set_list()

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
        
        casenr = inst.text
        data = self.store.get(casenr)

        self.root.ids.report.add_widget(
            MDLabel(text='Lichaamstemperatuur:    ' + str(data['bodyTemp']) + chr(176))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )
        self.root.ids.report.add_widget(
            MDLabel(text='Omgevingstemperatuur:    ' + str(data['surTemp'])+ chr(176))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Lichaamsgewicht:    ' + str(data['bodyWeight']) + 'kg')
        )
        
        self.root.ids.report.add_widget(
            MDSeparator()
        )
        
        self.root.ids.report.add_widget(
            MDLabel(text='Lichaamsbedekking:    ' + str(data['cover']))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Omgevingsfactoren:    ' + str(data['surFact']))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Datum en tijd van berekenen:    ' + str(data['datetime_calc']))
        )
        
        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Correctiefactor:    ' + str(data['f_value']))
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        self.root.ids.report.add_widget(
            MDLabel(text='Post Mortem Interval:    ' + str(data['pmi_save']))
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
            Image(source=data['formula'])
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
            Image(source=data['formulaB'])
        )

        self.root.ids.report.add_widget(
            MDSeparator()
        )

        
        # self.root.ids.report.add_widget(
        #     MDRaisedButton(text='Email report', on_release=lambda *args: self.dialog_email(casenr, *args)) 
        # )


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
        self.corrective_factor = self.get_corrective_factor(self.cover, self.surFact)
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

        alt_date = str(self.date).split("-")
        alt_time = str(self.time).split(":")
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
        
        # except ValueError:
        #     self.pmi = "Error, "
        #     self.longest_shortest_text = "vul een geldige waarde in."
        #     return self.pmi, self.longest_shortest_text
        
        # except AttributeError:
        #     self.pmi = "Error, "
        #     self.longest_shortest_text = "vul een geldige waarde in."
        #     return self.pmi, self.longest_shortest_text   


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
        
        self.store.put(casenr, datetime_calc=str(datetime_calc), f_value=f_value, pmi_save=pmi_save, 
                        min_pmi=min_pmi, max_pmi=max_pmi, bodyTemp=bodyTemp, surTemp=surTemp, bodyWeight=bodyWeight,
                        cover=cover, surFact=surFact, formula=casenr + '_formula.png', formulaB=casenr + 'B.png')

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
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()


    def get_date(self, *args):
        date_button = self.root.ids.date_button
        date_button.text = str(args[0])
        self.date = args[0]
        print(self.date)
        return self.date


    # def dialog_email(self, casenr, inst):
    #     self.dialog_email = MDDialog(title="Voer uw e-mailadres in:", type="custom", content_cls=ContentEmail(), buttons=[
    #         MDFlatButton(text="BACK", text_color=self.theme_cls.primary_color, on_release=self.dismiss_alert_dialog_email),
    #         MDFlatButton(text="SEND", text_color=self.theme_cls.primary_color, on_press=lambda *args:self.send_email(casenr, *args), on_release=self.dismiss_alert_dialog_email),
    #         ],
    #     )

    #     self.dialog_email.open()

    
    # def dismiss_alert_dialog_email(self, inst):
    #     self.dialog_email.dismiss()

    # def send_email(self, casenr, inst):
    #     email = self.dialog_email.content_cls.ids.email.text
    #     pdf = FPDF()
  
    #     pdf.add_page()
    #     pdf.set_font("Arial", size = 12)
    #     pdf.cell(200, 10, txt = "Post Mortem Interval App", 
    #             ln = 1, align = 'C')
        
    #     pdf.cell(200, 10, txt = "Een automatisch gegenereed rapport van het post mortem interval met zaaknummer " + casenr,
    #             ln = 1, align = 'C')
        
    #     data = self.store.get(casenr)
    #     pdf.multi_cell(300, 10, txt = 
    #                             "\nZaaknummer:    " + str(casenr) + '\n' + 
    #                             "Datum van berekening:    " + str(data['datetime_calc']) + '\n' + 
    #                             "Correctiefactor:    " + str(data['f_value']) + '\n' +
    #                             "PMI:    " + str(data['pmi_save']) + '\n' +
    #                             "Minimale PMI:    " + str(data['min_pmi']) + '\n' +
    #                             "Maximale PMI:    " + str(data['max_pmi']) + '\n' +
    #                             "Lichaamsgewicht:    " + str(data['bodyWeight']) + 'kg\n' +
    #                             "Lichaamstemperatuur:    " + str(data['bodyTemp']) + chr(176) + '\n' +
    #                             "Omgevingstemperatuur:    " + str(data['surTemp']) + chr(176) + '\n' +
    #                             "Lichaamsbedekking:    " + str(data['cover']) + '\n' +
    #                             "Omgevingsfactoren:    " + str(data['surFact']) + '\n' +
    #                             "Formule:")
                                
    
    #     formula = str(data['formula'])
    #     pdf.image(formula, w=180, h=15)

    #     pdf.cell(200, 10, txt = "Formule B:    " + '\n\n',
    #             ln=1, align = 'L')

    #     formulaB = str(data['formulaB'])
    #     pdf.image(formulaB, w=180, h=12)

    #     pdf.output("Report.pdf")   

        
    #     subject = "Rapport Post Mortem Interval"
    #     body = "In het bijgevoegde PDF-bestand kunt u het rapport van het berekende PMI vinden."
    #     sender_email = 'ph'
    #     receiver_email = email
    #     password = 'ph'

    #     message = MIMEMultipart()
    #     message["From"] = sender_email
    #     message["To"] = receiver_email
    #     message["Subject"] = subject

    #     message.attach(MIMEText(body, "plain"))

    #     filename = r"Report.pdf"  # In same directory as script

    #     with open(filename, "rb") as attachment:
    #         part = MIMEBase("application", "octet-stream")
    #         part.set_payload(attachment.read())
        
    #     encoders.encode_base64(part)

    #     part.add_header(
    #         "Content-Disposition",
    #         f"attachment; filename= {filename}",
    #     )

    #     message.attach(part)
    #     text = message.as_string()

    #     # try:
    #     #     _create_unverified_https_context = ssl._create_unverified_context
    #     # except AttributeError:
    #     #     pass
    #     # else:
    #     #     ssl._create_default_https_context = _create_unverified_https_context

    #     context = ssl._create_unverified_context()

    #     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    #         server.login(sender_email, password)
    #         server.sendmail(sender_email, receiver_email, text)


    def switch_tab(self, instance):
        print('ok')
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
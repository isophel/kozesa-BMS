from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import Image

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.menu import MDDropdownMenu

import sys
sys.path.append(r"C:\Users\user\Desktop\OpenSourceCode\kozesa-BMS\sales-manager") #part of testing code.

from salesmanager.system.appstorage import AdminAccount,AccountManager
from pathlib import Path

#============= Testing ===================================
from kivymd.app import MDApp
import os


page_layout = r"""
<LoginForm>:
    id:loginform
    emp_user_entry:userentry
    emp_password_entry:passwordentry
    orientation:"vertical"
    pos_hint:{"x":0.5,"y":0.5}
    size_hint:(0.5,0.7)
    Image:
        source:r"C:\Users\user\Desktop\OpenSourceCode\kozesa-BMS\sales-manager\salesmanager\res\kozesa-orange-nobg.png"
    MDTextField:
        id:userentry
        multiline:False
        hint_text:"user name"
        on_text_validate:loginform.emp_user_validate(*args)
    MDTextField:
        id:passwordentry
        hint_text:"password"
        multiline:False
        on_text_validate:loginform.emp_password_validate(*args)
        
<AdminCreationForm>:
    id:admform
    orientation:"vertical"
    adm_name_entry:admnameentry
    adm_password_entry:admpasswordentry
    pos_hint:{"x":0.5,"y":0.5}
    size_hint:(0.5,0.7)
    Image:
        source:r"C:\Users\user\Desktop\OpenSourceCode\kozesa-BMS\sales-manager\salesmanager\res\kozesa-orange-nobg.png"
    MDTextField:
        id:admnameentry
        multiline:False
        on_text_validate:admform.adm_name_validate(*args)
    MDTextField:
        id:admpasswordentry
        multiline:False
        on_text_validate:admform.adm_password_validate(*args)
"""

Builder.load_string(page_layout)

class LoginPage (MDFloatLayout):
    def __init__(self,acc_manager,login_function,adm_panelopen_function):
        super (LoginPage,self).__init__()
        self.acc_manager = acc_manager
        if self.acc_manager.setup:
            self.login_menu = LoginMenu(adm_panelopen_function)
            self.menu_button = MDFloatingActionButton(pos_hint = {"x":0.9,"y":0.1},
                                                        icon = "format-list-bulleted",
                                                        on_release = lambda inst:self.login_menu.open()
                                                        )
            self.add_widget(LoginForm(acc_manager,login_function))
            self.add_widget(menu_button)
        else:
            self.add_widget(AdminCreationForm(acc_manager,adm_panelopen_function))
    
class LoginForm (MDBoxLayout):
    emp_user_entry = ObjectProperty ()
    emp_password_entry = ObjectProperty ()
    
    def __init__ (self,acc_manager,login_function):
        super (LoginForm,self).__init__()
        self.acc_manager = acc_manager
        self.login_function = login_function
        self.emp_user = str()
        self.emp_password = str()
            
        
    def emp_user_validate (self, field_inst:MDTextField) -> None:
        self.emp_user = field_inst.text
        self.emp_password_entry.focus = True
        return
    
    def emp_password_validate (self, field_inst:MDTextField) -> None:
        self.emp_password = field_inst.text
        self._validate()
        return
        
    def _validate (self):
        pass
        
class AdminCreationForm (MDBoxLayout):
    adm_name_entry = ObjectProperty()
    adm_password_entry = ObjectProperty()
    
    def __init__(self,acc_manager,adm_panelopen_function):
        super (AdminCreationForm,self).__init__()
        self.acc_manager = acc_manager
        self.adm_panelopen_function = adm_panelopen_function
        self.adm_name = str()
        self.adm_password = str()
        
        
    def adm_name_validate (self,field_inst:MDTextField) -> None:
        self.adm_name = field_inst.text
        self.adm_password_entry.focus = True
        return
       
    def adm_password_validate (self,field_inst:MDTextField) -> None:
        self.adm_password = field_inst.text
        self.createAdmin()
        return
    
    def createAdmin (self):
        pass

class LoginMenu (MDDropdownMenu):
    pass
    
if __name__ == "__main__":
    
    accman = AccountManager(Path(os.getcwd()))
    
    def logfunc ():
        print("logging...")
        
    def AdmCreateFunc ():
        print("creating admin...")
        
    class TestApp(MDApp):
        def __init__(self):
            super(TestApp,self).__init__()
            self.theme_cls.primary_palette = "DeepOrange"
            
        def build (self):
            return LoginPage(accman,logfunc,AdmCreateFunc)
            
    TestApp().run()
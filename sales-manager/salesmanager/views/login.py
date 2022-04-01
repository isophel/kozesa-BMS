import os
import sys
from pathlib import Path

from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from salesmanager.system.appstorage import AccountManager
from salesmanager.system.appstorage import AdminAccount

# part of testing code.
sys.path.append(r"C:\Users\user\Desktop\OpenSourceCode\kozesa-BMS\sales-manager")


# =================== Testing ===================================


page_layout = r"""
<LoginForm>:
    id:loginform
    emp_user_entry:userentry
    emp_password_entry:passwordentry
    orientation:"vertical"
    pos_hint:{"x":0.25,"y":0.4}
    size_hint:(0.5,0.6)
    spacing:5
    Image:
        source:r"C:\Users\user\Desktop\OpenSourceCode\kozesa-BMS\sales-manager\salesmanager\res\kozesa-orange-nobg.png"
        pos_hint:{"x":0,"y":0}
    MDLabel:
        text:"Employee Login."
        font_style:"H4"
    MDTextField:
        id:userentry
        multiline:False
        hint_text:"user name"
        icon_right:"account"
        icon_right_color_focus:app.theme_cls.primary_color
        on_text_validate:loginform.emp_user_validate(*args)
    MDTextField:
        id:passwordentry
        hint_text:"password"
        multiline:False
        password:True
        icon_right:"key"
        icon_right_color_focus:app.theme_cls.primary_color
        on_text_validate:loginform.emp_password_validate(*args)
    MDRaisedButton:
        text:"login"
        on_release:loginform.emp_login()
        size_hint_x:1
        
<AdminCreationForm>:
    id:admform
    orientation:"vertical"
    adm_name_entry:admnameentry
    adm_password_entry:admpasswordentry
    pos_hint:{"x":0.25,"y":0.4}
    size_hint:(0.5,0.6)
    spacing:5
    Image:
        source:r"C:\Users\user\Desktop\OpenSourceCode\kozesa-BMS\sales-manager\salesmanager\res\kozesa-orange-nobg.png"
        pos_hint:{"x":0,"y":0}
    MDLabel:
        text:"Create Admin Account to proceed."
        font_style:"H4"
    MDTextField:
        id:admnameentry
        multiline:False
        hint_text:"admin name"
        icon_right:"account"
        on_text_validate:admform.adm_name_validate(*args)
    MDTextField:
        id:admpasswordentry
        multiline:False
        hint_text:"admin password"
        password:True
        icon_right:"key"
        on_text_validate:admform.adm_password_validate(*args)
    MDRaisedButton:
        text:"create"
        on_release:admform.createAdmin()
        size_hint_x:1
        
<LoginMenuItem>:
    text:self.text
    
"""

Builder.load_string(page_layout)


class LoginPage(MDFloatLayout):
    def __init__(self, acc_manager, login_function, adm_panelopen_function):
        super(LoginPage, self).__init__()
        self.acc_manager = acc_manager
        if self.acc_manager.setup:
            self.login_menu = LoginMenu(adm_panelopen_function)
            self.menu_button = MDFloatingActionButton(
                pos_hint={"x": 0.9, "y": 0.1},
                icon="format-list-bulleted",
                on_release=lambda inst: self.login_menu.open(),
            )
            self.add_widget(LoginForm(acc_manager, login_function))
            self.add_widget(self.menu_button)
        else:
            self.add_widget(AdminCreationForm(acc_manager, adm_panelopen_function))


class LoginForm(MDBoxLayout):
    emp_user_entry = ObjectProperty()
    emp_password_entry = ObjectProperty()

    def __init__(self, acc_manager, login_function):
        super(LoginForm, self).__init__()
        self.acc_manager = acc_manager
        self.login_function = login_function
        self.emp_user = str()
        self.emp_password = str()

    def emp_user_validate(self, field_inst: MDTextField) -> None:
        self.emp_user = field_inst.text
        self.emp_password_entry.focus = True
        return

    def emp_password_validate(self, field_inst: MDTextField) -> None:
        self.emp_password = field_inst.text
        self._validate()
        return

    def emp_login(self) -> None:
        if self.emp_user and self.emp_password:
            self._validate()

    def _validate(self):
        self.login_function(self.emp_user, self.emp_password)


class AdminCreationForm(MDBoxLayout):
    adm_name_entry = ObjectProperty()
    adm_password_entry = ObjectProperty()

    def __init__(self, acc_manager, adm_panelopen_function) -> None:
        super(AdminCreationForm, self).__init__()
        self.acc_manager = acc_manager
        self.adm_panelopen_function = adm_panelopen_function
        self.adm_name = str()
        self.adm_password = str()

    def adm_name_validate(self, field_inst: MDTextField) -> None:
        self.adm_name = field_inst.text
        self.adm_password_entry.focus = True
        return

    def adm_password_validate(self, field_inst: MDTextField) -> None:
        self.adm_password = field_inst.text
        self.createAdmin()
        return

    def createAdmin(self) -> None:
        if self.adm_name and self.adm_password:
            self.adm_panelopen_function(self.adm_name, self.adm_password)
        else:
            self.adm_name = self.adm_name_entry.text
            self.adm_password = self.adm_password_entry.text
            self.adm_panelopen_function(self.adm_name, self.adm_password)


class LoginMenu(MDDropdownMenu):
    def __init__(self, adm_panelopen_function):
        self.adm_panelopen_function = adm_panelopen_function


class LoginMenuItem(OneLineIconListItem):
    pass


# ============================== Testing ==========================================
if __name__ == "__main__":

    accman = AccountManager(Path(os.getcwd()))

    def logfunc(name, password):
        print("logging...")

    def AdmCreateFunc(name, password):
        print("creating admin...")
        accman.create(name, password, admin=True)

    class TestApp(MDApp):
        def __init__(self):
            super(TestApp, self).__init__()
            self.theme_cls.primary_palette = "DeepOrange"

        def build(self):
            return LoginPage(accman, logfunc, AdmCreateFunc)

    TestApp().run()

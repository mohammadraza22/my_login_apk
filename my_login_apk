from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
import sqlite3
import hashlib
import os
import threading
import time

Window.size = (400, 700)

# متغیرهای سراسری که بعداً در کلاس اپ مقداردهی میشن
DB_FILE = ''
AVATAR_DIR = ''

# 
#    (   )
# 
PUBLISHER_INFO = {
    'app_name': 'My Login App',
    'version': '1.0.0',
    'build_date': '1404/07/09',
    'developer': 'Arbab',
    'email': 'arbabkingok@gmail.com',
    'website': 'www.example.com',
    'telegram': '@arbab_dev',
    'instagram': '@arbab_dev',
    'description': '           .',
    'copyright': ' 1404 Arbab. All rights reserved.'
}


# 
#  
# 
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            avatar TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(username, email, phone, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''INSERT INTO users
                     (username, email, phone, password, created_at)
                     VALUES (?, ?, ?, ?, ?)''',
                  (username, email, phone, hash_password(password),
                   time.strftime('%Y-%m-%d %H:%M')))
        conn.commit()
        conn.close()
        return True, 'Registered successfully!'
    except sqlite3.IntegrityError:
        return False, 'Username already exists'
    except Exception as e:
        return False, str(e)


def check_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?',
              (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user


def check_email(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user


def update_password(username, new_password):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('UPDATE users SET password = ? WHERE username = ?',
                  (hash_password(new_password), username))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def update_avatar(username, avatar_path):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('UPDATE users SET avatar = ? WHERE username = ?',
                  (avatar_path, username))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_user_by_username(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user


current_user = {'username': '', 'email': '', 'phone': '', 'avatar': ''}


# 
#   
# 
class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'register'

        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=25,
                           spacing=8, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        title = Label(text='[b]Register[/b]', markup=True,
                      font_size='26sp', size_hint=(1, None), height=50,
                      color=(0.4, 0.8, 1, 1))
        layout.add_widget(title)

        layout.add_widget(Label(text='Username', size_hint=(1, None), height=25))
        self.username_input = TextInput(multiline=False,
                                        size_hint=(1, None), height=45,
                                        hint_text='Enter username')
        layout.add_widget(self.username_input)

        layout.add_widget(Label(text='Email', size_hint=(1, None), height=25))
        self.email_input = TextInput(multiline=False,
                                     size_hint=(1, None), height=45,
                                     hint_text='example@email.com')
        layout.add_widget(self.email_input)

        layout.add_widget(Label(text='Phone (optional)',
                                size_hint=(1, None), height=25))
        self.phone_input = TextInput(multiline=False,
                                     size_hint=(1, None), height=45,
                                     input_type='number',
                                     hint_text='09123456789')
        layout.add_widget(self.phone_input)

        layout.add_widget(Label(text='Password', size_hint=(1, None), height=25))
        self.password_input = TextInput(multiline=False,
                                        size_hint=(1, None), height=45,
                                        password=True,
                                        hint_text='Enter password')
        layout.add_widget(self.password_input)

        layout.add_widget(Label(text='Confirm Password',
                                size_hint=(1, None), height=25))
        self.confirm_input = TextInput(multiline=False,
                                       size_hint=(1, None), height=45,
                                       password=True,
                                       hint_text='Repeat password')
        layout.add_widget(self.confirm_input)

        layout.add_widget(Label(size_hint=(1, None), height=15))

        register_btn = Button(text='Register', font_size='17sp',
                              size_hint=(0.8, None), height=50,
                              pos_hint={'center_x': 0.5},
                              background_color=(0.2, 0.6, 0.9, 1))
        register_btn.bind(on_press=self.register)
        layout.add_widget(register_btn)

        login_btn = Button(text='Already have account? Login',
                           font_size='12sp', size_hint=(1, None), height=35,
                           background_normal='',
                           background_color=(0, 0, 0, 0),
                           color=(0.4, 0.8, 1, 1))
        login_btn.bind(on_press=self.go_login)
        layout.add_widget(login_btn)

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def register(self, *args):
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        phone = self.phone_input.text.strip()
        password = self.password_input.text
        confirm = self.confirm_input.text

        if not username or not email or not password:
            self.show_msg('Error', 'Please fill all required fields')
            return
        if '@' not in email or '.' not in email:
            self.show_msg('Error', 'Invalid email')
            return
        if len(password) < 4:
            self.show_msg('Error', 'Password must be 4+ characters')
            return
        if password != confirm:
            self.show_msg('Error', 'Passwords do not match')
            return

        self.show_msg('Connecting...', 'Sending to server...')
        threading.Thread(target=self.do_register,
                         args=(username, email, phone, password)).start()

    def do_register(self, username, email, phone, password):
        time.sleep(1.2)
        success, msg = add_user(username, email, phone, password)
        Clock.schedule_once(lambda dt: self.show_result(success, msg), 0)

    def show_result(self, success, msg):
        if success:
            self.show_msg('Success', msg + '\nYou can login now!')
            self.username_input.text = ''
            self.email_input.text = ''
            self.phone_input.text = ''
            self.password_input.text = ''
            self.confirm_input.text = ''
        else:
            self.show_msg('Error', msg)

    def go_login(self, *args):
        self.manager.current = 'login'

    def show_msg(self, title, msg):
        Popup(title=title, content=Label(text=msg),
              size_hint=(0.8, 0.35)).open()


# 
#   
# 
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'

        layout = BoxLayout(orientation='vertical', padding=30, spacing=10)

        title = Label(text='[b]Welcome Back[/b]', markup=True,
                      font_size='26sp', size_hint=(1, 0.1),
                      color=(0.4, 0.8, 1, 1))
        layout.add_widget(title)

        layout.add_widget(Label(size_hint=(1, 0.05)))

        layout.add_widget(Label(text='Username', size_hint=(1, 0.05)))
        self.username_input = TextInput(multiline=False,
                                        size_hint=(1, 0.1),
                                        hint_text='Enter username')
        layout.add_widget(self.username_input)

        layout.add_widget(Label(text='Password', size_hint=(1, 0.05)))
        self.password_input = TextInput(multiline=False,
                                        size_hint=(1, 0.1),
                                        password=True,
                                        hint_text='Enter password')
        layout.add_widget(self.password_input)

        layout.add_widget(Label(size_hint=(1, 0.05)))

        login_btn = Button(text='Login', font_size='18sp',
                           size_hint=(0.8, 0.12),
                           pos_hint={'center_x': 0.5},
                           background_color=(0.2, 0.6, 0.9, 1))
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)

        forgot_btn = Button(text='Forgot Password?',
                            font_size='12sp', size_hint=(1, 0.06),
                            background_normal='',
                            background_color=(0, 0, 0, 0),
                            color=(1, 0.6, 0.4, 1))
        forgot_btn.bind(on_press=self.go_forgot)
        layout.add_widget(forgot_btn)

        register_btn = Button(text="Don't have account? Register",
                              font_size='12sp', size_hint=(1, 0.06),
                              background_normal='',
                              background_color=(0, 0, 0, 0),
                              color=(0.4, 0.8, 1, 1))
        register_btn.bind(on_press=self.go_register)
        layout.add_widget(register_btn)

        about_btn = Button(text='About /  ',
                           font_size='12sp', size_hint=(1, 0.06),
                           background_normal='',
                           background_color=(0, 0, 0, 0),
                           color=(0.7, 0.5, 1, 1))
        about_btn.bind(on_press=self.go_about)
        layout.add_widget(about_btn)

        self.add_widget(layout)

    def login(self, *args):
        username = self.username_input.text.strip()
        password = self.password_input.text

        if not username or not password:
            self.show_msg('Error', 'Enter username and password')
            return

        self.show_msg('Connecting...', 'Checking with server...')
        threading.Thread(target=self.do_login,
                         args=(username, password)).start()

    def do_login(self, username, password):
        time.sleep(1.2)
        user = check_user(username, password)
        Clock.schedule_once(lambda dt: self.show_result(user), 0)

    def show_result(self, user):
        if user:
            current_user['username'] = user[1]
            current_user['email'] = user[2]
            current_user['phone'] = user[3] or 'Not set'
            current_user['avatar'] = user[5] or ''
            profile = self.manager.get_screen('profile')
            profile.load_user()
            self.manager.current = 'profile'
        else:
            self.show_msg('Error', 'Wrong username or password')

    def go_register(self, *args):
        self.manager.current = 'register'

    def go_forgot(self, *args):
        self.manager.current = 'forgot'

    def go_about(self, *args):
        self.manager.current = 'about'

    def show_msg(self, title, msg):
        Popup(title=title, content=Label(text=msg),
              size_hint=(0.8, 0.35)).open()


# 
#    
# 
class ForgotScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'forgot'

        layout = BoxLayout(orientation='vertical', padding=30, spacing=10)

        title = Label(text='[b]Reset Password[/b]', markup=True,
                      font_size='24sp', size_hint=(1, 0.1),
                      color=(1, 0.6, 0.4, 1))
        layout.add_widget(title)

        layout.add_widget(Label(text='Enter your email',
                                size_hint=(1, 0.06)))
        self.email_input = TextInput(multiline=False,
                                     size_hint=(1, 0.1),
                                     hint_text='example@email.com')
        layout.add_widget(self.email_input)

        layout.add_widget(Label(size_hint=(1, 0.05)))

        check_btn = Button(text='Check Email', font_size='16sp',
                           size_hint=(0.8, 0.1),
                           pos_hint={'center_x': 0.5},
                           background_color=(1, 0.6, 0.4, 1))
        check_btn.bind(on_press=self.check_email)
        layout.add_widget(check_btn)

        layout.add_widget(Label(size_hint=(1, 0.05)))

        layout.add_widget(Label(text='New Password',
                                size_hint=(1, 0.05)))
        self.new_password = TextInput(multiline=False,
                                      size_hint=(1, 0.1),
                                      password=True,
                                      hint_text='New password')
        layout.add_widget(self.new_password)

        layout.add_widget(Label(size_hint=(1, 0.05)))

        reset_btn = Button(text='Reset Password', font_size='16sp',
                           size_hint=(0.8, 0.1),
                           pos_hint={'center_x': 0.5},
                           background_color=(0.9, 0.3, 0.5, 1))
        reset_btn.bind(on_press=self.reset_password)
        layout.add_widget(reset_btn)

        back_btn = Button(text='<< Back to Login',
                          font_size='12sp', size_hint=(1, 0.06),
                          background_normal='',
                          background_color=(0, 0, 0, 0),
                          color=(0.4, 0.8, 1, 1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.found_username = ''
        self.add_widget(layout)

    def check_email(self, *args):
        email = self.email_input.text.strip()
        if not email:
            self.show_msg('Error', 'Enter your email')
            return
        self.show_msg('Checking...', 'Looking in database...')
        threading.Thread(target=self.do_check, args=(email,)).start()

    def do_check(self, email):
        time.sleep(1)
        user = check_email(email)
        Clock.schedule_once(lambda dt: self.show_check_result(user), 0)

    def show_check_result(self, user):
        if user:
            self.found_username = user[1]
            self.show_msg('Found', 'User: ' + user[1] +
                          '\nEnter new password and click Reset')
        else:
            self.show_msg('Error', 'Email not found')

    def reset_password(self, *args):
        new_pass = self.new_password.text
        if not self.found_username:
            self.show_msg('Error', 'First check your email')
            return
        if len(new_pass) < 4:
            self.show_msg('Error', 'Password must be 4+ chars')
            return

        if update_password(self.found_username, new_pass):
            self.show_msg('Success', 'Password changed!')
            self.new_password.text = ''
            self.email_input.text = ''
            self.found_username = ''
        else:
            self.show_msg('Error', 'Could not update')

    def go_back(self, *args):
        self.manager.current = 'login'

    def show_msg(self, title, msg):
        Popup(title=title, content=Label(text=msg),
              size_hint=(0.8, 0.35)).open()


# 
#   
# 
class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'profile'

        self.layout = BoxLayout(orientation='vertical', padding=25, spacing=10)

        self.add_widget(Label(size_hint=(1, 0.02)))

        self.avatar = Image(size_hint=(1, 0.3))
        self.layout.add_widget(self.avatar)

        avatar_btn = Button(text='Change Avatar',
                            font_size='12sp', size_hint=(0.5, 0.06),
                            pos_hint={'center_x': 0.5},
                            background_color=(0.5, 0.3, 0.7, 1))
        avatar_btn.bind(on_press=self.change_avatar)
        self.layout.add_widget(avatar_btn)

        self.add_widget(self.layout)

        self.info_label = Label(
            text='', size_hint=(1, 0.25),
            font_size='14sp', halign='center', valign='middle', markup=True
        )
        self.info_label.bind(size=self.info_label.setter('text_size'))
        self.layout.add_widget(self.info_label)

        about_btn = Button(text='About /  ',
                           font_size='14sp', size_hint=(0.8, 0.08),
                           pos_hint={'center_x': 0.5},
                           background_color=(0.5, 0.3, 0.7, 1))
        about_btn.bind(on_press=self.go_about)
        self.layout.add_widget(about_btn)

        logout_btn = Button(text='Logout', font_size='15sp',
                            size_hint=(0.8, 0.09),
                            pos_hint={'center_x': 0.5},
                            background_color=(0.9, 0.3, 0.3, 1))
        logout_btn.bind(on_press=self.logout)
        self.layout.add_widget(logout_btn)

        self.add_widget(Label(size_hint=(1, 0.02)))

    def load_user(self):
        username = current_user['username']
        user = get_user_by_username(username)

        if user and user[5] and os.path.exists(user[5]):
            self.avatar.source = user[5]
        else:
            self.avatar.source = ''

        self.info_label.text = (
            '[b]Username:[/b] ' + current_user['username'] + '\n\n' +
            '[b]Email:[/b] ' + current_user['email'] + '\n\n' +
            '[b]Phone:[/b] ' + current_user['phone'] + '\n\n' +
            '[b]Joined:[/b] ' + (user[6] if user else 'Unknown')
        )

    def change_avatar(self, *args):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Enter image path:'))

        # تغییر مسیر پیش‌فرض به مسیر استاندارد اندروید
        path_input = TextInput(
            text='/storage/emulated/0/Download/',
            multiline=False, size_hint=(1, 0.3)
        )
        content.add_widget(path_input)

        btn_layout = BoxLayout(size_hint=(1, 0.3), spacing=5)

        popup = Popup(title='Avatar Path', content=content,
                      size_hint=(0.9, 0.4))

        def save_avatar(inst):
            import shutil
            src = path_input.text.strip()
            try:
                if os.path.isfile(src):
                    ext = os.path.splitext(src)[1]
                    dst = os.path.join(AVATAR_DIR,
                                       current_user['username'] + ext)
                    shutil.copy(src, dst)
                    update_avatar(current_user['username'], dst)
                    self.avatar.source = ''
                    self.avatar.source = dst
                    popup.dismiss()
                else:
                    for f in os.listdir(src):
                        if f.lower().endswith(('.jpg', '.png', '.jpeg')):
                            full = os.path.join(src, f)
                            ext = os.path.splitext(f)[1]
                            dst = os.path.join(AVATAR_DIR,
                                               current_user['username'] + ext)
                            shutil.copy(full, dst)
                            update_avatar(current_user['username'], dst)
                            self.avatar.source = ''
                            self.avatar.source = dst
                            popup.dismiss()
                            return
            except Exception as e:
                print('Error:', e)

        ok_btn = Button(text='OK')
        ok_btn.bind(on_press=save_avatar)
        btn_layout.add_widget(ok_btn)

        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=popup.dismiss)
        btn_layout.add_widget(cancel_btn)

        content.add_widget(btn_layout)
        popup.open()

    def go_about(self, *args):
        self.manager.current = 'about'

    def logout(self, *args):
        current_user['username'] = ''
        current_user['email'] = ''
        current_user['phone'] = ''
        current_user['avatar'] = ''
        self.manager.current = 'login'


# 
#     (About)
# 
class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'about'

        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=25, spacing=12,
                           size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        logo = Label(text='[b]APP[/b]', markup=True, font_size='50sp',
                     size_hint=(1, None), height=80,
                     color=(0.4, 0.8, 1, 1))
        layout.add_widget(logo)

        app_title = Label(
            text='[b]' + PUBLISHER_INFO['app_name'] + '[/b]',
            markup=True, font_size='22sp',
            size_hint=(1, None), height=40
        )
        layout.add_widget(app_title)

        layout.add_widget(Label(
            text='' * 40, size_hint=(1, None), height=20,
            color=(0.5, 0.5, 0.5, 1)
        ))

        layout.add_widget(Label(
            text='[b]Version:[/b] ' + PUBLISHER_INFO['version'],
            markup=True, font_size='14sp',
            size_hint=(1, None), height=30,
            halign='left'
        ))
        layout.add_widget(Label(
            text='[b]Build Date:[/b] ' + PUBLISHER_INFO['build_date'],
            markup=True, font_size='14sp',
            size_hint=(1, None), height=30,
            halign='left'
        ))

        layout.add_widget(Label(
            text='' * 40, size_hint=(1, None), height=20,
            color=(0.5, 0.5, 0.5, 1)
        ))

        layout.add_widget(Label(
            text='[b]Developer Information[/b]',
            markup=True, font_size='16sp',
            size_hint=(1, None), height=30,
            color=(0.4, 0.8, 1, 1)
        ))

        info_rows = [
            ('Developer', PUBLISHER_INFO['developer']),
            ('Email', PUBLISHER_INFO['email']),
            ('Website', PUBLISHER_INFO['website']),
            ('Telegram', PUBLISHER_INFO['telegram']),
            ('Instagram', PUBLISHER_INFO['instagram']),
        ]

        for label, value in info_rows:
            row = BoxLayout(size_hint=(1, None), height=35)
            row.add_widget(Label(
                text='[b]' + label + ':[/b]',
                markup=True, size_hint=(0.35, 1),
                font_size='13sp', halign='right'
            ))
            row.add_widget(Label(
                text=value, size_hint=(0.65, 1),
                font_size='13sp', halign='left'
            ))
            layout.add_widget(row)

        layout.add_widget(Label(
            text='' * 40, size_hint=(1, None), height=20,
            color=(0.5, 0.5, 0.5, 1)
        ))

        layout.add_widget(Label(
            text='[b]About App[/b]',
            markup=True, font_size='16sp',
            size_hint=(1, None), height=30,
            color=(0.4, 0.8, 1, 1)
        ))

        desc_label = Label(
            text=PUBLISHER_INFO['description'],
            font_size='13sp', size_hint=(1, None), height=80,
            halign='center', valign='middle'
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        layout.add_widget(desc_label)

        layout.add_widget(Label(
            text='' * 40, size_hint=(1, None), height=20,
            color=(0.5, 0.5, 0.5, 1)
        ))

        layout.add_widget(Label(
            text=PUBLISHER_INFO['copyright'],
            font_size='11sp', size_hint=(1, None), height=40,
            color=(0.6, 0.6, 0.6, 1),
            halign='center'
        ))

        layout.add_widget(Label(size_hint=(1, None), height=20))

        back_btn = Button(
            text='<< Back', font_size='15sp',
            size_hint=(0.7, None), height=45,
            pos_hint={'center_x': 0.5},
            background_color=(0.2, 0.6, 0.9, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        layout.add_widget(Label(size_hint=(1, None), height=30))

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def go_back(self, *args):
        if current_user['username']:
            self.manager.current = 'profile'
        else:
            self.manager.current = 'login'


# 
#   (تغییرات اصلی اینجاست)
# 
class LoginApp(App):
    def build(self):
        global DB_FILE, AVATAR_DIR
        
        # تنظیم مسیر دیتابیس و آواتار بر اساس پوشه اختصاصی اپ در اندروید
        DB_FILE = os.path.join(self.user_data_dir, 'users.db')
        AVATAR_DIR = os.path.join(self.user_data_dir, 'avatars')
        
        # ساخت پوشه آواتار در صورت نبودن
        if not os.path.exists(AVATAR_DIR):
            os.makedirs(AVATAR_DIR)

        init_db()
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen())
        sm.add_widget(RegisterScreen())
        sm.add_widget(ForgotScreen())
        sm.add_widget(ProfileScreen())
        sm.add_widget(AboutScreen())
        sm.current = 'login'
        return sm


LoginApp().run()

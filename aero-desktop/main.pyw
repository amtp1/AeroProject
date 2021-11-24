from json import dumps, loads
from os import path, mkdir, listdir, remove, environ, rmdir, umask
from tkinter import *
from tkinter import messagebox

from requests import get

class AeroLogin:
    def __init__(self, root, host: str, port: int):
        """Initialization"""

        self.root = root
        self.host = host
        self.port = port
        self.initialization_elememnts()

    def initialization_elememnts(self):
        # Login page elements
        #Labels
        self.log_last_name_lbl = Label(self.root, width=20, text="Фамилия")
        self.log_last_name_lbl.grid(row=0, column=0, sticky=NW, padx=190, pady=100)

        self.log_department_lbl = Label(self.root, width=20, text="Отдел")
        self.log_department_lbl.grid(row=0, column=0, sticky=NW, padx=190, pady=150)

        self.log_password_lbl = Label(self.root, width=20, text="Пароль")
        self.log_password_lbl.grid(row=0, column=0, sticky=NW, padx=190, pady=200)

        # Entries
        self.log_last_name_entry = Entry(self.root, width=40)
        self.log_last_name_entry.grid(row=0, column=0, sticky=NW, padx=370, pady=100)

        self.log_department_entry = Entry(self.root, width=40)
        self.log_department_entry.grid(row=0, column=0, sticky=NW, padx=370, pady=150)

        self.log_password_entry = Entry(self.root, width=40, show="*")
        self.log_password_entry.grid(row=0, column=0, sticky=NW, padx=370, pady=200)

        # Button
        self.login_button = Button(self.root, text="Войти", bd=0, width=59, height=2, command=self.auth_user)
        self.login_button.grid(row=0, column=0, sticky=NW, padx=190, pady=270, ipadx=3)

        self.registration_lbl = Label(self.root, text=r"Нет аккаунта? Зарегистрироваться",
                fg="blue", cursor="hand2",
                width=59, height=2)
        self.registration_lbl.grid(row=0, column=0, sticky=NW, padx=190, ipadx=3)
        self.registration_lbl.bind("<Button-1>", self.registration_user)

        # Registration page elements
        #Labels
        self.reg_last_name_lbl = Label(self.root, width=20, text="Фамилия")
        self.reg_first_name_lbl = Label(self.root, width=20, text="Имя")
        self.reg_middle_name_lbl = Label(self.root, width=20, text="Отчество")
        self.reg_position_lbl = Label(self.root, width=20, text="Должность")
        self.reg_department_lbl = Label(self.root, width=20, text="Отдел")
        self.reg_password_lbl = Label(self.root, width=20, text="Пароль")

        # Entries
        self.reg_last_name_entry = Entry(self.root, width=40)
        self.reg_first_name_entry = Entry(self.root, width=40)
        self.reg_middle_name_entry = Entry(self.root, width=40)
        self.reg_position_entry = Entry(self.root, width=40)
        self.reg_department_entry = Entry(self.root, width=40)
        self.reg_password_entry = Entry(self.root, width=40, show="*")

        # Button
        self.reg_button = Button(self.root, text="Зарегистрироваться", bd=0, width=59, height=2, command=self.reg_user)

        self.login_lbl = Label(self.root, text=r"У вас уже есть аккаунт? Войти",
                fg="blue", cursor="hand2",
                width=59, height=2)
        self.login_lbl.bind("<Button-1>", self.login_user)

    def auth_user(self):
        last_name = self.log_last_name_entry.get()
        department = self.log_department_entry.get()
        password = self.log_password_entry.get()
        login_user_data = {
            "host": self.host,
            "port": self.port,
            "last_name": last_name,
            "department": department,
            "password": password
        }
        if last_name and department and password:
            try:
                user_data = get(r"http://%(host)s:%(port)i/api/user-login/%(last_name)s/%(department)s/%(password)s/" % (login_user_data))
                user_data = loads(user_data.text)
                if not user_data["is_reg"]:
                    return messagebox.showinfo("Вход", "Пользователь не найден! Нужно пройти регистрацию.")
                else:
                    if not bool(user_data["user"]):
                        return messagebox.showinfo("Вход", "Неверные данные!")
                    else:
                        with open(r"session/%s" % last_name, "w") as save_session:
                            save_session.close()
                        update_active_data = {
                            "host": self.host,
                            "port": self.port,
                            "last_name": last_name,
                            "value": 1
                        }
                        get("http://%(host)s:%(port)i/api/user-update-active/%(last_name)s/%(value)i" % update_active_data)
                        self.remove_login_elements_for_main_page()
                        return Aero(root, last_name, host=self.host, port=self.port)
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        else:
            return messagebox.showinfo("Вход", "Поля не должны оставаться пустыми!")

    def reg_user(self):
        last_name = self.reg_last_name_entry.get()
        first_name = self.reg_first_name_entry.get()
        middle_name = self.reg_middle_name_entry.get()
        position = self.reg_position_entry.get()
        department = self.reg_department_entry.get()
        password =self.reg_password_entry.get()
        register_user_data = {
            "host": self.host,
            "port": self.port,
            "last_name": last_name,
            "first_name": first_name,
            "middle_name": middle_name,
            "position": position,
            "department": department,
            "password": password
        }
        if (last_name and first_name and middle_name and 
            position and department and password):
                try:
                    response = get(("http://%(host)s:%(port)i/api/user-register/%(last_name)s/%(first_name)s"
                        "/%(middle_name)s/%(position)s/%(department)s/%(password)s/") % (register_user_data))

                    if loads(response.text)["response"]:
                        return messagebox.showinfo("Регистрация", "Регистрация прошла успешно!")
                    else:
                        return messagebox.showinfo("Регистрация", "Пользователь уже существует!")
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
        else:
            return messagebox.showinfo("Регистрация", "Поля не должны оставаться пустыми!")

    def registration_user(self, event):
        self.remove_login_elements()

    def login_user(self, event):
        self.remove_registration_elements()

    def remove_login_elements(self):
        self.log_last_name_lbl.grid_remove()
        self.log_department_lbl.grid_remove()
        self.log_password_lbl.grid_remove()
        self.log_last_name_entry.grid_remove()
        self.log_department_entry.grid_remove()
        self.log_password_entry.grid_remove()
        self.login_button.grid_remove()
        self.registration_lbl.grid_remove()

        self.reg_last_name_lbl.grid(row=0, column=0, sticky=NW, padx=190, pady=100)
        self.reg_first_name_lbl.grid(row=0, column=0, sticky=NW, padx=190, pady=150)
        self.reg_middle_name_lbl.grid(row=0, column=0, sticky=NW, padx=190, pady=200)
        self.reg_position_lbl.grid(row=0, column=0, sticky=NW, padx=190, pady=250)
        self.reg_department_lbl.grid(row=0, column=0, sticky=NW, padx=190, pady=300)
        self.reg_password_lbl.grid(row=0, column=0, sticky=NW, padx=190, pady=350)
        self.reg_last_name_entry.grid(row=0, column=0, sticky=NW, padx=370, pady=100)
        self.reg_first_name_entry.grid(row=0, column=0, sticky=NW, padx=370, pady=150)
        self.reg_middle_name_entry.grid(row=0, column=0, sticky=NW, padx=370, pady=200)
        self.reg_position_entry.grid(row=0, column=0, sticky=NW, padx=370, pady=250)
        self.reg_department_entry.grid(row=0, column=0, sticky=NW, padx=370, pady=300)
        self.reg_password_entry.grid(row=0, column=0, sticky=NW, padx=370, pady=350)
        self.reg_button.grid(row=0, column=0, sticky=NW, padx=190, pady=400, ipadx=3)
        self.login_lbl.grid(row=0, column=0, sticky=NW, padx=190, ipadx=3)
    
    def remove_login_elements_for_main_page(self):
        self.log_last_name_lbl.grid_remove()
        self.log_department_lbl.grid_remove()
        self.log_password_lbl.grid_remove()
        self.log_last_name_entry.grid_remove()
        self.log_department_entry.grid_remove()
        self.log_password_entry.grid_remove()
        self.login_button.grid_remove()
        self.registration_lbl.grid_remove()

    def remove_registration_elements(self):
        self.reg_last_name_lbl.grid_remove()
        self.reg_first_name_lbl.grid_remove()
        self.reg_middle_name_lbl.grid_remove()
        self.reg_position_lbl.grid_remove()
        self.reg_department_lbl.grid_remove()
        self.reg_password_lbl.grid_remove()
        self.reg_last_name_entry.grid_remove()
        self.reg_first_name_entry.grid_remove()
        self.reg_middle_name_entry.grid_remove()
        self.reg_position_entry.grid_remove()
        self.reg_department_entry.grid_remove()
        self.reg_password_entry.grid_remove()
        self.reg_button.grid_remove()
        self.login_lbl.grid_remove()

        self.log_last_name_lbl.grid()
        self.log_department_lbl.grid()
        self.log_password_lbl.grid()
        self.log_last_name_entry.grid()
        self.log_department_entry.grid()
        self.log_password_entry.grid()
        self.login_button.grid()
        self.registration_lbl.grid()


class Aero:
    def __init__(self, root, last_name: str, host: str, port: int):
        """Initialization"""

        self.root = root # Main Window
        self.last_name = last_name
        self.host = host
        self.port = port
        self.initialization_elements()

    def initialization_elements(self):
        # Main page elements
        self.main_page_btn = Button(self.root, text="Главная страница",
                bd=0, bg="black",
                fg="white", width=15,
                height=3, activeforeground="grey13",
                activebackground="grey13", command=self.main_page,
                cursor="hand2")
        self.main_page_btn.grid(row=0, column=0, sticky=NW)

        self.employees_btn = Button(self.root, text="Сотрудники",
                bd=0, bg="black",
                fg="white", width=15,
                height=3, activeforeground="grey13",
                activebackground="grey13", command=self.employees_page,
                cursor="hand2")
        self.employees_btn.grid(row=0, column=0, sticky=NW, padx=120)

        self.departments_btn = Button(self.root, text="Отделы",
                bd=0, bg="black",
                fg="white", width=15,
                height=3, activeforeground="grey13",
                activebackground="grey13", command=self.departments_page,
                cursor="hand2")
        self.departments_btn.grid(row=0, column=0, sticky=NW, padx=240)

        self.current_page_lbl = Label(self.root, text="Текущая страница: Главная",
                width=40, height=2,
                bg="yellow3", font=("Ubuntu", 9, "bold"))
        self.current_page_lbl.grid(row=0, column=0, sticky=NW, padx=370)

        variable = StringVar(self.root)
        variable.set("👤") # default value
        self.user_profile_actions = OptionMenu(self.root, variable, 
                "Выход", command=self.actions_callback)
        self.user_profile_actions.config(bg="black", fg="WHITE", activebackground="grey13", activeforeground="grey13", bd=0)
        self.user_profile_actions["menu"].config(bg="red", activebackground="red", activeforeground="black")
        self.user_profile_actions.grid(row=0, column=0, sticky=NW, padx=678, ipadx=30, ipady=12)

        # Own page
        self.calendar_btn = Button(self.root, text="Календарь",
                bd=0, bg="gray23",
                fg="white", width=25,
                height=5, activeforeground="grey13",
                activebackground="grey13", command=self.calendar_page,
                cursor="hand2")
        self.calendar_btn.grid(row=0, column=0, sticky=NW, pady=70)

        self.chat_btn = Button(self.root, text="Чат",
                bd=0, bg="gray23",
                fg="white", width=25,
                height=5, activeforeground="grey13",
                activebackground="grey13", command=self.chat_page,
                cursor="hand2")
        self.chat_btn.grid(row=0, column=0, sticky=NW, pady=170)

        self.make_calculations = Button(self.root, text="Провести расчёт",
                bd=0, bg="gray23",
                fg="white", width=25,
                height=5, activeforeground="grey13",
                activebackground="grey13", command=self.calculator_page,
                cursor="hand2")
        self.make_calculations.grid(row=0, column=0, sticky=NW, pady=270)

        self.notify_error_btn = Button(self.root, text="Сообщить о поломке",
                bd=0, bg="gray23",
                fg="white", width=25,
                height=5, activeforeground="grey13",
                activebackground="grey13", command=self.notify_error_page,
                cursor="hand2")
        self.notify_error_btn.grid(row=0, column=0, sticky=NW, pady=370)

        # Employees page elements
        # Labels
        self.fio_lbl = Label(self.root, text="ФИО",
                width=25)
        self.position_lbl = Label(self.root, text="Должность",
                width=25)
        self.department_lbl = Label(self.root, text="Отдел",
                width=25)
        self.date_lbl = Label(self.root, text="Дата принятия на работу",
                width=25)

        # Text and Scroll (FIO)
        self.fio_txtbox = Text(self.root, width=20, height=28, bd=0)
        self.fio_txtbox.insert("end", "ФИО" * 250)
        self.fio_txtbox.configure(state="disabled")

        self.fio_scrollbar = Scrollbar(self.root, command=self.fio_txtbox.yview, bd=0)
        self.fio_txtbox.configure(yscrollcommand=self.fio_scrollbar.set)

        # Text and Scroll (Position)
        self.position_txtbox = Text(self.root, width=20, height=28, bd=0)
        self.position_txtbox.insert("end", "Должность" * 150)
        self.position_txtbox.configure(state="disabled")

        self.position_scrollbar = Scrollbar(self.root, command=self.position_txtbox.yview, bd=0)
        self.position_txtbox.configure(yscrollcommand=self.position_scrollbar.set)

        # Text and Scroll (Department)
        self.department_txtbox = Text(self.root, width=20, height=28, bd=0)
        self.department_txtbox.insert("end", "Отдел" * 150)
        self.department_txtbox.configure(state="disabled")

        self.department_scrollbar = Scrollbar(self.root, command=self.department_txtbox.yview, bd=0)
        self.department_txtbox.configure(yscrollcommand=self.department_scrollbar.set)

        # Text and Scroll (Date)
        self.date_txtbox = Text(self.root, width=20, height=28, bd=0)
        self.date_txtbox.insert("end", "Дата принятия на работу" * 150)
        self.date_txtbox.configure(state="disabled")

        self.date_scrollbar = Scrollbar(self.root, command=self.date_txtbox.yview, bd=0)
        self.date_txtbox.configure(yscrollcommand=self.date_scrollbar.set)

        # Departments page elements
        self._department_lbl = Label(self.root, text="Отдел",
                width=25)
        self.city_lbl = Label(self.root, text="Город",
                width=25)
        self.list_employees_lbl = Label(self.root, text="Список сотрудников",
                width=25)
        self.address_lbl = Label(self.root, text="Точный адрес",
                width=25)

        # Text and Scroll (FIO)
        self._department_txtbox = Text(self.root, width=20, height=28, bd=0)
        self._department_txtbox.insert("end", "Отдел" * 250)
        self._department_txtbox.configure(state="disabled")

        self._department_scrollbar = Scrollbar(self.root, command=self._department_txtbox.yview, bd=0)
        self._department_txtbox.configure(yscrollcommand=self._department_scrollbar.set)

        # Text and Scroll (Position)
        self.city_txtbox = Text(self.root, width=20, height=28, bd=0)
        self.city_txtbox.insert("end", "Город" * 150)
        self.city_txtbox.configure(state="disabled")

        self.city_scrollbar = Scrollbar(self.root, command=self.city_txtbox.yview, bd=0)
        self.city_txtbox.configure(yscrollcommand=self.city_scrollbar.set)

        # Text and Scroll (Department)
        self.list_employees_txtbox = Text(self.root, width=20, height=28, bd=0)
        self.list_employees_txtbox.insert("end", "Список сотрудников" * 150)
        self.list_employees_txtbox.configure(state="disabled")

        self.list_employees_scrollbar = Scrollbar(self.root, command=self.list_employees_txtbox.yview, bd=0)
        self.list_employees_txtbox.configure(yscrollcommand=self.list_employees_scrollbar.set)

        # Text and Scroll (Date)
        self.address_txtbox = Text(self.root, width=20, height=28, bd=0)
        self.address_txtbox.insert("end", "Точный адрес" * 150)
        self.address_txtbox.configure(state="disabled")

        self.address_scrollbar = Scrollbar(self.root, command=self.address_txtbox.yview, bd=0)
        self.address_txtbox.configure(yscrollcommand=self.address_scrollbar.set)

        # Notify error page elements
        # Text
        self.error_txtbox = Text(self.root, width=64, height=23)

        # Button
        self.error_btn = Button(self.root, text="Отправить", bd=0, width=13, height=2)

        # Chat page elements
        # Text and Scroll
        self.chat_txtbox = Text(self.root, wrap='none', width=64, bd=0)

        self.chat_scrollbar = Scrollbar(self.root, command=self.chat_txtbox.yview, bd=0)
        self.chat_txtbox.configure(yscrollcommand=self.chat_scrollbar.set)

        # Calendar page elements
        self.btn_params = {
            "bd":0,
            "width":15,
            "height":3,
            "cursor":"hand2",
            "bg":"#2E2E2B",
            "fg":"white",
            "activebackground":"gray20"
        }

        self.calculator_action: str = ""
        self.value_1: float = None
        self.value_2: float = None

        # Text and Scroll
        self.calendar_txtbox = Text(self.root, wrap='none', width=64, bd=0)

        self.calendar_scrollbar = Scrollbar(self.root, command=self.calendar_txtbox.yview, bd=0)
        self.calendar_txtbox.configure(yscrollcommand=self.calendar_scrollbar.set)

        # Calculations frame
        self.calculator_frame = Frame(self.root, bg="grey13")

        self.input_value = Entry(self.calculator_frame, font=('arial', 12, 'bold'), bd=0, width=49, bg='#595954', fg='white')
        self.input_value.grid(row=0, sticky=NW, ipady=10)

        self.one_btn = Button(self.calculator_frame, text="1", **self.btn_params, command=lambda: self.calculator_callback(1))
        self.one_btn.grid(row=1, sticky=NW)

        self.two_btn = Button(self.calculator_frame, text="2", **self.btn_params, command=lambda: self.calculator_callback(2))
        self.two_btn.grid(row=1, sticky=NW, padx=111)

        self.three_btn = Button(self.calculator_frame, text="3", **self.btn_params, command=lambda: self.calculator_callback(3))
        self.three_btn.grid(row=1, sticky=NW, padx=222)

        self.plus_btn = Button(self.calculator_frame, text="+", **self.btn_params, command=lambda: self.calculator_actions("+"))
        self.plus_btn.grid(row=1, padx=332)

        self.four_btn = Button(self.calculator_frame, text="4", **self.btn_params, command=lambda: self.calculator_callback(4))
        self.four_btn.grid(row=2, sticky=NW)

        self.five_btn = Button(self.calculator_frame, text="5", **self.btn_params, command=lambda: self.calculator_callback(5))
        self.five_btn.grid(row=2, sticky=NW, padx=111)

        self.six_btn = Button(self.calculator_frame, text="6", **self.btn_params, command=lambda: self.calculator_callback(6))
        self.six_btn.grid(row=2, sticky=NW, padx=222)

        self.sub_btn = Button(self.calculator_frame, text="-", **self.btn_params, command=lambda: self.calculator_actions("-"))
        self.sub_btn.grid(row=2, padx=332)

        self.seven_btn = Button(self.calculator_frame, text="7", **self.btn_params, command=lambda: self.calculator_callback(7))
        self.seven_btn.grid(row=3, sticky=NW)

        self.eight_btn = Button(self.calculator_frame, text="8", **self.btn_params, command=lambda: self.calculator_callback(8))
        self.eight_btn.grid(row=3, sticky=NW, padx=111)

        self.nine_btn = Button(self.calculator_frame, text="9", **self.btn_params, command=lambda: self.calculator_callback(9))
        self.nine_btn.grid(row=3, sticky=NW, padx=222)

        self.mul_btn = Button(self.calculator_frame, text="*", **self.btn_params, command=lambda: self.calculator_actions("*"))
        self.mul_btn.grid(row=3, padx=332)

        self.clear_btn = Button(self.calculator_frame, text="C", **self.btn_params, command=self.clear_value)
        self.clear_btn.grid(row=4, sticky=NW)

        self.zero_btn = Button(self.calculator_frame, text="0", **self.btn_params, command=lambda: self.calculator_callback(0))
        self.zero_btn.grid(row=4, sticky=NW, padx=111)

        self.res_btn = Button(self.calculator_frame, text="=", **self.btn_params, command=self.calculator_res)
        self.res_btn.grid(row=4, sticky=NW, padx=222)

        self.div_btn = Button(self.calculator_frame, text="/", **self.btn_params, command=lambda: self.calculator_actions("/"))
        self.div_btn.grid(row=4, padx=332)

    def main_page(self):
        self.current_page_lbl.configure(text="Текущая страница: Главная")

        self.remove_employyes_and_departments_elements()

        self.calendar_btn.grid()
        self.chat_btn.grid()
        self.make_calculations.grid()
        self.notify_error_btn.grid()

    def employees_page(self):
        self.current_page_lbl.configure(text="Текущая страница: Сотрудники")

        self.remove_main_page_and_departments_elements()

        # Employees
        # Set labels
        self.fio_lbl.grid(row=0, column=0, sticky=NW, pady=70)
        self.position_lbl.grid(row=0, column=0, sticky=NW, pady=70, padx=206)
        self.department_lbl.grid(row=0, column=0, sticky=NW, pady=70, padx=414)
        self.date_lbl.grid(row=0, column=0, sticky=NW, pady=70, padx=619)

        # Set texts
        self.fio_txtbox.grid(row=0, column=0, sticky=NW, pady=95)
        self.position_txtbox.grid(row=0, column=0, sticky=NW, pady=95, padx=206)
        self.department_txtbox.grid(row=0, column=0, sticky=NW, pady=95, padx=414)
        self.date_txtbox.grid(row=0, column=0, sticky=NW, pady=95, padx=619)

        # Set scrolls
        self.fio_scrollbar.grid(row=0, column=0, sticky=NW, padx=163, pady=95, ipady=200)
        self.position_scrollbar.grid(row=0, column=0, sticky=NW, padx=369, pady=95, ipady=200)
        self.department_scrollbar.grid(row=0, column=0, sticky=NW, padx=577, pady=95, ipady=200)
        self.date_scrollbar.grid(row=0, column=0, sticky=NW, padx=782, pady=95, ipady=200)

    def departments_page(self):
        self.current_page_lbl.configure(text="Текущая страница: Отделы")

        self.remove_main_page_and_employees_elements()

        # Departments
        # Set labels
        self._department_lbl.grid(row=0, column=0, sticky=NW, pady=70)
        self.city_lbl.grid(row=0, column=0, sticky=NW, pady=70, padx=206)
        self.list_employees_lbl.grid(row=0, column=0, sticky=NW, pady=70, padx=414)
        self.address_lbl.grid(row=0, column=0, sticky=NW, pady=70, padx=619)

        # Set texts
        self._department_txtbox.grid(row=0, column=0, sticky=NW, pady=95)
        self.city_txtbox.grid(row=0, column=0, sticky=NW, pady=95, padx=206)
        self.list_employees_txtbox.grid(row=0, column=0, sticky=NW, pady=95, padx=414)
        self.address_txtbox.grid(row=0, column=0, sticky=NW, pady=95, padx=619)

        # Set scrolls
        self._department_scrollbar.grid(row=0, column=0, sticky=NW, padx=163, pady=95, ipady=200)
        self.city_scrollbar.grid(row=0, column=0, sticky=NW, padx=369, pady=95, ipady=200)
        self.list_employees_scrollbar.grid(row=0, column=0, sticky=NW, padx=577, pady=95, ipady=200)
        self.address_scrollbar.grid(row=0, column=0, sticky=NW, padx=782, pady=95, ipady=200)

    def notify_error_page(self):
        self.remove_chat_elements()
        self.remove_calendar_elements()
        self.remove_calculator_frame()
        self.error_txtbox.grid(row=0, column=0, sticky=NW, padx=235, pady=70, ipady=4)
        self.error_btn.grid(row=0, column=0, sticky=NW, padx=655, pady=480)

    def chat_page(self):
        self.remove_error_elements()
        self.remove_calendar_elements()
        self.remove_calculator_frame()
        self.chat_txtbox.grid(row=0, column=0, sticky=NW, padx=235, pady=70, ipady=32)
        self.chat_scrollbar.grid(row=0, column=0, sticky=NW, padx=750, pady=70, ipady=200)
        
        for i in range(1, 10):
            self.but = Button(self.chat_txtbox, text=f"Пользователь: {i}",
                bd=0, width=73, height=4,
                bg='cornflower blue', fg='white',
                font=("Ubuntu", 9, "bold"),
                activebackground='grey25', activeforeground='grey25')
            self.chat_txtbox.window_create("end", window=self.but)
            self.chat_txtbox.insert("end", '\n\n')
        self.chat_txtbox.configure(state="disabled")

    def calendar_page(self):
        self.remove_error_elements()
        self.remove_chat_elements()
        self.remove_calculator_frame()
        self.calendar_txtbox.grid(row=0, column=0, sticky=NW, padx=235, pady=70, ipady=32)
        self.calendar_scrollbar.grid(row=0, column=0, sticky=NW, padx=750, pady=70, ipady=200)
        
        for i in range(1, 10):
            self.but = Button(self.calendar_txtbox, text=f"Новость: {i}",
                bd=0, width=73, height=4,
                bg='LightSteelBlue4', fg='white',
                font=("Ubuntu", 9, "bold"),
                activebackground='grey25', activeforeground='grey25')
            #self.but.bind('<Button-1>', self.text_and_user)
            self.calendar_txtbox.window_create("end", window=self.but)
            self.calendar_txtbox.insert("end", '\n\n')
        self.calendar_txtbox.configure(state="disabled")

    def calculator_page(self):
        self.remove_error_elements()
        self.remove_chat_elements()
        self.remove_calendar_elements()
        self.calculator_frame.grid(row=0, column=0, sticky=NW, pady=70, padx=265)

    def remove_main_page_elements(self):
        # Main page
        # Remove buttons
        self.calendar_btn.grid_remove()
        self.chat_btn.grid_remove()
        self.make_calculations.grid_remove()
        self.notify_error_btn.grid_remove()

    def remove_employees_elements(self):
        # Employees
        # Remove labels
        self.fio_lbl.grid_remove()
        self.position_lbl.grid_remove()
        self.department_lbl.grid_remove()
        self.date_lbl.grid_remove()

        # Remove texts
        self.fio_txtbox.grid_remove()
        self.position_txtbox.grid_remove()
        self.department_txtbox.grid_remove()
        self.date_txtbox.grid_remove()

        # Remove scrolls
        self.fio_scrollbar.grid_remove()
        self.position_scrollbar.grid_remove()
        self.department_scrollbar.grid_remove()
        self.date_scrollbar.grid_remove()

    def remove_departments_elements(self):
        # Departments
        # Remove labels
        self._department_lbl.grid_remove()
        self.city_lbl.grid_remove()
        self.list_employees_lbl.grid_remove()
        self.address_lbl.grid_remove()

        # Remove texts
        self._department_txtbox.grid_remove()
        self.city_txtbox.grid_remove()
        self.list_employees_txtbox.grid_remove()
        self.address_txtbox.grid_remove()

        # Remove scrolls
        self._department_scrollbar.grid_remove()
        self.city_scrollbar.grid_remove()
        self.list_employees_scrollbar.grid_remove()
        self.address_scrollbar.grid_remove()

    def remove_main_page_and_employees_elements(self):
        self.remove_main_page_elements()
        self.remove_employees_elements()

        self.remove_error_elements()
        self.remove_chat_elements()
        self.remove_calendar_elements()

    def remove_main_page_and_departments_elements(self):
        self.remove_main_page_elements()
        self.remove_departments_elements()

        self.remove_error_elements()
        self.remove_chat_elements()
        self.remove_calendar_elements()

    def remove_employyes_and_departments_elements(self):
        self.remove_employees_elements()
        self.remove_departments_elements()

        self.remove_error_elements()
        self.remove_chat_elements()
        self.remove_calendar_elements()

    def remove_chat_elements(self):
        self.chat_txtbox.grid_remove()
        self.chat_scrollbar.grid_remove()

    def remove_error_elements(self):
        self.error_txtbox.grid_remove()
        self.error_btn.grid_remove()

    def remove_calendar_elements(self):
        self.calendar_txtbox.grid_remove()
        self.calendar_scrollbar.grid_remove()

    def remove_calculator_frame(self):
        self.calculator_frame.grid_remove()

    def calculator_callback(self, var: float):
        self.input_value.insert(END, str(var))

    def calculator_actions(self, var: str):
        self.value_1 = self.input_value.get()
        self.input_value.delete(0, END)
        self.calculator_action = var

    def calculator_res(self):
        if self.input_value.get():
            self.value_2 = self.input_value.get()
            if self.calculator_action == "+":
                result: str = str(float(self.value_1) + float(self.value_2))
                self.input_value.insert(END, result)
            elif self.calculator_action == "-":
                result: str = str(float(self.value_1) - float(self.value_2))
                self.input_value.insert(END, result)
            elif self.calculator_action == "*":
                result: str = str(float(self.value_1) * float(self.value_2))
                self.input_value.insert(END, result)
            elif self.calculator_action == "/":
                result: str = str(float(self.value_1) / float(self.value_2))
                self.input_value.insert(END, result)
            self.input_value.delete(0, END)
            self.input_value.insert(0, str(result))

    def clear_value(self):
        self.calculator_action = ""
        self.value_1 = None
        self.value_2 = None
        self.input_value.delete(0, END)

    def actions_callback(self, action):
        if action == "Выход":
            remove(r"session/%s" % self.last_name)
            exit_user_data = {
                "host": self.host,
                "port": self.port,
                "last_name": self.last_name,
                "value": 0
            }
            get("http://%(host)s:%(port)i/api/user-update-active/%(last_name)s/%(value)i" % exit_user_data)
            self.root.destroy()

if __name__ == "__main__":
    CONFIG = loads(open(r"data/config.json", "r", encoding="utf-8").read())
    root = Tk()
    root.iconbitmap("./static/images/rocket.ico")
    root.title("Aero")
    root.geometry("800x550+400+120")
    root.resizable(width=False, height=False)
    root["bg"] = "grey13"

    if not path.exists(r"session"):
        mkdir(r"session")
    session = listdir(r"session")
    if session:
        Aero(root, last_name=session[0], host=CONFIG["host"], port=CONFIG["port"])
    else:
        AeroLogin(root, host=CONFIG["host"], port=CONFIG["port"])
    root.mainloop()
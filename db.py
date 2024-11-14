import sqlite3

class DataBase():
    def __init__(self, db_file): # конструктор класса
        self.connection = sqlite3.connect(db_file, check_same_thread = False)
        self.cursor = self.connection.cursor()

    def info(self, id): # функция, которая выводит готовый текст для расписания по списку id
        result = "" # переменная для конечного результата
        counter = 1 # счётчик
        with self.connection:
            for i in id:
                row = self.cursor.execute("SELECT `title`, `link` FROM `main` WHERE `id` = ?", (i,)).fetchone() # получает список названий предметов и ссылок по id
                result = result+str(counter)+". "+str(row[0])+": "+str(row[1])+"\n"
                counter+=1
        return result

    def all_teacher(self): # позволяет получить список всех преподователей
        result = "" # переменная для конечного результата
        with self.connection:
            row = self.cursor.execute("SELECT `title`, `teachers_name` FROM `main`", ()).fetchall() # получает список всех названий предметов и ФИО преподавателей
            for i in row:
                result = result+str(i[0])+": "+str(i[1])+"\n"
        return result

    def all_link(self): # позволяет получить список всех ссылок на конференции
        result = "" # переменная для конечного результата
        with self.connection:
            row = self.cursor.execute("SELECT `title`, `link` FROM `main`", ()).fetchall() # получает список всех названий предметов и ссылок на конференции
            for i in row:
                result = result+str(i[0])+": "+str(i[1])+"\n"
        return result

    def add_user(self, user_id): # добавляет user_id нового пользователя в БД
        with self.connection:
            self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id, ))

    def user_info(self, user_id): # проверяет наличие user_id пользователя в БД
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id, )).fetchall()
            return bool(len(result))

        
    def all_user_id(self): # список всех user_id в БД
        with self.connection:
            chat = self.cursor.execute("SELECT `user_id` FROM `users`", ()).fetchmany(0)
        return chat

    def schedule_update(self, id, schedule_week, schedule): # обновляет расписание в день заданый id
        with self.connection:
            try:
                if "1" in schedule_week:
                    self.cursor.execute("UPDATE `schedule` SET `schedule1` = ? WHERE id = ?", (schedule, id, ))
                    if id == 1:
                        self.cursor.execute("UPDATE `schedule` SET `schedule1-tom` = ? WHERE id = ?", (schedule, 7, ))
                    else:
                        self.cursor.execute("UPDATE `schedule` SET `schedule1-tom` = ? WHERE id = ?", (schedule, id-1, ))
                else:
                    self.cursor.execute("UPDATE `schedule` SET `schedule` = ? WHERE id = ?", (schedule, id, ))
                    if id == 1:
                        self.cursor.execute("UPDATE `schedule` SET `schedule-tom` = ? WHERE id = ?", (schedule, 7, ))
                    else:
                        self.cursor.execute("UPDATE `schedule` SET `schedule-tom` = ? WHERE id = ?", (schedule, id-1, ))
                return "Дані розкладу успішно змінино"
            except Exception as ex:
                return ex

    def info_schedule(self, schedule, id): # получает расписание из БД
        with self.connection:
            result = self.cursor.execute(f"SELECT `{schedule}` FROM `schedule` WHERE `id` = ?", (id,)).fetchall()
        return result

    def link_update(self, id, link): # обновляет ссылки на заданых id
        with self.connection:
            try: 
                self.cursor.execute("UPDATE `main` SET `link` = ? WHERE id = ?", (link, id,))
                return "Дані успішно змінено!"
            except Exception as ex:
                return ex

    def add_admin(self, user_id): # добавляет администратора
        with self.connection:
            try: 
                for i in self.cursor.execute("SELECT `user_id` FROM `users`").fetchall(): # проверка на существование такого user_id в БД
                    if i == user_id:
                        continue
                    else:
                        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id, ))
                        continue

                self.cursor.execute("UPDATE `users` SET `admin` = 1 WHERE `user_id` = ?", (user_id, ))
                return "Адміністратор успішно додано!"
            except Exception as ex:
                return ex
    
    def list_admin(self): # получает список администраторов
        res_list = []
        with self.connection:
            result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `admin` = 1").fetchall()
            for i in result:
                res_list.append(int(i[0]))
            return res_list
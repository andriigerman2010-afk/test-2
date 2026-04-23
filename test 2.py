import sqlite3

conn = sqlite3.connect("db.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, major TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS courses (course_id INTEGER PRIMARY KEY AUTOINCREMENT, course_name TEXT, instructor TEXT, cost INTEGER)")
cursor.execute("""CREATE TABLE IF NOT EXISTS student_courses (student_id INTEGER, course_id INTEGER, FOREIGN KEY(student_id) REFERENCES students (id), FOREIGN KEY(course_id) REFERENCES courses (course_id), PRIMARY KEY (student_id, course_id), courses_amount INTEGER"""")

while True:
    print("--- Menu ---")
    print("1. Додавання продуктів\n2. Додавання класичних 3. Замовлення товарів\n4. Сумарний обсяг продажів\n5. Кількість замовлень на кожного класну книгу\n6. Середній час замовлення")
    print("7. Найбільш популярна категорія товарів\n8. Загальна кількість товарів кожного категорії\n9. Оновлення цін\n10. Вийти/зберегти")

action = int(input("Виберіть дію:"))

if action == 1:
    cursor.executemany(sql="INSERT INTO courses (course_name, instructor, cost) VALUES (?, ?, ?)", seq_of_parameters=["Математика", "Petro", 30000]))
if action == 2:
    cursor.executemany(sql="INSERT INTO students (name, age, major) VALUES (?, ?, ?)", seq_of_parameters=["Vasya", 18, "Прикладна математика"]))
if action == 3:
    cursor.executemany(sql="INSERT INTO student_courses (student_id, course_id, courses_amount) VALUES(?, ?, ?)", seq_of_parameters=[(0, 0, 1)])
if action == 4:
    cursor.execute("""SELECT SUM(c.cost * sc.courses_amount) FROM student_courses sc JOIN courses c ON sc.course_id = c.course_id""")
    print(cursor.fetchone()[0])

if action == 5:
    cursor.execute("""SELECT c.course_name, COUNT(sc.student_id) FROM student_courses sc JOIN courses c ON sc.course_id = c.course_id GROUP BY c.course_id""")
    for i in cursor.fetchall():
    print(f"{i[0]}, Кількість: {i[1]}")

if action == 6:
    cursor.execute("""SELECT AVG(total) FROM SELECT SUM(c.cost * sc.courses_amount) AS total FROM student_courses sc JOIN courses c ON sc.course_id = c.course_id GROUP BY sc.student_id""")
    result = cursor.fetchone()[0]
    if result:
    print(f"Середній час: {result}")
else:
    print("Даних немає")
if action == 7:
    cursor.execute("""SELECT c.course_name, COUNT(*) FROM student_courses sc JOIN courses c ON sc.course_id = c.course_id GROUP BY c.course_id ORDER BY count(*) DESC LIMIT 1 """)
    result = cursor.fetchone()
    if result:
    print(f"Найпопулярніший курс: {result}")

else:
    print("Даних немає")

if action == 8:
    cursor.execute("""SELECT course_name, COUNT(*) FROM courses GROUP BY course_name """)
    for i in cursor.fetchall():
    print(f"{i}, Кількість: {i[0]}")

if action == 9:
    cursor.execute("""UPDATE courses SET cost = cost * 1.1 """)
    print("Сума збільшена на 10%")

if action == 10:
    save = input("Чи хочеш ти зберегти зміни?(так, ні)")
    if save.lower() == "так":
    conn.commit()
    else:
    conn.rollback()
    break
conn.close()
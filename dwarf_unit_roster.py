import sqlite3
db_name = 'dwarf_roster.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()


def clear_db():
    ''' видаляє всі таблиці '''
    open()
    query = '''DROP TABLE IF EXISTS units'''
    do(query)
    close()


def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')

    do('''CREATE TABLE IF NOT EXISTS units(
            id INTEGER PRIMARY KEY,
            unit VARCHAR,
            type VARCHAR,
            health INTEGER,
            armour INTEGER,
            leadership INTEGER,
            speed INTEGER,
            meele_attack INTEGER,
            meele_defense INTEGER,
            charge_bonus INTEGER,
            dmg_per_volley INTEGER,
            ammunition INTEGER
            )''')
    close()


def add_units():
    units = [
        ('Thorgrim Grudgebearer', 'Legendary Lord','125','8208', '85', '30','52','62','20','',''),
        ('Ungrim Ironfist', 'Legendary Lord', '5536','120','100', '32','65','50','50','',''),
        ('Belegar Ironhammer', 'Legendary Lord', '5988', '120','85', '32','60','60','30','',''),
        ('Grombrindal - The White Dwarf', 'Legendary Lord', '6620', '125','100', '32','70','45','45','',''), ######
        ('Thorek Ironbrow', 'Legendary Lord', '5424', '120','85','32','45','45','16','',''),
        ('Lord', 'Lord', '4892', '120','75','32','50','60','30','',''),
        ('Runelord', 'Lord', '4348', '120','75','32','40','40','16','',''),
        ('Halkenhaf Stonebeard', 'Unique Hero', '2780', '0','100','32','65','45','20','',''),
        ('King Lunn Ironhammer', 'Unique Hero', '2780', '0','100','32','55','50','30','',''),
        ('Dramar Hammerfist', 'Unique Hero', '3300', '0','80','32','42','32','18','60','45'),
        ('Hans Valhirrson', 'Unique Hero', '2780', '0','100','32','65','50','45','',''),
        ('Throni Ironbrow', 'Unique Hero', '3300', '0','80','32','40','36','16','',''),
        ('Tom Phillipson', 'Unique Hero', '3908', '120','72','32','38','30','14','50','60'),
        ('Thane', 'Hero', '4168', '120','70','32','50','55','30','',''),
        ('Runesmith', 'Hero', '3908', '120','70','32','40','30','16','',''),
        ('Master Engineer', 'Hero', '3908', '120','72','32','38','30','14','60','50'),
        ('Miner', 'Infantry', '7600', '80','68','28','20','18','12','',''),
        ('Miner(blast charges)', 'Infantry', '7600', '80','68','28','20','18','12','3','1'),
        ('Dawi Warriors', 'Infantry', '7800', '85','70','28','22','40','12','',''),
        ('Dawi Warriors(great weapons)', 'Infantry', '7800', '85','70','28','24','30','12','',''),
        ('Slayers', 'Infantry', '8640', '0','100','40','38','42','26','',''),
        ('Longbeards', 'Infantry', '8600', '100','80','26','30','48','10','',''),
        ('Longbeards(great weapons)', 'Infantry', '8600', '100','80','26','30','38','18','',''),
        ('Hammerers', 'Infantry', '10000', '100','80','28','46','38','24','',''),
        ('Ironbreakers', 'Infantry', '9600', '125','85','26','34','66','8','',''),
        ('Giant slayers', 'Infantry', '118', '0','100','40','48','48','34','',''),
        ('Quarrellers', 'Missile Infantry', '5600', '80','64','28','18','28','4','18','18'),
        ('Quarrellers(great weapons)', 'Missile Infantry', '5600', '80','64','28','24','22','16','18','18'),
        ('Thunderers', 'Missile Infantry', '5680', '80','64','28','20','28','4','5','22'),
        ('Irondrakes', 'Missile Infantry', '3584', '125','85','26','20','27','6','32','100'),
        ('Irondrakes(Trollhammer Torpedoes)', 'Missile Infantry', '3584', '125','85','26','20','27','6','28','18'),
        ('Rangers', 'Missile Infantry', '5440', '40','60','33','18','26','4','18','18'),
        ('Rangers(Great Weapons)', 'Missile Infantry', '5440', '40','60','33','22','20','16','6','12'),
        ("Bugman's Rangers", 'Missile Infantry', '6400', '40','75','33','24','38','10','18','20'),
        ('Gyrocopters', 'War Machine', '3772', '100','64','105','30','6','25','12','22'),
        ('Gyrocopters(brimstone guns)', 'War Machine', '3772', '100','64','105','30','6','25','28','18'),
        ('Gyrobombers', 'War Machine', '3125', '100','64','90','40','4','30','88','230'),
        ('Grudgethrowers', 'Artillery', '4576', '40','64','20','16','20','2','30','22'),
        ('Cannons', 'Artillery', '4476', '40','64','20','16','20','2','84','22'),
        ('Organ Guns', 'Artillery', '4476', '40','64','20','16','20','2','80','24'),
        ('Flame Cannons', 'Artillery', '4476', '40','64','25','16','20','2','260','25')
    ]
    open()
    cursor.executemany('''INSERT INTO units (unit, type, health, armour, leadership, speed, meele_attack, meele_defense, charge_bonus, dmg_per_volley, ammunition) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', units)
    conn.commit()
    close()


# отримання даних з бази даних, з можливістю сортування на основі вказаних параметрів
#sort_column: параметр, що вказує, за яким стовпцем потрібно виконати сортування (за замовчуванням None, тобто без сортування).
#sort_order: параметр, що вказує порядок сортування ('asc' — за зростанням, 'desc' — за спаданням). Значення за замовчуванням — 'asc'.
def get_data(sort_column=None, sort_order='asc'):
    open()
    # Запит на вибір усіх даних з таблиці units
    query = "SELECT * FROM units"
    # Перевіряється, чи вказаний стовпець для сортування. Якщо так, то код далі обробляє сортування
    if sort_column is not None:
        try:
            # Спроба перетворити sort_column на ціле число і додає 1 до значення, 
            # оскільки SQLite використовує 1-індексацію (перше значення має індекс 1, а не 0)
            column_index = int(sort_column) + 1  # SQLite використовує 1-індексацію
            #Визначається, яке ім'я стовпця відповідає вибраному індексу, де індекс 1 відповідає стовпцю id, індекс 2 — стовпцю unit і так далі до 12
            match column_index:
                case 1:
                    column_name = "id"
                case 2:
                    column_name = "unit"
                case 3:
                    column_name = "type"
                case 4:
                    column_name = "health"
                case 5:
                    column_name = "armour"
                case 6:
                    column_name = "leadership"
                case 7:
                    column_name = "speed"
                case 8:
                    column_name = "meele_attack"
                case 9:
                    column_name = "meele_defense"
                case 10:
                    column_name = "charge_bonus"
                case 11:
                    column_name = "dmg_per_volley"
                case 12:
                    column_name = "ammunition"
            # Перевіряється, чи знаходиться column_index у діапазоні від 1 до 12 (це гарантує, що вибрано дійсне значення стовпця).
            # Якщо це так, до базового запиту query додається умова ORDER BY, 
            # щоб відсортувати результати відповідно до вибраного стовпця і порядку (зростання або спадання).
            if 1 <= column_index <= 12: 
                query += f" ORDER BY {column_name} {sort_order}"
        # Якщо перетворення sort_column на ціле число не вдається (наприклад, якщо передано некоректне значення), 
        # функція просто пропускає цю частину коду, не додаючи жодного сортування до запиту.
        except ValueError:
            pass 
    cursor.execute(query)
    data = cursor.fetchall()
    close()
    return data
    

def main():
    clear_db()
    create()
    add_units()

if __name__ == "__main__":
    main()
import datetime


def date(kun, oy, yil, soat, minut):
    try:
        print(datetime.datetime(yil, oy, kun, soat, minut))
        return True
    except Exception as exp:
        print(exp)
        return False


print(date(12, 12, 2023, 15, 58))
print(date(78, 12, 1, 25, 68))
print(date(7, "Yanvar", "2023-yil", 10, 00))



class Logging:
    """
    info - контроль работы
    warning - поломка чаще связанная с некачественными данными
    error - поломка глобально проблема с кодом
    """

    @staticmethod
    def info(catch_error):
        with open('logs/app.log', 'a', encoding='UTF-8') as f:
            f.write(f" -INFO- {catch_error}\n")
        print(f" -INFO- {catch_error}")

    @staticmethod
    def warning(catch_error):
        with open('logs/app.log', 'a', encoding='UTF-8') as f:
            f.write(f" -WARNING- {catch_error}\n")
        print(f" -WARNING- {catch_error}")

    @staticmethod
    def error(catch_error):
        with open('logs/app.log', 'a', encoding='UTF-8') as f:
            f.write(f" -ERROR- {catch_error}\n")
        print(f" -ERROR- {catch_error}")

from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


"""
    def __get_config(self) -> dict:
     parser = ConfigParser()
     parser.read('../database.ini')
     config = {}
     if parser.has_section('postgresql'):
         params = parser.items('postgresql')
         for param in params:
             config[param[0]] = param[1]

     else:
         raise ConfigException
             #('Секция postgresql не найдена в database.ini')

     return config
     """

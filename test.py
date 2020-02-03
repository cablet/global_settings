

from global_settings import GlobalSettings




def one():
    x = GlobalSettings()
    x.load_file("test_data.json")
    print(x.dict())

def two():
    y = GlobalSettings()
    print(y.dict())


one()
two()



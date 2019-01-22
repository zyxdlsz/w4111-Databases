import data_service

def test1():
    result = data_service.retrieve_by_primary_key('People', ['willite01'])
    print("test1 result = ", result)

test1()

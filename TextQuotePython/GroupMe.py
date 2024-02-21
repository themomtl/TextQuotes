from groupy import Client
c = Client.from_token(
        'CbxaV0Qczv3ahCaK0nagt73fJI4pgrjpRA1O8puc')
def GroupMe(chatName, message):
    listOfGroups = list(c.groups.list_all())
    for group in listOfGroups:
        if group.name == chatName:
            group.post(message)



GroupMe('Quotes','and this')
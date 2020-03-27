import vk_api
import random

def write_msg(user_id, msg):
    vk.method('messages.send', {'user_id':user_id, 'message':msg, 'random_id': random.randint(-9999999999999, 9999999999)})

try:
    login = input('Enter VK login: ')
    password = input('Enter VK password: ')
    message = input('Enter message for autoresponding: ')

    app_id='2685278' # Kate Mobile App ID (messages.send bypass)

    try:
        vk = vk_api.VkApi(login, password, app_id=app_id)
        vk.auth()
    except vk_api.exceptions.BadPassword:
        print('Bad password!'); exit()
    except vk_api.exceptions.AuthError:
        vk = vk_api.VkApi(login, password, app_id=app_id, auth_handler=lambda:[input('Enter two-factor auth code: '), False])
        vk.auth()

    values = {'count': 100, 'filter': 'unread'}

    while True:
        response = vk.method('messages.getConversations', values)
        if response['items']:
            values['last_message_id'] = response['items'][0]['conversation']['peer']['id']
        for item in response['items']:
            write_msg(item['conversation']['peer']['id'],message)
except KeyboardInterrupt:
    print('Goodbye :D'); exit()

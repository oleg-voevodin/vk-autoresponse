import vk_api
import random

def write_msg(user_id, msg):
    vk.method('messages.send', {'user_id':user_id, 'message':msg, 'random_id': random.randint(-9999999999999, 9999999999)})

try:
    login = input('Enter VK login: ')
    password = input('Enter VK password: ')

    app_id='2685278' # Kate Mobile App ID (messages.send bypass)

    try:
        vk = vk_api.VkApi(login, password, app_id=app_id)
        vk.auth()
    except vk_api.exceptions.BadPassword:
        print('Bad password!'); exit()
    except vk_api.exceptions.AuthError:
        vk = vk_api.VkApi(login, password, app_id=app_id, auth_handler=lambda:[input('Enter two-factor auth code: '), False])
        vk.auth()

    message = input('Enter message for autoresponsing: ')

    values = {'count': 100, 'filter': 'unread'}

    need_for_answer = []

    while True:
        response = vk.method('messages.getConversations', values)
        if response['items']:
            values['last_message_id'] = response['items'][0]['conversation']['peer']['id']
            if response['items'][0]['conversation']['peer']['id'] not in need_for_answer:
                need_for_answer.append(response['items'][0]['conversation']['peer']['id'])
        for item in response['items']:
            write_msg(item['conversation']['peer']['id'],message)
        vk.method('account.setOnline')
except KeyboardInterrupt:
    print('Stopped.')
    for k in need_for_answer:
        first_name = vk.method('users.get', {'user_ids':k})[0]['first_name']
        last_name = vk.method('users.get', {'user_ids': k})[0]['last_name']
        print(f'You need answer to {first_name} {last_name}.')
    print('Goodbye :D'); exit()

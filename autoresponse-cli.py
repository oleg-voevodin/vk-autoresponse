from datetime import datetime
import vk_api
import random
import time
import os

try:
    if os.path.exists('vk_config.v2.json'):
        if os.name == 'nt':
            os.system('del vk_config.v2.json')
        else:
            os.system('rm vk_config.v2.json')
    is_data_entered = False
    login = input('Enter VK login: ')
    password = input('Enter VK password: ')
    app_id='2685278' # Kate Mobile App ID (messages.send bypass)

    try:
        vk = vk_api.VkApi(login, password, app_id=app_id)
        vk.auth()
    except vk_api.exceptions.LoginRequired:
        print('Login is required!'); exit()
    except vk_api.exceptions.PasswordRequired:
        print('Password is required!'); exit()
    except vk_api.exceptions.BadPassword:
        print('Bad password!'); exit()
    except vk_api.exceptions.Captcha:
        print('Wait a little and try again.'); exit()
    except vk_api.exceptions.AuthError:
        vk = vk_api.VkApi(login, password, app_id=app_id, auth_handler=lambda:[input('Enter two-factor auth code: '), False])
        vk.auth()

    message = input('Enter message for autoresponsing: ')

    is_data_entered = True

    values = {'count': 100, 'filter': 'unread'}

    need_for_answer = []

    status = vk.method('status.get')['text']

    while True:
        response = vk.method('messages.getConversations', values)
        if response['items']:
            values['last_message_id'] = response['items'][0]['conversation']['peer']['id']
            if response['items'][0]['conversation']['peer']['id'] not in need_for_answer:
                need_for_answer.append(dict(peer_id=response['items'][0]['conversation']['peer']['id'], peer_type=response['items'][0]['conversation']['peer']['type']))
        for item in response['items']:
            # VK have 3 types of chats, depends from chat object: 
            # 'user' - vk user
            # 'chat' - vk chat (multiusers conversation)
            # 'group' - vk group (chat with group)

            if item['conversation']['peer']['type'] == 'user': 
                vk.method('messages.send', {'user_id': item['conversation']['peer']['id'], 'message': message, 'random_id': random.randint(-999999999, 999999999)})
            elif item['conversation']['peer']['type'] == 'chat':
                vk.method('messages.send', {'peer_id': item['conversation']['peer']['id'], 'message': message, 'random_id': random.randint(-999999999, 999999999)})
            elif item['conversation']['peer']['type'] == 'group':
                vk.method('messages.send', {'peer_id': item['conversation']['peer']['id'], 'message': message, 'random_id': random.randint(-999999999, 999999999)})
        vk.method('account.setOnline')
        vk.method('status.set', {'text': f'[{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}] Autoresponse by Oleg Voevodin is working on this account.'})
        time.sleep(3)
except KeyboardInterrupt:
    if is_data_entered:
        print('Stopped.')
        vk.method('status.set', {'text': status})
        print('Status restored.')
        if len(need_for_answer) != 0:
            for k in need_for_answer:
                if k['peer_type'] == 'user':
                    first_name = vk.method('users.get', {'user_ids':k['peer_id']})[0]['first_name']
                    last_name = vk.method('users.get', {'user_ids': k['peer_id']})[0]['last_name']
                    print(f'You need answer to {first_name} {last_name}.')
                elif k['peer_type'] == 'chat':
                    chat_title = vk.method('messages.getConversationsById', {'peer_ids': k['peer_id']})['items'][0]['chat_settings']['title']
                    print(f'You need answer in \'{chat_title}\' chat.')
                elif k['peer_type'] == 'group':
                    group_title = vk.method('groups.getById', {'group_id': -k['peer_id']})[0]['name']
                    print(f'You need to answer for \'{group_title}\' group.')

        else:
            print('You have no unanswered messages.')
        print('Goodbye :D'); input('<Press Enter for exit>\n'); exit()
    exit()

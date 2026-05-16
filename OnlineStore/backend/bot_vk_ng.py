import os

import requests
from vk_api import VkApi, VkUpload
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from dotenv import load_dotenv

from OnlineStore.backend.repositories import ProductRepo, OrderRepo
PRODUCT_REPO = ProductRepo()
ORDER_REPO = OrderRepo()

from workbook_master import create_category_groups_template, \
    create_categories_template, create_product_groups_template, create_products_template, create_drop_points_template, \
    save_doc, construct_category_groups, construct_categories, \
    construct_items, construct_drop_points, construct_item_groups, create_category_details_template, \
    construct_category_details, get_data_from_file

load_dotenv()

GROUP_ID = os.getenv('vk_group_id')
GROUP_TOKEN = os.getenv('vk_token')
API_VERSION = os.getenv('vk_api_version')
ADMIN_ID = os.getenv('vk_admin_id')

vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
settings = dict(one_time=False, inline=True)
upload = VkUpload(vk_session)

BUTTONS = [
    {'label' : 'Управление групами категорий', 'payload':{'type':'ctrl_mcgb'},'last': False},
    {'label': 'Управление категорий', 'payload': {'type': 'ctrl_mcb'},'last': False},
    {'label': 'Управление характеристиками', 'payload': {'type': 'ctrl_mcdb'},'last': False},
    {'label': 'Управление группами товаров', 'payload': {'type': 'ctrl_migb'},'last': False},
    {'label': 'Управление товарами', 'payload': {'type': 'ctrl_mpb'},'last': False},
    {'label': 'Управление пунктами вывоза', 'payload': {'type': 'ctrl_mdpb'},'last': True}
]

ACTIONS = {
    'mcgb': (
        'Группы категорий',
        create_category_groups_template,
        PRODUCT_REPO.get_category_groups,
        (
            PRODUCT_REPO.insert_category_groups,
            PRODUCT_REPO.update_category_groups
        ),
        construct_category_groups
    ),
    'mcb': (
        'Категории',
        create_categories_template,
        PRODUCT_REPO.get_categories,
        (
            PRODUCT_REPO.insert_categories,
            PRODUCT_REPO.update_categories
        ),
        construct_categories
    ),
    'mcdb': (
        'Характеристики товаров',
        create_category_details_template,
        PRODUCT_REPO.get_category_details,
        (
            PRODUCT_REPO.insert_category_details,
            PRODUCT_REPO.update_category_details
        ),
        construct_category_details
    ),
    'migb': (
        'Группы товаров',
        create_product_groups_template,
        PRODUCT_REPO.get_product_groups,
        (
            PRODUCT_REPO.insert_product_groups,
            PRODUCT_REPO.update_product_groups
        ),
        construct_item_groups
    ),
    'mpb': (
        'Товары',
        create_products_template,
        PRODUCT_REPO.get_products,
        (
            PRODUCT_REPO.insert_products,
            PRODUCT_REPO.update_products
        ),
        construct_items
    ),
    'mdpb':(
        'Пункты вывоза заказов',
        create_drop_points_template,
        ORDER_REPO.get_drop_points,
        (
            ORDER_REPO.insert_drop_points,
            ORDER_REPO.update_drop_points
        ),
        construct_drop_points
    )
}

CURRENT_STATE = {
    'action': None,
    'operation': None
}

def send_doc(user_id, mod):
    doc = upload.document_message(f'storage/doc_{mod}.xlsx', title=f'doc_{mod}.xlsx', peer_id=user_id)['doc']
    attachment = f"doc{doc['owner_id']}_{doc['id']}"

    vk.messages.send(
        peer_id=user_id,
        message=f'Таблица {ACTIONS[mod][0]}',
        attachment=attachment,
        random_id=0
    )

def construct_main_menu():
    keyboard = VkKeyboard(**settings)
    for button in BUTTONS:
        keyboard.add_callback_button(label=button['label'], color=VkKeyboardColor.SECONDARY, payload=button['payload'])
        if not button['last']:
            keyboard.add_line()
    return keyboard

def send_notification(text, user_id, url=None):
    keyboard = VkKeyboard(**settings)
    if url:
        pass
    keyboard.add_callback_button(label='Прочитано', color=VkKeyboardColor.SECONDARY, payload={'type':'dismiss'})
    vk.messages.send(
        peer_id=user_id,
        message=text,
        keyboard=keyboard.get_keyboard(),
        random_id=get_random_id()
    )


if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.obj.message
            user_id = msg['from_id']
            attachments = msg.get('attachments', [])
            text = msg.get('text', '')

            if str(user_id) != str(ADMIN_ID):
                continue

            if attachments and len(attachments) == 1:
                if CURRENT_STATE.get('action') and CURRENT_STATE.get('operation'):
                    mod = CURRENT_STATE.get('action')
                    operation = CURRENT_STATE.get('operation')
                    if attachments[0]['type'] == 'doc' and attachments[0]['doc'].get('ext') == 'xlsx':
                        url = attachments[0]['doc']['url']
                        file_name = f'upload_{mod}.xlsx'
                        file_path = f"storage/{file_name}"
                        response = requests.get(url)
                        with open(file_path, 'wb') as f:
                            f.write(response.content)

                        try:
                            msg_text, template_func, template_data_func, db_action_funcs, extruct_data_func = ACTIONS[mod]
                            if mod == 'mpb':
                                data = extruct_data_func(operation, get_data_from_file(file_name))
                            else:
                                data = extruct_data_func(get_data_from_file(file_name))
                            if operation == 'add':
                                db_action_funcs[0](data)
                                pass
                            elif operation == 'edit':
                                db_action_funcs[1](data)

                            vk.messages.send(
                                peer_id=user_id,
                                random_id=get_random_id(),
                                message="Данные успешно прошли обработку и внесены в базу!"
                            )
                            vk.messages.send(
                                peer_id=user_id,
                                random_id=get_random_id(),
                                keyboard=construct_main_menu().get_keyboard(),
                                message="Главное меню"
                            )

                            CURRENT_STATE['action'] = None
                            CURRENT_STATE['operation'] = None
                        except Exception as e:
                            vk.messages.send(
                                peer_id=user_id,
                                random_id=get_random_id(),
                                message=f"Произошла ошибка при импорте: {e}"
                            )
                    else:
                        vk.messages.send(
                            peer_id=user_id,
                            random_id=get_random_id(),
                            message="Файл должен быть в формате xlsx!"
                        )
                        continue

            if text != '':
                vk.messages.send(
                    peer_id=user_id,
                    random_id=get_random_id(),
                    keyboard=construct_main_menu().get_keyboard(),
                    message="Главное меню"
                )

        elif event.type == VkBotEventType.MESSAGE_EVENT:
            if '_' in event.object.payload.get('type'):
                operation, mod = event.object.payload.get('type').split('_')
            else:
                operation = event.object.payload.get('type')

            if operation == 'ctrl':
                msg_text = ACTIONS[mod][0]
                actions_keyboard = VkKeyboard(**settings)
                actions_keyboard.add_callback_button(label='Добавить', color=VkKeyboardColor.SECONDARY,
                                                     payload={'type': f'add_{mod}'})
                actions_keyboard.add_callback_button(label='Изменить', color=VkKeyboardColor.SECONDARY,
                                                     payload={'type': f'edit_{mod}'})
                actions_keyboard.add_line()
                actions_keyboard.add_callback_button(label='Назад', color=VkKeyboardColor.SECONDARY,
                                                     payload={'type': f'back'})

                vk.messages.edit(
                    peer_id=event.object.peer_id,
                    random_id=get_random_id(),
                    keyboard=actions_keyboard.get_keyboard(),
                    conversation_message_id=event.obj.conversation_message_id,
                    message=msg_text
                )

            elif operation == 'back':
                vk.messages.edit(
                    peer_id=event.object.peer_id,
                    random_id=get_random_id(),
                    keyboard=construct_main_menu().get_keyboard(),
                    conversation_message_id=event.obj.conversation_message_id,
                    message='Главное меню'
                )

            elif operation in ('add', 'edit'):
                if mod in ACTIONS:
                    CURRENT_STATE['action'] = mod
                    CURRENT_STATE['operation'] = operation
                    msg_text, template_func, template_data_func, db_action_funcs, extruct_data_func = ACTIONS[mod]
                    vk.messages.send(
                        user_id=event.object.user_id,
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message='Генерирую шаблон, пожалуйста подождите...'
                    )
                    doc = template_func() if operation == 'add' else template_func(template_data_func())
                    save_doc(doc, mod)
                    vk.messages.send(
                        user_id=event.object.user_id,
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message='Шаблон сгенерирован. Необходимо заполнить все ячейки в строке для успешной обработки и внесение изменений в интернет магазин.'
                    )
                    send_doc(event.object.user_id, mod)
                    vk.messages.send(
                        user_id=event.object.user_id,
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message='Перехожу в режим ожидания файла...'
                    )

            elif operation == 'dismiss':
                vk.messages.delete(
                    peer_id=event.obj.peer_id,
                    conversation_message_ids=event.obj.conversation_message_id,
                    delete_for_all=1
                )
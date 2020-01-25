import asyncio
from typing import Dict, List, Optional

from aiohttp import ClientConnectorError, ClientSession
from dotenv import dotenv_values
from telebot import TeleBot
from telebot.types import Message


env = dotenv_values().get


async def _make_request(method: str, url: str, payload: Dict) -> Optional[Dict]:
    async with ClientSession() as session:
        if method == 'get':
            async with session.get(url=url, params=payload) as resp:
                status = resp.status
                return await resp.json() if status == 200 else None
        elif method == 'post':
            async with session.post(url=url, json=payload) as resp:
                status = resp.status
                return await resp.json() if status == 201 else None
        else:
            raise NotImplementedError('bad method')


def make_request(method: str, url: str, payload: Dict = None) -> Optional[Dict]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_make_request(method=method, url=url, payload=payload))
    except ClientConnectorError as exc:
        print(exc)
        return None


def geo_request(text: str, white_list: List[str]) -> Optional[str]:
    if not text or not white_list:
        return None

    apikey = dotenv_values().get('GEO_TOKEN')
    resp = make_request(method='get', url=env('YANDEX_GEO_URL').format(apikey, text))
    if not resp:
        return None

    geo_objects = resp['response']['GeoObjectCollection']['featureMember']
    for geo_object in geo_objects:
        object_name = geo_object['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        for while_name in white_list:
            if while_name in object_name:
                return object_name
    else:
        return None


def get_white_list() -> Optional[List]:
    resp = make_request(method='get', url=env('STORAGE_URL').format('search_area'))
    if not resp:
        return None

    return [area['name'] for area in resp]


def get_history(t_user_id: int, limit: int) -> Optional[str]:
    url = env('STORAGE_URL').format('history')
    payload = {'user': t_user_id, 'page': 1, 'page_size': limit}
    resp = make_request(method='get', url=url, payload=payload)
    if not resp:
        return None

    total_count, histories = resp.get('count'), resp.get('results')
    if not total_count or not histories:
        return None

    text = [
        f'Вы совершили {total_count} поисков\n',
        f'Последние {min(limit, total_count)} штук:',
    ]
    for history in histories:
        date = history.get('date', '')[:10]
        request = history.get('request')
        result = history.get('result')
        text.append(f'{request} -> {result} ({date})')
    return '\n'.join(text)


def save_history(response: str, result: str, t_user_id: int) -> bool:
    url = env('STORAGE_URL').format('history')
    payload = {'request': response, 'result': result, 'user': str(t_user_id)}
    resp = make_request(method='post', url=url, payload=payload)
    return bool(resp)


def show_history(bot: TeleBot, message: Message, markup=None) -> None:
    text = get_history(t_user_id=message.from_user.id, limit=5) or 'No data'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


def get_geo_step(bot: TeleBot, message: Message) -> None:
    text = message.text
    geo = geo_request(text=text, white_list=get_white_list()) or 'No results'
    save_history(response=text, result=geo, t_user_id=message.from_user.id)
    bot.send_message(chat_id=message.chat.id, text=geo)

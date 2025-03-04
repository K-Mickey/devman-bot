import logging
from asyncio import sleep

import aiohttp
from aiohttp import ClientSession, ClientTimeout

logger = logging.getLogger(__name__)


async def get_devman_reviews(devman_token: str):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {devman_token}'}
    timestamp = None
    timeout = ClientTimeout(total=120)
    retry_delay = 60

    async with ClientSession(timeout=timeout) as session:
        while True:
            params = {'timestamp': timestamp} if timestamp else {}
            logger.debug(f'{params=}')

            try:
                async with session.get(url=url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_response = await response.json()
                    logger.debug(json_response)

                    match json_response['status']:
                        case 'found':
                            timestamp = json_response['last_attempt_timestamp']
                            new_attempts = json_response['new_attempts']
                            yield _parse_reviews(new_attempts)

                        case 'timeout':
                            timestamp = json_response['timestamp_to_request']
                        case _:
                            logger.error(f'Unexpected status: {json_response["status"]}')
                            await sleep(retry_delay)

            except aiohttp.ClientResponseError as e:
                logger.error(f'HTTP Error {e.status}: {e.message}')
                await sleep(retry_delay)
            except aiohttp.ClientConnectionError:
                logger.error('ConnectionError')
                await sleep(retry_delay)
            except aiohttp.ClientError as e:
                logger.error(f'Client error: {str(e)}')
                await sleep(retry_delay)
            except Exception as e:
                logger.exception(f'Unexpected error: {str(e)}')
                await sleep(retry_delay)


def _parse_reviews(reviews: list[dict]) -> list[str]:
    """
    review: {
    'submitted_at': datetime,
    'timestamp': timestamp,
    'is_negative': bool,
    'lesson_title': str,
    'lesson_url': str
    }
    """
    messages = []
    for review in reviews:
        title = review['lesson_title']
        url = review['lesson_url']
        message = f'У вас проверили работу ["{title}"]({url})\n\n'

        match review['is_negative']:
            case True:
                message += 'К сожалению, в работе нашлись ошибки.'
            case False:
                message += 'Преподавателю все понравилось, можно приступать к следующему уроку!'

        messages.append(message)

    return messages

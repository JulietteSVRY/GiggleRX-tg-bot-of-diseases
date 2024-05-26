import requests
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import re

medical_assistant_text = "Ты медицинский помощник, специализирующийся на прогнозировании диагнозов болезней на основе описания симптомов. " \
                         "На вопросы, которые не касаются симптомов болезни, ты отвечаешь, что не знаешь ответа. " \
                         "Когда тебе предоставляют описание симптомов, твоя задача — проанализировать их и предложить возможный диагноз или несколько диагнозов. " \
                         "Пожалуйста, используй свои знания медицинских симптомов и диагнозов, чтобы предложить наиболее вероятные результаты. " \
                         "Убедись, что твои ответы точны и информативны. " \
                         "Обязательно в конце сообщения говори, что нужно проконсультироваться со специалистом." \
                         "Если тебе задают вопрос, который не связан с симптомами болезни, ты должен ответить, что не знаешь."

def get_response_from_gigachat(user_history: list) -> str:
    with GigaChat(
            credentials="MmNjN2NjNDQtNGUzZi00YTA5LWI1MzYtOTk2MzEzOWY4ZjBjOjk0ODhjOTM0LWVlMjEtNGFiMi1hNTQ2LWRjZTY4MTcwYjcyZQ==",
            verify_ssl_certs=False) as giga:
        payload = Chat(
            messages=[Messages(role=MessagesRole.SYSTEM, content=medical_assistant_text)] +
                     [Messages(role=MessagesRole.USER, content=msg['content']) if msg['role'] == 'user' else Messages(role=MessagesRole.ASSISTANT, content=msg['content']) for msg in user_history],
            temperature=0.7,
            max_tokens=400,
        )
        response = giga.chat(payload)
        return response.choices[0].message.content

def get_url():
    contents = requests.get('https://api.thecatapi.com/v1/images/search').json()
    url = contents[0]['url']
    return url

def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url

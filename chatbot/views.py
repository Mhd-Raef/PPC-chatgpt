from django.shortcuts import render
from django.http import JsonResponse
from .models import Chat
from django.utils import timezone
import openai
import pyDes
from dotenv import load_dotenv
import os
import json
import random
load_dotenv()




def ask_openai(message):
    openai.api_key = json.loads(os.environ.get('API_TOKENS'))[random.randint(0, 2)]
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

def three_des(data, is_encrypt):
    """" data: String could be for encryption or decryption """
    key = pyDes.triple_des(os.environ.get('ENCRYPTION_KEY'), pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    if is_encrypt:
        text = key.encrypt(data)
    else:
        text = key.decrypt(data)
    return text


def chatbot(request):
    if request.method == 'GET':
        # reset context for first load
        Chat.objects.all().delete()

    if request.method == 'POST':
        message = request.POST.get('message')
        if message == "RESET":
            Chat.objects.all().delete()
            response = "Context deleted successfully"
        else:
            records = Chat.objects.all()
            all_context = ""
            for record in records:
                all_context = all_context + str(three_des(record.context, False), 'UTF-8') + ". "
            all_context = all_context + message
            print(all_context)
            response = ask_openai(all_context)
            context = three_des(message, True)
            chat = Chat(context=context, response=response, created_at=timezone.now())
            chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')

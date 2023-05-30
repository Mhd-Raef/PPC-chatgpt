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




def ask_openai(chatgpt_chat):
    openai.api_key = json.loads(os.environ.get('API_TOKENS'))[random.randint(0, 2)]
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=chatgpt_chat
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
            
            if not records:
                chatgpt_chat = [
                    {"role": "system", "content": "You are an helpful assistant."},
                    {"role": "user", "content": message},
                ]
            else:
                chatgpt_chat = [
                    {"role": "system", "content": "You are an helpful assistant."},
                ]
                for record in records:
                    chatgpt_chat.append({"role": "user", "content": str(three_des(record.context, False), 'UTF-8')},)
                    chatgpt_chat.append({"role": "assistant", "content": str(three_des(record.response, False), 'UTF-8')},)
                chatgpt_chat.append({"role": "user", "content": message},)

            response = ask_openai(chatgpt_chat=chatgpt_chat)
            context = three_des(message, True)
            res_enc = three_des(response, True)
            chat = Chat(context=context, response=res_enc, created_at=timezone.now())
            chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')

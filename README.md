# PPC-chatgpt
Privacy-Preserving Chat with ChatGPT 

## ENV file
You need three API_TOKENS in .ENV file and 8, 16 or 24 bytes for ENCRYPTION_KEY
An example is:
```
API_TOKENS='["sk-******", "sk-*******", "sk-*******"]'
ENCRYPTION_KEY="********"
```

## Run Commands
```
cd PPC-chatbot
python -m pip install -r requirements.txt
cd react_chatbot
npm install
npm run build
cd ..
python manage.py runserver
```

and have fun! ❤️
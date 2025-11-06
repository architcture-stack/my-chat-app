from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# ذخیره ساده پیام‌ها
messages = []

@app.route('/')
def home():
    return """
    <div style="text-align: center; font-family: Arial; padding: 50px;">
        <h1>🚀 سرور چت آنلاین فعال است!</h1>
        <p>این سرور برای اپلیکیشن چت شما ساخته شده</p>
        <p>آدرس: <strong>/api/message</strong></p>
    </div>
    """

@app.route('/api/message', methods=['POST'])
def receive_message():
    try:
        data = request.json
        user_message = data.get('message', '')
        user_type = data.get('user', 'website')
        
        print(f"📨 پیام جدید: {user_message}")
        
        # پاسخ خودکار
        reply = generate_reply(user_message)
        
        # ذخیره پیام
        messages.append({
            'user': user_type,
            'message': user_message,
            'reply': reply,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'status': 'success',
            'reply': reply,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'reply': 'متاسفانه خطایی رخ داد!'
        })

def generate_reply(message):
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['سلام', 'سلامتی', 'hello', 'hi']):
        return 'سلام! 👋 چطور می‌تونم کمک کنم؟'
    elif any(word in message_lower for word in ['قیمت', 'هزینه', 'price', 'cost']):
        return 'برای اطلاعات قیمت لطفا به بخش "محصولات" در سایت مراجعه کنید. 💰'
    elif any(word in message_lower for word in ['ساعت', 'time', 'کار', 'hours']):
        return 'ساعات کاری: 🕐 شنبه تا چهارشنبه ۸:۰۰ تا ۱۶:۰۰'
    elif any(word in message_lower for word in ['تشکر', 'ممنون', 'thanks', 'thank you']):
        return 'خواهش می‌کنم! 😊 خوشحال که تونستم کمک کنم.'
    elif any(word in message_lower for word in ['چطوری', 'حالت', 'چطوري']):
        return 'خوبم ممنون! شما چطورید؟ 🌟'
    else:
        return 'پیام شما دریافت شد! 📩 به زودی با شما تماس می‌گیریم.'

@app.route('/api/messages', methods=['GET'])
def get_all_messages():
    return jsonify({
        'total_messages': len(messages),
        'messages': messages
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

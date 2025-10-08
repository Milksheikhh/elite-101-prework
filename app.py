from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample order data
ORDERS = {
    "ORD001": {
        "items": ["Blue Denim Jacket - Size M", "White Cotton T-Shirt - Size L"],
        "total": 89.99,
        "date": "2025-10-01"
    },
    "ORD002": {
        "items": ["Black Leather Boots - Size 9", "Gray Wool Sweater - Size S"],
        "total": 149.99,
        "date": "2024-10-03"
    },
    "ORD003": {
        "items": ["Red Summer Dress - Size M", "White Sneakers - Size 8"],
        "total": 79.99,
        "date": "2024-10-05"
    },
    "ORD004": {
        "items": ["Black Formal Pants - Size 32", "Blue Button-up Shirt - Size L", "Brown Belt"],
        "total": 119.99,
        "date": "2024-10-06"
    },
    "ORD005": {
        "items": ["Pink Hoodie - Size XL", "Dark Jeans - Size 30"],
        "total": 69.99,
        "date": "2024-10-07"
    }
}

@app.route('/')
def index():
    return redirect(url_for('chat'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    chat_history = []
    
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()
        step = request.form.get('step', '1')
        customer_name = request.form.get('customer_name', '')
        order_id = request.form.get('order_id', '')
        
        if step == '1':  # Getting name
            if user_input:
                customer_name = user_input
                chat_history.append({'type': 'bot', 'message': "Welcome to Customer Service! I'm here to help you with returns and exchanges. What's your name?"})
                chat_history.append({'type': 'user', 'message': user_input})
                chat_history.append({'type': 'bot', 'message': f"Hello {user_input}! I'm here to help you with returns and exchanges. Please enter your order ID:"})
                return render_template('chat.html', chat_history=chat_history, step='2', customer_name=customer_name)
        
        elif step == '2':  # Getting order ID
            if user_input:
                chat_history.append({'type': 'bot', 'message': "Welcome to Customer Service! I'm here to help you with returns and exchanges. What's your name?"})
                chat_history.append({'type': 'user', 'message': customer_name})
                chat_history.append({'type': 'bot', 'message': f"Hello {customer_name}! I'm here to help you with returns and exchanges. Please enter your order ID:"})
                chat_history.append({'type': 'user', 'message': user_input})
                
                if user_input.upper() in ORDERS:
                    order_id = user_input.upper()
                    order = ORDERS[order_id]
                    items_list = "\n".join([f"• {item}" for item in order['items']])
                    chat_history.append({'type': 'bot', 'message': f"Great! I found your order {order_id} from {order['date']}.\n\nItems in this order:\n{items_list}\n\nHow can I help you today?\n\n1. Return an item\n2. Exchange an item\n3. Check return policy\n\nPlease enter the number of your choice:"})
                    return render_template('chat.html', chat_history=chat_history, step='3', customer_name=customer_name, order_id=order_id)
                else:
                    chat_history.append({'type': 'bot', 'message': f"I couldn't find order ID '{user_input}'. Please check your order ID and try again. Valid format example: ORD001"})
                    return render_template('chat.html', chat_history=chat_history, step='2', customer_name=customer_name)
        
        elif step == '3':  # Handling final choice
            if user_input:
                order = ORDERS[order_id]
                items_list = "\n".join([f"• {item}" for item in order['items']])
                
                chat_history.append({'type': 'bot', 'message': "Welcome to Customer Service! I'm here to help you with returns and exchanges. What's your name?"})
                chat_history.append({'type': 'user', 'message': customer_name})
                chat_history.append({'type': 'bot', 'message': f"Hello {customer_name}! I'm here to help you with returns and exchanges. Please enter your order ID:"})
                chat_history.append({'type': 'user', 'message': order_id})
                chat_history.append({'type': 'bot', 'message': f"Great! I found your order {order_id} from {order['date']}.\n\nItems in this order:\n{items_list}\n\nHow can I help you today?\n\n1. Return an item\n2. Exchange an item\n3. Check return policy\n\nPlease enter the number of your choice:"})
                chat_history.append({'type': 'user', 'message': user_input})
                
                if user_input == "1":
                    chat_history.append({'type': 'bot', 'message': "Thank you for choosing to return an item. A customer service representative will contact you within 24 hours to process your return request."})
                elif user_input == "2":
                    chat_history.append({'type': 'bot', 'message': "Thank you for choosing to exchange an item. A customer service representative will contact you within 24 hours to process your exchange request."})
                elif user_input == "3":
                    chat_history.append({'type': 'bot', 'message': "Our Return Policy:\n\n• Items can be returned within 30 days of purchase\n• Items must be in original condition with tags\n• Free returns for defective items\n• Return shipping fee applies for size/style changes\n\nThank you for reviewing our policy!"})
                else:
                    chat_history.append({'type': 'bot', 'message': "I didn't understand that. Please enter:\n1. Return an item\n2. Exchange an item\n3. Check return policy"})
                    return render_template('chat.html', chat_history=chat_history, step='3', customer_name=customer_name, order_id=order_id)
                
                return render_template('chat.html', chat_history=chat_history, step='done')
    
    # Initial load
    chat_history.append({'type': 'bot', 'message': "Welcome to Customer Service! I'm here to help you with returns and exchanges. What's your name?"})
    return render_template('chat.html', chat_history=chat_history, step='1')

if __name__ == '__main__':
    app.run(debug=True)
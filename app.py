from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL = 'https://htmwdwodxkbvadhpmsxa.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh0bXdkd29keGtidmFkaHBtc3hhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIxOTY5MjUsImV4cCI6MjA3Nzc3MjkyNX0.qdDwUegnxgmZuRioUcGdrsxjN_XK9fPkSx5qMQh6fQU'

# Initialize Supabase
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL != "YOUR_SUPABASE_URL_HERE":
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase connected successfully!")
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")


def get_order_from_db(order_id):
    """Get order from Supabase database"""
    if not supabase:
        return None
    
    try:
        response = supabase.table('orders').select('*').eq('order_id', order_id).execute()
        if response.data and len(response.data) > 0:
            order_data = response.data[0]
            return {
                'items': order_data['items'],
                'total': order_data['total'],
                'date': order_data['date'],
                'email': order_data['email']
            }
    except Exception as e:
        print(f"Error fetching order from database: {e}")
    
    return None
    

def get_all_order_ids():
    """Get all order IDs from Supabase database"""
    if not supabase:
        return []
    
    try:
        response = supabase.table('orders').select('order_id').execute()
        if response.data:
            return [order['order_id'] for order in response.data]
    except Exception as e:
        print(f"Error fetching orders from database: {e}")
    
    return []

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
                
                # Handle both typed input and button selections
                order_input = user_input.upper().strip()
                order = get_order_from_db(order_input)
                if order:
                    order_id = order_input
                    chat_history.append({'type': 'bot', 'message': f"Thank you! For security purposes, please enter the email address associated with order {order_id}:"})
                    return render_template('chat.html', chat_history=chat_history, step='2.5', customer_name=customer_name, order_id=order_id)
                else:
                    chat_history.append({'type': 'bot', 'message': f"I couldn't find order ID '{user_input}'. Please check your order ID and try again."})
                    return render_template('chat.html', chat_history=chat_history, step='2', customer_name=customer_name)
        
        elif step == '2.5':  # Verifying email
            if user_input and order_id:
                order = get_order_from_db(order_id)
                
                chat_history.append({'type': 'bot', 'message': "Welcome to Customer Service! I'm here to help you with returns and exchanges. What's your name?"})
                chat_history.append({'type': 'user', 'message': customer_name})
                chat_history.append({'type': 'bot', 'message': f"Hello {customer_name}! I'm here to help you with returns and exchanges. Please enter your order ID:"})
                chat_history.append({'type': 'user', 'message': order_id})
                chat_history.append({'type': 'bot', 'message': f"Thank you! For security purposes, please enter the email address associated with order {order_id}:"})
                chat_history.append({'type': 'user', 'message': user_input})
                
                # Verify email matches the order
                if order and user_input.lower().strip() == order['email'].lower().strip():
                    items_list = "\n".join([f"• {item}" for item in order['items']])
                    chat_history.append({'type': 'bot', 'message': f"Great! I found your order {order_id} from {order['date']}.\n\nItems in this order:\n{items_list}\n\nHow can I help you today?\n\n1. Return an item\n2. Exchange an item\n3. Check return policy\n\nPlease enter the number of your choice:"})
                    return render_template('chat.html', chat_history=chat_history, step='3', customer_name=customer_name, order_id=order_id)
                else:
                    chat_history.append({'type': 'bot', 'message': "Sorry, your email isn't associated with this order. Please try again with the correct email address:"})
                    return render_template('chat.html', chat_history=chat_history, step='2.5', customer_name=customer_name, order_id=order_id)
        
        elif step == '3':  # Handling final choice
            if user_input and order_id:
                order = get_order_from_db(order_id)
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
            else:
                # If we're in step 3 but missing data, go back to step 2
                chat_history.append({'type': 'bot', 'message': "Welcome to Customer Service! I'm here to help you with returns and exchanges. What's your name?"})
                chat_history.append({'type': 'user', 'message': customer_name})
                chat_history.append({'type': 'bot', 'message': f"Hello {customer_name}! I'm here to help you with returns and exchanges. Please enter your order ID:"})
                return render_template('chat.html', chat_history=chat_history, step='2', customer_name=customer_name)
    
    # Initial load
    chat_history.append({'type': 'bot', 'message': "Welcome to Customer Service! I'm here to help you with returns and exchanges. What's your name?"})
    return render_template('chat.html', chat_history=chat_history, step='1')

if __name__ == '__main__':
    app.run(debug=True)

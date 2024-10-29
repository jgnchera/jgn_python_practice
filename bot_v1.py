import telebot

# Replace 'YOUR_API_TOKEN' with your actual bot token
bot = telebot.TeleBot('8062140335:AAHibpblJClr8GFglfSURnXQI5GcHOQhqVs')

# Dictionary to track users who are waiting for a number input
waiting_for_number = {}

# Dictionary to track retry state per user
retry_state = {}


# Define a simple command handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi da mapla \nEthana number sollu, Athu ODD ah ila EVEN ah nu pathu soldren")
    waiting_for_number[message.chat.id] = True # Track that we are expecting a number next
    retry_state[message.chat.id] = False  # Initialize retry state

# Function to check if the input is a valid number
def is_number(text):
    try:
        int(text)  # Attempt to convert the text to an integer
        return True  # If successful, return True
    except ValueError:
        return False  # If it fails (raises ValueError), return False

# Fallback for invalid number inputs
@bot.message_handler(func=lambda message: message.chat.id in waiting_for_number and not is_number(message.text) and message.text.strip().lower()!='yes' and retry_state.get(message.chat.id, False) != False )
def handle_invalid_number(message):
    bot.reply_to(message, "yenda unta number thanada ketta, kandatha anupitu iruka!!")  # Ask for a valid number
    retry_state[message.chat.id] = True  # Set retry state to True
        
#number check function
@bot.message_handler(func=lambda message: message.chat.id in waiting_for_number and is_number(message.text))
def check_number(message):
            num = int(message.text)
            if num % 2 == 0:
                bot.reply_to(message,"ithu EVEN number uh")
            else:
                bot.reply_to(message,"ithu ODD number uh")
            
            # Ask if the user wants to check another number
            bot.send_message(message.chat.id, "innoru number check pandriya??  'yes'nu solli paaru !")
            retry_state[message.chat.id] = False  # Reset retry state


# Handler for messages with 'yes' or 'no'
@bot.message_handler(func=lambda message: message.chat.id in waiting_for_number)
def check_another(message):
    if message.text.strip().lower() == 'yes':
        bot.send_message(message.chat.id, "Super uhh, number ah sollu")
        waiting_for_number[message.chat.id] = True  # Expect a new number next
        retry_state[message.chat.id] = True  # Reset retry state
    else:
        re_try = False
        image_path = r'C:\Users\jagan\Desktop\BOT trial\imagecheck.jpg'
        with open(image_path, 'rb') as image_file:
             bot.send_photo(message.chat.id, image_file)
        bot.send_message(message.chat.id, "Punda magane, Unna number thaane ketta")
        waiting_for_number.pop(message.chat.id, None)  # Remove user from active list
        retry_state.pop(message.chat.id, None)  # Remove user from retry state




# Fallback for other messages outside the flow
@bot.message_handler(func=lambda message: message.chat.id not in waiting_for_number )
def default_response(message):
    bot.send_message(message.chat.id, "start pannumbothu /start type panni start panuda ")


# Start the bot
bot.polling()

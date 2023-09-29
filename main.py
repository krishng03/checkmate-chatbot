import openai
import sys
from random import choice
from tabulate import tabulate

openai.api_key = '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'
system_message = {"role": "system", "content": "I am a career guidance Chatbot and I have vast knowledge in psychology. I have dealt with thousands of students who are preparing for competitive examinations and can also help with teaching students the syllabus of different competitive examinations held in India for example JEE, NEET, GATE, CAT, UPSC, along with 10th, 12th, College Interviews, etc. I have deep knowledge in inspiring, motivationg students who are depressed and suicidal."}

def ask_gpt(message, messages_history):
    messages_history += [{"role": "user", "content": message}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_history
    )
    return response['choices'][0]['message']['content'], messages_history

def init_history():
    messages_history = []
    messages_history += [system_message]
    return messages_history

def check_for_depression(user_prompt):
    keywords = ["die", "suicide", "kill", "hang", "stab", "murder", "depress", "suicidal"]
    words = user_prompt.lower().split(' ')
    for word in words:
        if word in keywords:
            return True
    return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <user_prompt>")
        sys.exit(1)
    user_prompt = sys.argv[1]
    if len(sys.argv) >= 3 and sys.argv[2]:
        system_message["content"] += f" My sole responsibility is to provide assistance to {sys.argv[2]}."
    if not check_for_depression(user_prompt):
        messages_history = init_history()
        bot_message, messages_history = ask_gpt(user_prompt, messages_history)
        print(bot_message)
    else:
        suicide_list = ["Your well-being is a top priority, and it's advisable to seek support from friends, family, or mental health professionals when facing challenging times. If you ever require someone to talk to or have questions regarding mental health, please contemplate reaching out to a mental health hotline or a mental health expert for guidance. Your mental health is significant, and there are individuals and resources accessible to assist you during trying periods.", "Remember, your health and happiness are important, and it's a wise choice to seek help from loved ones or mental health experts if you're going through a difficult phase. If you ever feel the need to share or have concerns about your mental well-being, please think about getting in touch with a mental health hotline or a professional in the field. Your mental health is valuable, and there are supportive people and resources ready to assist you through challenging times.", "It's crucial to prioritize your own well-being, and it's a good idea to reach out to friends, family, or mental health professionals when you're facing tough circumstances. If you ever find yourself in need of someone to talk to or if you have any inquiries or worries about mental health, please consider contacting a mental health hotline or a mental health specialist for help. Your mental health is important, and there are individuals and resources available to provide guidance during challenging moments.", "Always remember that your well-being is significant, and it's a smart move to seek help from friends, family, or mental health professionals when you're going through a challenging period. If you ever feel the need to talk to someone or have concerns related to mental health, please consider contacting a mental health hotline or a mental health provider for assistance. Your mental health holds importance, and there are individuals and resources available to provide you with guidance during difficult times. Your personal well-being is vital, and it's a wise decision to reach out to friends, family, or mental health professionals when you're facing difficulties. If you ever feel the inclination to open up or have inquiries concerning mental health, please contemplate getting in touch with a mental health hotline or a mental health expert for support. Keep in mind that your mental health is significant, and there are people and resources ready to offer assistance during trying moments.", "Here are some resources that can help: \nThe Samaritans of India: 0800 2277 825 \nNIMHANS (National Institute of Mental Health and Neurosciences):080 2552 0500\nAASRA (Association for the Prevention of Suicide and Risk Reduction in Asia): 022 2754 6669\nYou can also chat online with a counselor at the Crisis Text Line or AASRA's website. \nIt is important to remember that you are not alone and there is help available. Please reach out for help if you are thinking about suicide."]
        print(choice(suicide_list))
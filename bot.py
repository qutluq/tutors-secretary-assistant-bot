import nltk
from nltk.stem.snowball import SnowballStemmer 
import sys
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # choose from {'0', '1', '2', '3'}
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import tflearn
import random
import json
import pickle
import logging
from Schedule import Schedule
from UserProfile import UserProfile

stemmer = SnowballStemmer(language='russian')
CODE_SCHEDULE_RESPONSE = "code_schedule_response"

def bag_of_words(s, words):

    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def ask_user_for_additional_info(user_profile):
    
    # ask user for additional info: first name, last name etc.

    printed_header = False
    for att_name, att_type in user_profile.get_attribute_names(exclude_schedule=True):
        val = user_profile._get_attribute_value(att_name)

        # if attribute value is not filled in
        if not val:

            if not printed_header:
                printed_header = True
                print('Пожалуйста введите дополнительную информацию(для отказа напишите 0):')

            att_name_hf = user_profile.get_attribute_name_hf(att_name)

            if att_type == int:
                while True:
                    val = input(f"{att_name_hf}: ")

                    if val.strip() == '0':
                        break

                    try:
                        int(val)
                        break
                    except:
                        print('Пожалуйста введите число.')

            else:
                val = input(f"{att_name_hf}: ")

            if val.strip() == '0':
                
                continue

            user_profile.update(_att_name=att_name, _att_value=val)

def choose_date(code, user_profile):

    schedule = Schedule()
    schedule.print()
    success = False
    while True:

        numbers = input("Выберите часы в которые вы хотите заниматься(укажите номера через запятую, для выхода наберите 0): ")
        
        if numbers.strip() == '0':
            break

        success, schedule_str = schedule.get_schedule(numbers)
        if success:
            print(f"Выбрано время : {schedule_str.strip('[').strip(']')}")
            user_profile.update(schedule=schedule_str)
            break
        else:
            print('Попробуйте еще раз.')
    
    if success:
        ask_user_for_additional_info(user_profile)
        user_profile.save()
        if user_profile.contact_info_set():
            return "Заявка оформлена. Мы свяжемся с вами в ближайшее время."
        else:
            return "Заявка отменена. Отсутствует контактная информация!"
    
    return code

def custom_response(code, user_profile):
    
    
    if code == CODE_SCHEDULE_RESPONSE:
        # show options using buttons
        return CODE_SCHEDULE_RESPONSE, choose_date(code, user_profile)
    
    return code, ""

def chat(user_id):
    
    user_profile = UserProfile(user_id)

    print("Бот: Я помощник преподавателя математики, чем могу вам помочь? (Чтобы закрыть чат напишите `стоп`).")
    
    while True:
        
        inp = input("Вы: ")
        if inp.lower() == 'стоп':
            print(f"Бот: До свидания!")
            break

        probabilities = model.predict([bag_of_words(inp, words)])    
        probabilities = model.predict([bag_of_words(inp, words)])[0]
        ind = np.argmax(probabilities)
        tag_probability = probabilities[ind]
        tag = labels[ind]
        
        code = ""
        if tag_probability > 0.7:
            for tg in data['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
            code, response = custom_response(random.choice(responses), user_profile)

            if code == CODE_SCHEDULE_RESPONSE:
                print(f"Бот: Если у вас не осталось вопросов, для закрытия чата наберите `стоп`.")
            elif response:
                print(f"Бот: {response}")
        else:
            
            print("Бот: Я вас не понял. Попробуйте написать по другому.")


if __name__ == "__main__":

    try:
        with open('data/intents.json', encoding="utf8") as f:

            data = json.load(f)

        with open('data/data.pickle', "rb") as f:
            words, labels, training, output = pickle.load(f)

    except Exception as e:
        logging.exception(f"Data files not found: {e}")
        sys.exit(1)

    try:
        tf.compat.v1.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)
        model = tflearn.DNN(net)
        model.load("model.tflearn/model.tflearn")
    except Exception as e:
        logging.exception(f"Neural Net not found: {e}")
        sys.exit(1)


    user_id = 4 # e.g user_id of a telegram user
    chat(user_id)

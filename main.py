#!/usr/bin/python3

import telebot
import requests

from telebot import types

from supersecret import *
from lang import *

waitingfor = []

logChatIds = [1307705984,1143193416]

model_ai = "gemini-2.5-flash"
GOOGLE_GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{model_ai}:generateContent"

def sendLogs(texxt):
	for lox in logChatIds:
		bot.send_message(chat_id=lox,text=f"получен новый лог! \n\n{texxt}")

def getAIResponse(prompt):
	if not prompt or prompt == "@s1clan_bot" or prompt == "s1clan_bot":
		prompt = "привет"

	headers = {
		"Content-Type": "application/json",
	}
	params = {
		"key": GOOGLEGEMINIAPIKEYLOLSAJHDGJ
	}
	payload = {
		"contents": [
			{
				"parts": [
					{"text": prompt}
				]
			}
		]
	}
	response = requests.post(GOOGLE_GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=30)
	response.raise_for_status()

	content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
	return content

bot = telebot.TeleBot(SUPERSECRETTOKENADJASHDJKHSKJDHK)

@bot.message_handler(content_types=['new_chat_members'])
def newmember(msg):
	for member in msg.new_chat_members:
		user_full = member.first_name

		if member.last_name:
			user_full += f" {member.last_name}"

		if member.id == bot.get_me().id:
			bot.send_message(chat_id=msg.chat.id,text=bot_join_msg)
			sendLogs(f"бот авторизован в новой беседе")
		else:
			bot.send_message(chat_id=msg.chat.id,text=user_join_msg+f"{user_full}"+user_join_msg2)
			sendLogs(f"юзер tg://user?id={member.id} (@{bot.get_chat(msg.from_user.id).username}) nickname:{user_full} зашел в беседу!")

			if not member.id in waitingfor:
				waitingfor.append(member.id)

@bot.message_handler(content_types=['left_chat_member'])
def leftmember(msg):
	member = msg.left_chat_member

	if not member:
		return

	user_full = member.first_name

	if member.last_name:
		user_full += f" {member.last_name}"

	bot.send_message(chat_id=msg.chat.id,text=user_leave_msg+f"{user_full}")
	sendLogs(f"юзер tg://user?id={member.id} (@{bot.get_chat(msg.from_user.id).username}) nickname:{user_full} ливнул с беседы!")

@bot.message_handler(commands=['add'])
def addinfo(msg):
	if msg.content_type == "text":# and msg.from_user.id in waitingfor:
		try:
			if msg.text[4] == "@":
				bot.send_message(chat_id=msg.chat.id,text=add_usage_msg,reply_to_message_id=msg.message_id)
				sendLogs(f"юзер tg://user?id={msg.from_user.id} (@{bot.get_chat(msg.from_user.id).username}) немножечка тупоц🤏🤏🤏🤏")
				return

			args = msg.text.split(" ")

			for arg in args:
				print(arg)

			nickname = args[1][:-1]
			lvl = args[2][:-1]
			name = args[3]

			bot.send_message(chat_id=msg.chat.id,text=f"📜 Вы ввели: никнейм в Калибре: {nickname}, уровень в Калибре: {lvl}, имя: {name}",reply_to_message_id=msg.message_id)
			sendLogs(f"юзер tg://user?id={msg.from_user.id} (@{bot.get_chat(msg.from_user.id).username}) ввел /add nickname:{nickname}, lvl={lvl}, name:{name}")
		except Exception as e:
			print(f"an error has occured while parsing /add: {str(e)}")
			bot.send_message(chat_id=msg.chat.id,text=add_error_msg,reply_to_message_id=msg.message_id)

@bot.message_handler(commands=['ping'])
def ping(msg):
	bot.send_message(chat_id=msg.chat.id,text=pong_msg,reply_to_message_id=msg.message_id)

@bot.message_handler(commands=['ask'])
def ai(msg):
	if msg.content_type == "text":
		botmsg = None
		try:
			botmsg = bot.send_message(chat_id=msg.chat.id,text=ask_wait_msg,reply_to_message_id=msg.message_id)
			bot.edit_message_text(chat_id=msg.chat.id,text=ask_part1+msg.text[5:]+ask_part2+getAIResponse(msg.text[5:]),message_id=botmsg.message_id)
		except Exception as e:
			bot.edit_message_text(chat_id=msg.chat.id,text=f"❌Exception!:\n\n{str(e)}",message_id=botmsg.message_id)
		#sendLogs(f"юзер tg://user?id={msg.from_user.id} (@{bot.get_chat(msg.from_user.id).username}) ввел /ask prompt:{msg.text[4:]}")

@bot.message_handler(commands=['help'])
def helpmsg(msg):
	bot.send_message(chat_id=msg.chat.id,text=help_msg,reply_to_message_id=msg.message_id)

@bot.message_handler(commands=['ds','discord','dx','dc','dw','de','discorf'])
def dslink(msg):
	bot.send_message(chat_id=msg.chat.id,text=ds_msg,reply_to_message_id=msg.message_id)

bot.infinity_polling()

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 10:01:57 2020

Modulo para enviar avisos a un grupo de Telegram
******************************************************************************
******************************************************************************

Objetivo: creamos un bot en telegram (en realidad no hace falta un bot para enviar mensajes a un grupo, pero
mola hacerlos para otras posibilidades).
Creamos el bot desde telegram con BotFather. Obtengo el token, el bot Id y el grupo ID y luego solo tenemos 
que enviar mensajes. Facil potente y chulo


@author: J3Viton

Comandos para obtener info del BOT de telegram
URL
https://api.telegram.org/bot1473252352:AAFmMaiHO7rCSycmLFfO2wa9j6iIcb-eH14/getMe
{"ok":true,"result":{"id":1473252352,"is_bot":true,"first_name":"vital_bot","username":"vital_quant_bot",
"can_join_groups":true,"can_read_all_group_messages":false,"supports_inline_queries":false}}

"""

import telegram

bot_token= '1473252352:AAFmMaiHO7rCSycmLFfO2wa9j6iIcb-eH14'
chat_id ='1473252352'  #ID del Bot
chat_id2='1343379526'  #ID de J3 Viton
chat_id3 ='-405295194' #ID Chat del grupo Vital Quant (enviando el getupdate al bot veo el historio y los ID)


bot =telegram.Bot(token=bot_token)

print(bot.get_me())

#bot.send_message(chat_id=chat_id3, text='hola, soy el primer BOT Quant. Soy un trade advisor :' )



#################################################### func_mensaje()
def telegram_send( mensaje ):
    """Estrategia basica, v0
    Trataremo
    Parámetros:
    a --   
    Devuelve:

    Excepciones:
    
    """
    
    bot.send_message(chat_id=chat_id3, text=mensaje )
    
#################################################### func_mensaje() FIN


#telegram_send('soy un robot, bot para los amigos')
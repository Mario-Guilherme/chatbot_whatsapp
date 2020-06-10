from chatbot_whats import wpp_bot
import re

bot = wpp_bot('acai_bot')
bot.train_word('treino')
bot.select_tab('Nome_do_contato')
bot.apresentation(['Bot: Olá, eu sou a Açaí_bot!','Bot: Use :: no início para falar comigo',
'Bot:Qual delícias do nosso cardápio você gostaria?'])
ultimo_texto = ''

while True:
    texto = bot.read_msg()

    if texto != ultimo_texto and re.match(r'^::',texto):
        ultimo_texto = texto
        texto = texto.replace('::','')
        texto = texto.lower()

        if (texto == 'aprender' or texto == ' aprender' or texto == 'ensinar' or texto == ' ensinar'):
             bot.learn_Word(texto,'bot: Escreva a pergunta e após o ? a resposta.','bot: Obrigado por ensinar! Agora já sei!','bot: Você escreveu algo errado! Comece novamente..')
        else:
            bot.reply(texto)
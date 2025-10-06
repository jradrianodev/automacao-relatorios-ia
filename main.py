# 1. INSTALAÇÃO DAS BIBLIOTECAS (para ambientes como Colab)
# !pip install python-telegram-bot==21.0.1 --upgrade google-generativeai nest_asyncio pytz

# 2. IMPORTS E CONFIGURAÇÕES
import os
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import nest_asyncio
from datetime import datetime
import pytz

# APLICA PATCH PARA AMBIENTES COM LOOP DE EVENTOS JÁ EM EXECUÇÃO (COMO JUPYTER/COLAB)
nest_asyncio.apply()

# --- CONFIGURE SUAS VARIÁVEIS AQUI ---
# Para segurança, é recomendado usar variáveis de ambiente (os.getenv) em produção.
# Para este template, usamos placeholders claros.
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'COLE_SEU_TOKEN_DO_TELEGRAM_AQUI')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'COLE_SUA_CHAVE_DE_API_DO_GEMINI_AQUI')
EMAIL_REMETENTE = os.getenv('EMAIL_REMETENTE', 'seu_email@gmail.com')
SENHA_REMETENTE = os.getenv('SENHA_REMETENTE', 'sua_senha_de_app_de_16_letras_aqui')
LISTA_EMAIL_DESTINATARIOS = ['destinatario1@email.com', 'destinatario2@email.com']
# -----------------------------------------

# Configurando a IA
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except Exception as e:
    print(f"Erro ao configurar a IA. Verifique sua GEMINI_API_KEY: {e}")
    model = None

# --- Funções do Bot ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de boas-vindas."""
    await update.message.reply_text('Olá! Este bot está pronto para gerar relatórios operacionais. Envie seu resumo de atividades.')

def gerar_relatorio_com_ia(resumo: str, data_atual: str) -> str:
    """Gera o relatório operacional usando o prompt definido."""
    if not model:
        return "Erro: O modelo de IA não foi inicializado corretamente."

    prompt = f"""
    Aja como um assistente de operações sênior, criando um relatório diário claro e conciso para a gestão.

    Sua missão é organizar o resumo de atividades em três seções bem definidas, usando os seguintes títulos e emojis EXATAMENTE como listados:

    ✅ **Atividades Concluídas:**
    (Liste aqui tudo o que foi finalizado e resolvido no dia)

    ⚠️ **Pontos de Atenção / Pendências:**
    (Use esta seção para problemas encontrados, itens faltantes ou tarefas que precisam de acompanhamento)

    🚀 **Próximos Passos:**
    (Liste aqui as tarefas futuras que foram planejadas ou que precisam ser iniciadas)

    Seja direto e use frases curtas em formato de lista (bullet points). O tom é de um relatório interno, rápido e eficiente. Não use parágrafos.

    Use a seguinte data e hora como referência para o relatório: {data_atual}

    Aqui está o resumo das atividades:
    '{resumo}'
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao gerar conteúdo com a IA: {e}")
        return "Erro ao gerar o relatório. Não foi possível conectar à IA."

def enviar_email(relatorio_html: str) -> bool:
    """Envia o e-mail formatado."""
    relatorio_com_titulo = "### Relatório Diário de Operações\n" + relatorio_html
    destinatarios_str = ", ".join(LISTA_EMAIL_DESTINATARIOS)
    msg = MIMEText(relatorio_com_titulo.replace('\n', '<br>'), 'html')
    msg['Subject'] = 'Relatório Diário de Operações'
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = destinatarios_str
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
            smtp_server.sendmail(EMAIL_REMETENTE, LISTA_EMAIL_DESTINATARIOS, msg.as_string())
        print("E-mail enviado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

async def processar_resumo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processa o resumo do usuário, gera o relatório e envia o e-mail."""
    fuso_horario_sp = pytz.timezone('America/Sao_Paulo')
    agora_em_sp = datetime.now(fuso_horario_sp)
    data_formatada = agora_em_sp.strftime('%d de %B de %Y, %H:%M')
    # Traduz meses para português
    meses_pt = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril',
        'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto',
        'September': 'Setembro', 'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
    }
    for mes_en, mes_pt in meses_pt.items():
        data_formatada = data_formatada.replace(mes_en, mes_pt)

    resumo_usuario = update.message.text
    await update.message.reply_text('Recebido! Gerando relatório com a IA...')
    
    relatorio_gerado = await asyncio.to_thread(gerar_relatorio_com_ia, resumo_usuario, data_formatada)
    
    print(f"Relatório Gerado:\n{relatorio_gerado}")
    await update.message.reply_text('Relatório pronto. Enviando por e-mail...')
    sucesso_envio = await asyncio.to_thread(enviar_email, relatorio_gerado)
    if sucesso_envio:
        await update.message.reply_text('Sucesso! O relatório foi enviado.')
    else:
        await update.message.reply_text('Ops! Houve um erro ao enviar o e-mail.')

def main() -> None:
    """Inicia e executa o bot."""
    if not all([TELEGRAM_TOKEN, GEMINI_API_KEY, EMAIL_REMETENTE, SENHA_REMETENTE]):
        print("ERRO: Uma ou mais variáveis de configuração (tokens, chaves, senhas) não foram definidas.")
        return

    print("Iniciando o bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_resumo))

    print("Bot iniciado com sucesso. Aguardando mensagens.")
    application.run_polling()

if __name__ == '__main__':
    main()

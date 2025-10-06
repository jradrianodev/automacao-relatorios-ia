# 1. INSTALAÇÃO DAS BIBLIOTECAS (para ambientes como Colab)
# !pip install python-telegram-bot==21.0.1 --upgrade google-generativeai nest_asyncio

# 2. IMPORTS E CONFIGURAÇÕES
import os
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import nest_asyncio

# APLICA PATCH PARA AMBIENTES COM LOOP DE EVENTOS JÁ EM EXECUÇÃO (COMO JUPYTER/COLAB)
nest_asyncio.apply()

# --- CONFIGURE SUAS VARIÁVEIS AQUI ---
# Para segurança, é recomendado usar variáveis de ambiente (os.getenv) em produção
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'COLE_SEU_TOKEN_DO_TELEGRAM_AQUI')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'COLE_SUA_CHAVE_DE_API_DO_GEMINI_AQUI')
EMAIL_REMETENTE = os.getenv('EMAIL_REMETENTE', 'seu_email@gmail.com')
SENHA_REMETENTE = os.getenv('SENHA_REMETENTE', 'sua_senha_de_app_de_16_letras_aqui')
LISTA_EMAIL_DESTINATARIOS = ['destinatario1@email.com', 'destinatario2@email.com']
# -----------------------------------------

# Configurando a IA
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- Funções do Bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de boas-vindas."""
    await update.message.reply_text('Olá! Este bot está pronto para gerar relatórios e planos de ação. Envie seu resumo de atividades.')

def gerar_relatorio_com_ia(resumo: str) -> str:
    """Gera o relatório e plano de ação usando o prompt definido."""
    prompt = f"""
    Aja como um assistente de operações sênior, altamente eficiente.
    Sua missão é criar um documento em duas partes a partir de um resumo de atividades: um Relatório Diário e um Plano de Ação.

    **PARTE 1: RELATÓRIO DIÁRIO**
    Primeiro, organize o resumo nas três seções a seguir, usando os emojis e títulos exatos:

    ✅ **Atividades Concluídas:**
    (Liste aqui tudo o que foi finalizado e resolvido no dia)

    ⚠️ **Pontos de Atenção / Pendências:**
    (Use esta seção para problemas encontrados, itens faltantes ou tarefas que precisam de acompanhamento)

    🚀 **Próximos Passos:**
    (Liste aqui as tarefas futuras que foram planejadas ou que precisam ser iniciadas)

    **PARTE 2: PLANO DE AÇÃO**
    Segundo, APÓS criar o relatório, adicione uma nova seção chamada `📋 **Plano de Ação**`.
    Nesta seção, analise os itens das seções 'Pontos de Atenção / Pendências' e 'Próximos Passos' e transforme-os em ações concretas. Para cada ação, use a seguinte estrutura:

    - **Tarefa:** [Ação específica]
    - **Responsável:** [Use "[A definir]" se não for claro]
    - **Prazo:** [Use "[A definir]" se não for claro]
    - **Status:** [Use PENDENTE ou ⚠️ EM ANDAMENTO]

    Adicione a data de hoje no final de tudo.

    Aqui está o resumo das atividades:
    '{resumo}'
    """
    try:
        response = model.generate_content(prompt)
        return "### Resumo e Plano de Ação Diário\n" + response.text
    except Exception as e:
        print(f"Erro ao gerar conteúdo com a IA: {e}")
        return "Erro ao gerar o relatório. Não foi possível conectar à IA."

def enviar_email(relatorio_html: str) -> bool:
    """Envia o e-mail formatado."""
    destinatarios_str = ", ".join(LISTA_EMAIL_DESTINATARIOS)
    msg = MIMEText(relatorio_html.replace('\n', '<br>'), 'html')
    msg['Subject'] = 'Relatório de Atividades Diárias - Portal Future Today'
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
    resumo_usuario = update.message.text
    await update.message.reply_text('Recebido! Gerando relatório com a IA...')
    relatorio_gerado = await asyncio.to_thread(gerar_relatorio_com_ia, resumo_usuario)
    print(f"Relatório Gerado:\n{relatorio_gerado}")
    await update.message.reply_text('Relatório pronto. Enviando por e-mail...')
    sucesso_envio = await asyncio.to_thread(enviar_email, relatorio_gerado)
    if sucesso_envio:
        await update.message.reply_text('Sucesso! O relatório foi enviado.')
    else:
        await update.message.reply_text('Ops! Houve um erro ao enviar o e-mail.')

def main() -> None:
    """Inicia e executa o bot."""
    print("Iniciando o bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_resumo))

    print("Bot iniciado com sucesso. Aguardando mensagens.")
    application.run_polling()

if __name__ == '__main__':
    main()

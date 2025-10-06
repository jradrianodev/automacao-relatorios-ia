# 🤖 Bot Gerador de Relatórios e Planos de Ação com IA

## 🚀 Demonstração do Projeto

![GIF de Demonstração do Bot]([LINK_PARA_SEU_GIF_AQUI])
*(Clique na imagem para ver o bot em ação: envio de resumo via Telegram e recebimento do relatório/plano de ação por e-mail.)*

## 📄 Descrição do Projeto

Este projeto consiste em uma automação inteligente desenvolvida em Python que utiliza a API do Google Gemini (Inteligência Artificial) para transformar resumos diários de atividades, enviados através do Telegram, em documentos estruturados. O bot gera um relatório operacional detalhado e, subsequentemente, um plano de ação claro, ambos entregues automaticamente por e-mail aos destinatários configurados.

O objetivo é otimizar a comunicação interna, economizar tempo na elaboração de relatórios e garantir que as pendências e próximos passos sejam organizados de forma acionável para a equipe de gestão.

## 🎯 Problema Resolvido

A necessidade de criar relatórios diários e planos de ação de forma manual é uma tarefa repetitiva que consome tempo valioso e está sujeita a variações de formato e conteúdo. Este projeto aborda diretamente esse desafio, automatizando:
* A coleta de informações (via uma interface familiar como o Telegram).
* O processamento e a formatação inteligente dos dados (com IA).
* A distribuição eficiente (por e-mail).

Isso resulta em relatórios padronizados, consistentes e entregues instantaneamente, liberando tempo para atividades mais estratégicas.

## ✨ Funcionalidades Principais

* **Entrada de Dados Simplificada:** Envio de resumos de atividades via chat do Telegram.
* **Processamento Inteligente com IA:** Utiliza a API do Google Gemini para:
    * Gerar um **Relatório Operacional** com status visual (✅ concluído, ⚠️ atenção, 🚀 próximos passos).
    * Criar um **Plano de Ação** detalhado com Tarefa, Responsável, Prazo e Status.
* **Notificação Automatizada:** Envio instantâneo dos documentos gerados por e-mail para múltiplos destinatários.
* **Configuração Flexível:** Facilmente adaptável para diferentes modelos de relatórios e planos de ação via ajuste do "prompt" da IA.
* **Compatibilidade:** Desenvolvido para funcionar em ambientes como o Google Colab, facilitando a execução.

## 🛠️ Tecnologias Utilizadas

* **Linguagem de Programação:** Python
* **Inteligência Artificial:** Google Gemini API (`google-generativeai` com modelo `models/gemini-2.5-flash`)
* **Comunicação Bot:** API do Telegram (`python-telegram-bot`)
* **Envio de E-mail:** `smtplib` e `email.mime.text` (bibliotecas padrão do Python)
* **Ambiente de Execução:** Google Colab (também configurado para execução local)

## ⚙️ Como Configurar e Rodar o Projeto

### Pré-requisitos
* Python 3.8+
* Conta Google (para Google Colab e Google AI Studio)
* Conta Telegram

### Passos
1.  **Clone o repositório:**
    ```bash
    git clone [SEU_LINK_GITHUB_AQUI]
    cd nome-do-seu-repositorio
    ```
2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Obtenha as Chaves de Acesso:**
    * **Token do Bot Telegram:** Fale com o `@BotFather` no Telegram, crie um novo bot e obtenha seu token.
    * **Chave API do Google Gemini:** Acesse o [Google AI Studio](https://aistudio.google.com/), crie um projeto e gere sua chave API.
    * **Senha de App do Google (para e-mail):** Em seu gerenciador de conta Google -> Segurança -> Senhas de app, crie uma senha de 16 caracteres para o aplicativo de e-mail (se usar Gmail).
4.  **Configure as Variáveis de Ambiente:**
    * Renomeie o arquivo `env_example.py` para `env.py` (ou crie-o).
    * Preencha `env.py` com suas chaves e e-mails:
        ```python
        TELEGRAM_TOKEN = 'SEU_TOKEN_DO_TELEGRAM'
        GEMINI_API_KEY = 'SUA_CHAVE_API_DO_GEMINI'
        EMAIL_REMETENTE = 'seu_email@gmail.com'
        SENHA_REMETENTE = 'SUA_SENHA_DE_APP_GMAIL'
        LISTA_EMAIL_DESTINATARIOS = ['gestora@empresa.com', 'seu_email_secundario@empresa.com']
        ```
    * (Alternativamente, configure diretamente no `main.py` para testes rápidos, mas a prática profissional é usar variáveis de ambiente ou um `.env`.)
5.  **Execute o Bot:**
    ```bash
    python main.py
    ```
    Ou execute diretamente no Google Colab.
6.  **Interaja via Telegram:** Envie uma mensagem para o seu bot e acompanhe o recebimento do e-mail.

## 🌟 Contribuições

Sinta-se à vontade para abrir issues para sugestões ou melhorias, ou enviar Pull Requests. Toda contribuição é bem-vinda!

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

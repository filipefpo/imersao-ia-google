# -*- coding: utf-8 -*-
"""
Sistema Multi-Agentes para Buscar Assuntos Quentes no Google e Planejar Post para LinkedIn

Este script demonstra um fluxo de agentes usando Google ADK e Google Gemini
para encontrar tendências online sobre um tópico, planejar um post para LinkedIn,
escrever um rascunho e revisá-lo.

Pré-requisitos:
1. Python instalado.
2. Bibliotecas instaladas: pip install google-genai google-adk python-dotenv
3. Google API Key obtida no Google AI Studio ou Google Cloud Platform.
4. Arquivo .env na mesma pasta com a linha: GOOGLE_API_KEY=SUA_CHAVE_AQUI
"""

# --- 0. Setup e Importações ---
import os
from datetime import date
import textwrap
import warnings
import google.generativeai as genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService # Usado para simulação local
from google.adk.tools import google_search
from google.genai import types

# Ignora avisos (opcional, para manter a saída mais limpa durante o desenvolvimento)
warnings.filterwarnings("ignore")

# Carrega variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
load_dotenv()

# Configura a API Key do Google Gemini
# Pega a chave da variável de ambiente GOOGLE_API_KEY
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("Erro: GOOGLE_API_KEY não configurada.")
    print("Por favor, crie um arquivo .env com a linha: GOOGLE_API_KEY=SUA_CHAVE_AQUI")
    # Você pode adicionar um exit() aqui se quiser parar o programa caso a chave não seja encontrada
    # exit()
else:
    print("API Key do Gemini configurada com sucesso!")

# Define o modelo Gemini a ser usado
MODEL_ID = "gemini-2.0-flash"
print(f"Usando o modelo: {MODEL_ID}")

# --- Funções Auxiliares ---

# Função para chamar um agente e obter a resposta
def call_agent(agent: Agent, message_text: str) -> str:
    """Chama um agente e retorna sua resposta final."""
    from google.adk.sessions import InMemorySessionService
    from google.adk.runners import Runner
    from google.genai import types

    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)

    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    try:
        for event in runner.run(user_id="user1", session_id="session1", new_message=content):
            if event.is_final_response():
                # Checagem se content e content.parts existem e não são None
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text is not None:
                            final_response += part.text
                            final_response += "\n"
                else:
                    # >>>>> CORRIGIDO: Mensagem de erro simplificada para evitar acessar safety_ratings <<<<<
                    print(f"⚠️ Aviso: O Agente {agent.name} retornou um conteúdo vazio ou inválido.")
                    final_response = f"Resposta do Agente {agent.name} vazia ou inválida. Não foi possível obter o conteúdo da resposta."

    except Exception as e:
        # Captura outros possíveis erros durante a execução do agente
        print(f"❌ Erro durante a execução do Agente {agent.name}: {e}")
        final_response = f"Ocorreu um erro ao executar o Agente {agent.name}. Detalhes: {e}"

    return final_response.strip() # Remove espaços extras no final

# Função para formatar texto para melhor visualização (adaptada para print)
def format_output(text):
    """Formata o texto para exibição usando print."""
    text = text.replace('•', '  *') # Formata marcadores de lista
    # Adiciona um prefixo a cada linha para simular a indentação do markdown no print
    formatted_text = "\n".join([f"> {line}" for line in text.splitlines()])
    return formatted_text

# --- Definição dos Agentes ---

# Agente 1: Buscador de Notícias/Assuntos Quentes
def agente_buscador(topico, data_de_hoje):
    """Agente que busca assuntos quentes no Google."""
    buscador = Agent(
        name="agente_buscador",
        model=MODEL_ID,
        instruction="""
        Você é um assistente de pesquisa. A sua tarefa é usar a ferramenta de busca do Google (google_search)
        para recuperar os assuntos mais comentados e relevantes (assuntos quentes) sobre o tópico abaixo.
        Foque em no máximo 5 assuntos relevantes que possam ser interessantes para um post no LinkedIn,
        com base na quantidade e no burburinho online sobre eles.
        Se um tema tiver pouca repercussão, pode ser substituído por outro que tenha mais.
        Esses assuntos relevantes devem ser atuais, de no máximo um mês antes da data de hoje.
        """,
        description="Agente que busca assuntos quentes no Google para posts do LinkedIn",
        tools=[google_search]
        )
    entrada_do_agente_buscador = f"Tópico: {topico}\nData de hoje: {data_de_hoje}"
    assuntos_quentes = call_agent(buscador, entrada_do_agente_buscador)
    return assuntos_quentes

# Agente 2: Planejador de posts para LinkedIn
def agente_planejador(topico, assuntos_buscados):
    """Agente que analisa assuntos quentes e planeja conteúdo para LinkedIn."""
    planejador = Agent(
        name="agente_planejador",
        model=MODEL_ID,
        instruction="""
        Você é um planejador de conteúdo, especialista em redes sociais, focado em LinkedIn.
        Com base na lista de assuntos quentes e relevantes que o Agente Buscador encontrou sobre o tópico:
        - Use a ferramenta de busca do Google (google_search) para encontrar mais informações sobre os temas e aprofundar seu entendimento.
        - Analise a relevância de cada assunto para o público do LinkedIn (profissionais, empresas, tecnologia, etc.).
        - Escolha o tema MAIS relevante entre eles para ser o foco do post.
        - Retorne o tema escolhido, os 3 a 5 pontos mais relevantes e interessantes sobre ele, e um plano estruturado com os tópicos principais a serem abordados no post para o LinkedIn.
        - O plano deve ser claro e conciso, pensando em um post informativo e engajador para o LinkedIn.
        """,
        description="Agente que analisa assuntos quentes e planeja o conteúdo de posts para o LinkedIn.",
        tools=[google_search]
    )
    entrada_do_agente_planejador = f"Tópico original: {topico}\nAssuntos quentes encontrados pelo buscador: {assuntos_buscados}"
    plano_do_post = call_agent(planejador, entrada_do_agente_planejador)
    return plano_do_post

# Agente 3: Redator de rascunhos para LinkedIn
def agente_redator(topico_original, plano_de_post):
    """Agente que escreve o rascunho do post para LinkedIn."""
    redator = Agent(
        name="agente_redator",
        model=MODEL_ID,
        instruction="""
        Você é um Redator Criativo especializado em criar rascunhos de posts para o LinkedIn.
        Seu objetivo é transformar o plano de post fornecido pelo Agente Planejador em um texto corrido, informativo e engajador para o LinkedIn.
        Baseie-se no 'Tema escolhido' e nos 'Pontos mais relevantes' do plano.
        Escreva um rascunho de post que:
        - Tenha um título ou gancho inicial para prender a atenção.
        - Desenvolva os pontos principais de forma clara e profissional.
        - Use uma linguagem adequada para o LinkedIn (informativa, concisa, mas que estimule a reflexão/discussão).
        - Inclua uma chamada para ação sutil (ex: "O que você pensa sobre isso?", "Deixe seu comentário!").
        - Finalize com 3 a 5 hashtags relevantes para o tema e para o LinkedIn (ex: #InteligenciaArtificial #Tecnologia #Inovacao #LinkedIn).
        Não inclua emojis excessivos, a menos que sejam muito pontuais para enfatizar algo.
        Priorize clareza e valor para o leitor profissional do LinkedIn.
        """,
        description="Agente redator de rascunhos de posts para LinkedIn, baseado em um plano.",
        tools=[]
    )
    entrada_do_agente_redator = f"Tópico original: {topico_original}\nPlano de post: {plano_de_post}"
    rascunho_gerado = call_agent(redator, entrada_do_agente_redator)
    return rascunho_gerado

# Agente 4: Revisor de qualidade para LinkedIn
def agente_revisor(topico_original, rascunho_gerado):
    """Agente que revisa a qualidade do rascunho para LinkedIn."""
    revisor = Agent(
        name="agente_revisor",
        model=MODEL_ID,
        instruction="""
        Você é um Editor e Revisor de Conteúdo meticuloso, especializado em rascunhos de posts para LinkedIn.
        Sua tarefa é revisar o rascunho de post sobre o tópico indicado, verificando:
        - Clareza e concisão: O texto é fácil de entender e direto ao ponto?
        - Correção: Não tem erros de português (gramática, ortografia)?
        - Tom: A linguagem está profissional, mas ainda assim engajadora para o público do LinkedIn?
        - Adequação: O conteúdo e o formato são apropriados para uma postagem no LinkedIn?
        Se o rascunho estiver ótimo e pronto para publicar no LinkedIn, responda APENAS a frase: 'O rascunho está ótimo e pronto para publicar no LinkedIn!'
        Caso haja problemas ou algo que possa ser melhorado, aponte-os de forma clara e sugira melhorias específicas no rascunho para deixá-lo perfeito para o LinkedIn.
        """,
        description="Agente que revisa rascunhos de posts para o LinkedIn.",
        tools=[]
    )
    entrada_do_agente_revisor = f"Tópico original: {topico_original}\nRascunho do post: {rascunho_gerado}"
    texto_revisado = call_agent(revisor, entrada_do_agente_revisor)
    return texto_revisado

# --- Fluxo Principal de Execução ---

if __name__ == "__main__":
    # Código que será executado quando você rodar o script diretamente

    data_de_hoje = date.today().strftime("%d/%m/%Y")

    print("🚀 Iniciando o Sistema de Criação de Posts para LinkedIn com 4 Agentes 🚀")

    # --- Obter o Tópico do Usuário ---
    topico = input("❓ Por favor, digite o TÓPICO sobre o qual você quer criar o post de tendências para o LinkedIn: ")

    if not topico:
        print("Você esqueceu de digitar o tópico! Encerrando.")
    else:
        print(f"\nMaravilha! Vamos criar um post sobre novidades em {topico} para o LinkedIn.")

        # 1. Buscador encontra os assuntos quentes
        print("\n--- 🕵️‍♂️ Agente Buscador em ação! Buscando assuntos quentes... ---")
        assuntos_encontrados = agente_buscador(topico, data_de_hoje)
        print("\nResultado do Buscador:")
        print(format_output(assuntos_encontrados))
        print("-" * 60) # Imprime uma linha separadora

        # 2. Planejador cria o plano
        print("\n--- 📝 Agente Planejador em ação! Criando o plano do post... ---")
        plano_gerado = agente_planejador(topico, assuntos_encontrados)
        print("\nResultado do Planejador:")
        print(format_output(plano_gerado))
        print("-" * 60)

        # 3. Redator escreve o rascunho
        print("\n--- ✍️ Agente Redator em ação! Escrevendo o rascunho... ---")
        rascunho_do_post = agente_redator(topico, plano_gerado)
        print("\nResultado do Redator:")
        print(format_output(rascunho_do_post))
        print("-" * 60)

        # 4. Revisor revisa o rascunho
        print("\n--- ✅ Agente Revisor em ação! Revisando o rascunho... ---")
        revisao_final = agente_revisor(topico, rascunho_do_post)
        print("\nResultado do Revisor:")
        print(format_output(revisao_final))
        print("-" * 60)

        print("\n🎉 Fluxo completo de criação e revisão finalizado! O texto acima é o resultado da revisão. 🎉")

        # Aqui seria o ponto para um futuro Agente Publicador
        print("\n➡️ Próximo passo (desafio extra!): Implementar um Agente Publicador para interagir com a API do LinkedIn.")
# Imersão IA Alura e Google

# 🤖 Projeto Multi-Agentes: Tendências & Posts para LinkedIn

Bem-vindo ao **Projeto Multi-Agentes para Criação de Conteúdo no LinkedIn**!  
Este projeto demonstra como a Inteligência Artificial pode automatizar todo o fluxo de criação de posts profissionais para o LinkedIn, desde a pesquisa de tendências até a revisão final do texto, utilizando Google Gemini e Google ADK.

---

## ✨ Visão Geral

O sistema é composto por **4 agentes inteligentes**, cada um responsável por uma etapa do processo:

1. **Agente Buscador:** Pesquisa os assuntos mais quentes e relevantes sobre um tópico no Google.
2. **Agente Planejador:** Analisa os temas encontrados e estrutura um plano de post para o LinkedIn.
3. **Agente Redator:** Escreve um rascunho envolvente e profissional baseado no plano.
4. **Agente Revisor:** Revisa o texto, garantindo clareza, correção e adequação ao LinkedIn.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [Google ADK](https://github.com/google/adk)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 🚀 Como Funciona

1. **Você informa um tópico de interesse.**
2. O **Agente Buscador** pesquisa tendências e assuntos quentes sobre o tema.
3. O **Agente Planejador** seleciona o melhor assunto e estrutura um plano de post.
4. O **Agente Redator** transforma o plano em um texto pronto para o LinkedIn.
5. O **Agente Revisor** garante a qualidade final do texto.

Tudo isso de forma automatizada, rápida e inteligente!

---

## 📦 Instalação

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seu-usuario/seu-repo.git
   cd imersao-ia-google
   ```

2. **Instale as dependências:**
   ```sh
   pip install google-genai google-adk python-dotenv
   ```

3. **Configure sua chave de API:**
   - Crie um arquivo `.env` na raiz do projeto com o conteúdo:
     ```
     GOOGLE_API_KEY=SUA_CHAVE_AQUI
     ```

---

## 🏃‍♂️ Como Usar

Execute o script principal:

```sh
python agentes-linkedin.py
```

Siga as instruções no terminal, informe o tópico desejado e acompanhe o fluxo dos agentes até o texto final revisado!

---

## 📚 Exemplo de Uso

```sh
❓ Por favor, digite o TÓPICO sobre o qual você quer criar o post de tendências para o LinkedIn: Inteligência Artificial
```
O sistema irá buscar tendências, planejar, redigir e revisar um post sobre o tema escolhido.

---

## 💡 Possibilidades Futuras

- Integração com a API do LinkedIn para publicação automática.
- Personalização dos agentes para outros tipos de conteúdo e redes sociais.
- Dashboard para acompanhamento dos resultados dos posts.

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Contribua!

Sinta-se à vontade para abrir issues, sugerir melhorias ou enviar pull requests. Vamos juntos impulsionar a criação de conteúdo inteligente!

---
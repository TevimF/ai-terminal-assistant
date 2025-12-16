<p align="center">
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini">
</p>

<h1 align="center">�� AI - Assistente de Terminal</h1>

<p align="center">
  <strong>Esqueceu um comando Linux? Pergunte no terminal!</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/versão-2.2-blue" alt="Versão">
  <img src="https://img.shields.io/badge/licença-MIT-green" alt="Licença">
</p>

---

## 🎬 Demo

```bash
$ ai como ver espaço em disco
❯ `df -h`: mostra o espaço em disco de forma legível.

$ ai -x liste os arquivos
❯ `ls`: lista os arquivos no diretório atual.
⚡ Comando a executar: ls
   Executar? [s/N]: s
────────────────────────────────────────
ai.py  config  README.md  scripts
────────────────────────────────────────
```

---

## ✨ Por que usar?

| ❌ Sem o AI | ✅ Com o AI |
|------------|------------|
| Abrir o navegador | `ai como fazer X` |
| Pesquisar no Google | Resposta instantânea |
| Copiar comando | `-c` copia automático |
| Voltar pro terminal | `-x` executa direto |

---

## 🚀 Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/seuuser/meu_assistente.git
cd meu_assistente

# 2. Instale a dependência
pip install google-generativeai

# 3. Configure sua API key
cp config/.env.example config/.env
nano config/.env  # Cole sua chave

# 4. Crie o alias
echo 'alias ai="python3 $(pwd)/ai.py"' >> ~/.bashrc
source ~/.bashrc

# 5. Teste!
ai oi
```

> 🔑 Pegue sua API key gratuita em: [aistudio.google.com](https://aistudio.google.com/app/apikey)

---

## 💡 Exemplos de Uso

```bash
# Perguntas simples
ai que dia é hoje
ai como atualizar o sistema

# Copiar comando para clipboard
ai -c como listar containers docker

# Executar o comando sugerido
ai -x como matar processo por nome

# Ver histórico
ai --historico

# Ver status
ai --status
```

---

## 🔌 Provedores Suportados

| Provedor | Modelo | Custo | Limites |
|----------|--------|-------|---------|
| 🟢 **Google** | gemini-2.0-flash | Grátis | 1500/dia |
| 🟢 **Groq** | llama-3.1-8b | Grátis | 14400/dia |
| 🟡 OpenAI | gpt-4o-mini | Pago | - |
| 🟡 Anthropic | claude-3-haiku | Pago | - |

Para trocar de provedor, edite `config/.env`:
```
PROVEDOR=groq
GROQ_API_KEY=sua_chave
```

---

## 📁 Estrutura

```
meu_assistente/
├── ai.py              # Script principal
├── config/
│   ├── .env           # Suas chaves (privado)
│   └── contexto.txt   # Suas preferências
├── scripts/
│   └── teste_apikey.py
└── README.md
```

---

## ⚙️ Personalização

Edite `config/contexto.txt`:
```
Minhas Preferências:
- Responda em Português Brasileiro
- Sou desenvolvedor, pode ser técnico
- Prefira dnf ou flatpak para instalações
```

---

## 📖 Documentação Completa

Veja o [TUTORIAL.md](TUTORIAL.md) para:
- Configuração avançada
- Todos os flags disponíveis
- Limites detalhados das APIs
- Changelog completo

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/melhoria`)
3. Commit suas mudanças (`git commit -m 'Adiciona melhoria'`)
4. Push para a branch (`git push origin feature/melhoria`)
5. Abra um Pull Request

---

## 📄 Licença

MIT © [Fonseca](https://github.com/seuuser)

---

<p align="center">
  Feito com ❤️ para quem vive no terminal
</p>

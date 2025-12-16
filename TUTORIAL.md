# 📖 Tutorial Completo - AI Assistente de Terminal

Este documento contém a documentação técnica completa do projeto.

---

## 📁 Estrutura do Projeto

```
meu_assistente/
├── ai.py                # 🤖 Script principal do assistente
├── config/
│   ├── .env             # 🔐 Sua API key (não compartilhar!)
│   ├── .env.example     # 📄 Exemplo de configuração
│   ├── contexto.txt     # ⚙️  Suas preferências pessoais
│   └── contexto.txt.example
├── scripts/
│   └── teste_apikey.py  # 📋 Lista modelos disponíveis na API
├── .gitignore           # 🚫 Arquivos ignorados pelo git
├── historico.log        # 📜 Histórico de consultas (auto-gerenciado)
├── README.md            # 📖 Página principal (GitHub)
└── TUTORIAL.md          # 📚 Este arquivo
```

---

## 🚀 Instalação Detalhada

### Passo 1: Dependências

```bash
# Google Gemini (padrão)
pip install google-generativeai

# OpenAI (opcional)
pip install openai

# Anthropic Claude (opcional)
pip install anthropic

# Groq - Llama/Mixtral grátis (opcional)
pip install groq
```

### Passo 2: Configurar API Key

```bash
cp config/.env.example config/.env
```

Edite `config/.env`:
```bash
# Provedor ativo: google, openai, anthropic, groq
PROVEDOR=google

# Google Gemini
GOOGLE_API_KEY=sua_chave_aqui

# OpenAI (opcional)
OPENAI_API_KEY=

# Anthropic (opcional)
ANTHROPIC_API_KEY=

# Groq (opcional)
GROQ_API_KEY=
```

### Passo 3: Criar Alias Global

Adicione ao `~/.bashrc`:
```bash
alias ai='python3 /caminho/para/meu_assistente/ai.py'
```

Depois:
```bash
source ~/.bashrc
```

### Passo 4: Configurar Preferências

Edite `config/contexto.txt`:
```
Minhas Preferências:
- Responda sempre em Português Brasileiro.
- Sou desenvolvedor, então pode ser técnico.
- Se a resposta envolver instalação, prefira 'dnf' ou 'flatpak'.
- Gosto de explicações curtas e comandos diretos.
```

---

## 🔧 Flags e Opções

| Flag | Descrição |
|------|-----------|
| `-c`, `--copiar` | Copia o comando para a área de transferência |
| `-x`, `--executar` | Pergunta se quer executar o comando |
| `--historico` | Mostra últimas consultas |
| `--status` | Mostra status do provedor e uso |
| `-n N` | Número de entradas do histórico (padrão: 10) |
| `--help` | Mostra ajuda |

---

## 📖 Exemplos de Uso

### Perguntas simples
```bash
ai que dia é hoje
ai como ver espaço em disco
ai quantos núcleos tem meu processador
```

### Copiar comando
```bash
ai -c como listar containers docker
# 📋 Comando copiado para a área de transferência!
```

### Executar comando
```bash
ai -x liste os arquivos
# ⚡ Comando a executar: ls
#    Executar? [s/N]: s
```

### Ver histórico
```bash
ai --historico
ai --historico -n 20  # últimas 20
```

### Ver status
```bash
ai --status
# 📊 Status do Assistente AI
#   Provedor:  GOOGLE
#   Modelo:    gemini-2.0-flash
#   ...
```

### Listar modelos disponíveis
```bash
python3 scripts/teste_apikey.py
```

---

## 🔌 Provedores Suportados

### Google Gemini (Padrão)
- **Modelo:** gemini-2.0-flash
- **Custo:** Grátis
- **Limites:** 15 RPM, 1500 RPD
- **API Key:** [aistudio.google.com](https://aistudio.google.com/app/apikey)

### Groq (Recomendado)
- **Modelo:** llama-3.1-8b-instant
- **Custo:** Grátis
- **Limites:** 30 RPM, 14400 RPD
- **API Key:** [console.groq.com](https://console.groq.com/)

### OpenAI
- **Modelo:** gpt-4o-mini
- **Custo:** Pago
- **API Key:** [platform.openai.com](https://platform.openai.com/api-keys)

### Anthropic
- **Modelo:** claude-3-haiku
- **Custo:** Pago
- **API Key:** [console.anthropic.com](https://console.anthropic.com/)

---

## ⚠️ Limites das APIs Gratuitas

| Provedor | Modelo | RPM | RPD | Custo |
|----------|--------|-----|-----|-------|
| Google | gemini-2.0-flash | 15 | 1500 | Grátis |
| Google | gemini-2.5-flash | 10 | 20 | Grátis |
| Groq | llama-3.1-8b | 30 | 14400 | Grátis |
| OpenAI | gpt-4o-mini | - | - | Pago |
| Anthropic | claude-3-haiku | - | - | Pago |

> **RPM** = Requisições por minuto  
> **RPD** = Requisições por dia

---

## 🔄 Como Trocar de Provedor

1. Edite `config/.env`
2. Mude `PROVEDOR=groq` (ou openai, anthropic)
3. Cole a API key correspondente
4. Teste: `ai oi`

---

## 📝 Changelog

### v2.2 (15/12/2025)
- ✅ Suporte a múltiplos provedores (Google, OpenAI, Anthropic, Groq)
- ✅ Seleção de provedor via config/.env
- ✅ Groq (Llama 3.1 grátis) como alternativa
- ✅ Flag --status para ver uso
- ✅ Extração de comandos inline (backticks)

### v2.1 (15/12/2025)
- ✅ Instrução do sistema otimizada (~80 tokens)
- ✅ Modelo trocado para gemini-2.0-flash (mais quota)
- ✅ Histórico compacto (máx 50 entradas)
- ✅ Arquivos organizados com .gitignore e .env.example

### v2.0 (15/12/2025)
- ✅ Personalidade amigável (conversa natural)
- ✅ Contexto do sistema (data, SO, diretório)
- ✅ Spinner de "pensando"
- ✅ Visual melhorado com separadores
- ✅ Carregamento de `.env` automático

### v1.0
- Versão inicial com foco em comandos Linux

---

## 🐛 Solução de Problemas

### Erro: "Limite de requisições excedido"
- Aguarde alguns segundos e tente novamente
- Ou troque para Groq (14400 req/dia grátis)

### Erro: "Chave API inválida"
- Verifique se a chave está correta em `config/.env`
- Verifique se o PROVEDOR está correto

### Comando não executa com -x
- Verifique se o modelo está retornando o comando em backticks
- Teste com `ai -x liste os arquivos`

---

**Modelo:** Configurável (Gemini, GPT, Claude, Llama)  
**Licença:** MIT

#!/usr/bin/env python3
import sys
import os
import subprocess
import datetime
import argparse
import re
import threading
import time

# --- CONFIGURAÇÃO ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(SCRIPT_DIR, "config")
CONTEXTO_FILE = os.path.join(CONFIG_DIR, "contexto.txt")
HISTORICO_FILE = os.path.join(SCRIPT_DIR, "historico.log")
DOTENV_FILE = os.path.join(CONFIG_DIR, ".env")

# Modelos padrão por provedor
MODELOS = {
    'google': 'gemini-2.0-flash',
    'openai': 'gpt-4o-mini',
    'anthropic': 'claude-3-haiku-20240307',
    'groq': 'llama-3.1-8b-instant',
}

# --- 1. CARREGAR .ENV ---
def carregar_dotenv():
    """Carrega variáveis do arquivo .env"""
    if os.path.exists(DOTENV_FILE):
        with open(DOTENV_FILE, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#") and "=" in linha:
                    chave, valor = linha.split("=", 1)
                    os.environ[chave.strip()] = valor.strip()

carregar_dotenv()

# --- 2. SELECIONAR PROVEDOR ---
PROVEDOR = os.getenv("PROVEDOR", "google").lower()
API_KEY = None

if PROVEDOR == "google":
    API_KEY = os.getenv("GOOGLE_API_KEY")
elif PROVEDOR == "openai":
    API_KEY = os.getenv("OPENAI_API_KEY")
elif PROVEDOR == "anthropic":
    API_KEY = os.getenv("ANTHROPIC_API_KEY")
elif PROVEDOR == "groq":
    API_KEY = os.getenv("GROQ_API_KEY")
else:
    print(f"❌ Provedor '{PROVEDOR}' não suportado.")
    print("   Use: google, openai, anthropic, groq")
    sys.exit(1)

if not API_KEY or len(API_KEY) < 10 or "cole_sua" in API_KEY.lower():
    print(f"❌ Erro: {PROVEDOR.upper()}_API_KEY não configurada.")
    print(f"   Edite o arquivo: {DOTENV_FILE}")
    sys.exit(1)

# --- 3. CARREGAR CONTEXTO DO USUÁRIO ---
def carregar_contexto():
    if os.path.exists(CONTEXTO_FILE):
        with open(CONTEXTO_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

# --- 4. COLETAR INFORMAÇÕES DO SISTEMA ---
def coletar_info_sistema():
    """Coleta informações do sistema operacional e ambiente"""
    info = {}
    
    # Data e hora atual
    agora = datetime.datetime.now()
    info['data_hora'] = agora.strftime("%d/%m/%Y %H:%M:%S")
    info['dia_semana'] = agora.strftime("%A")
    
    # Sistema operacional
    try:
        with open('/etc/os-release', 'r') as f:
            for linha in f:
                if linha.startswith('PRETTY_NAME='):
                    info['so'] = linha.split('=')[1].strip().strip('"')
                    break
    except:
        info['so'] = 'Linux'
    
    # Kernel
    try:
        info['kernel'] = subprocess.check_output(['uname', '-r'], text=True).strip()
    except:
        info['kernel'] = 'desconhecido'
    
    # Diretório atual
    info['pwd'] = os.getcwd()
    
    # Arquivos no diretório atual (limitado)
    try:
        arquivos = os.listdir('.')[:10]
        info['arquivos_dir'] = ', '.join(arquivos)
        if len(os.listdir('.')) > 10:
            info['arquivos_dir'] += '...'
    except:
        info['arquivos_dir'] = ''
    
    # Desktop Environment
    info['desktop'] = os.getenv('XDG_CURRENT_DESKTOP', 'desconhecido')
    
    # Session type (Wayland/X11)
    info['session'] = os.getenv('XDG_SESSION_TYPE', 'desconhecido')
    
    # Shell
    info['shell'] = os.path.basename(os.getenv('SHELL', '/bin/bash'))
    
    # Usuário
    info['usuario'] = os.getenv('USER', 'usuário')
    
    return info

# --- 4. ANIMAÇÃO DE PENSANDO ---
class Spinner:
    """Mostra uma animação enquanto processa"""
    def __init__(self):
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.running = False
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()
    
    def _animate(self):
        i = 0
        while self.running:
            print(f'\r{self.frames[i % len(self.frames)]} Pensando...', end='', flush=True)
            time.sleep(0.1)
            i += 1
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print('\r' + ' ' * 20 + '\r', end='', flush=True)  # Limpar linha

# --- 5. SALVAR NO HISTÓRICO (compacto) ---
MAX_HISTORICO = 50  # Máximo de entradas

def salvar_historico(pergunta, resposta):
    """Salva no histórico de forma compacta"""
    try:
        # Ler histórico existente
        entradas = []
        if os.path.exists(HISTORICO_FILE):
            with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
                conteudo = f.read()
            entradas = [e.strip() for e in conteudo.split('---') if e.strip()]
        
        # Criar nova entrada (compacta)
        timestamp = datetime.datetime.now().strftime("%d/%m %H:%M")
        # Resumir resposta se muito longa
        resposta_curta = resposta[:200] + "..." if len(resposta) > 200 else resposta
        resposta_curta = resposta_curta.replace('\n', ' ').strip()
        nova = f"[{timestamp}] {pergunta}\n→ {resposta_curta}"
        entradas.append(nova)
        
        # Manter apenas as últimas MAX_HISTORICO
        entradas = entradas[-MAX_HISTORICO:]
        
        # Salvar
        with open(HISTORICO_FILE, "w", encoding="utf-8") as f:
            f.write('\n---\n'.join(entradas))
    except Exception:
        pass

# --- 6. EXTRAIR COMANDO DO MARKDOWN ---
def extrair_comando(texto):
    """Extrai o primeiro bloco de código ou comando inline da resposta"""
    # Tenta bloco de código ```bash ... ```
    match = re.search(r'```(?:bash|sh|shell)?\n?(.*?)```', texto, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Tenta backtick inline `comando`
    match = re.search(r'`([^`]+)`', texto)
    if match:
        cmd = match.group(1).strip()
        # Verificar se parece comando (não é só texto)
        if cmd and not ' ' in cmd or cmd.split()[0] in ['sudo', 'dnf', 'apt', 'flatpak', 'ls', 
            'cd', 'cat', 'grep', 'find', 'chmod', 'chown', 'mkdir', 'rm', 'cp', 'mv', 
            'systemctl', 'journalctl', 'docker', 'podman', 'git', 'pip', 'python', 'echo']:
            return cmd
    
    # Tenta pegar linha que parece comando
    linhas = texto.split('\n')
    for linha in linhas:
        linha = linha.strip()
        if linha.startswith('$ '):
            return linha[2:]
        if linha and not linha.startswith('#') and not linha.startswith('*'):
            palavras_comando = ['sudo', 'dnf', 'apt', 'flatpak', 'ls', 'cd', 'cat', 'grep', 
                               'find', 'chmod', 'chown', 'mkdir', 'rm', 'cp', 'mv', 'systemctl',
                               'journalctl', 'docker', 'podman', 'git', 'pip', 'python']
            if any(linha.startswith(cmd) for cmd in palavras_comando):
                return linha
    return None

# --- 7. COPIAR PARA CLIPBOARD ---
def copiar_clipboard(texto):
    """Copia texto para a área de transferência"""
    try:
        # Tenta wl-copy (Wayland)
        subprocess.run(['wl-copy', texto], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Tenta xclip (X11)
            proc = subprocess.Popen(['xclip', '-selection', 'clipboard'], 
                                   stdin=subprocess.PIPE)
            proc.communicate(texto.encode())
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

# --- 8. EXECUTAR COMANDO ---
def executar_comando(comando):
    """Executa o comando após confirmação"""
    print(f"\n⚡ Comando a executar: {comando}")
    resposta = input("   Executar? [s/N]: ").strip().lower()
    if resposta in ['s', 'sim', 'y', 'yes']:
        print(f"\n{'─'*40}")
        os.system(comando)
        print(f"{'─'*40}\n")
        return True
    print("   Cancelado.")
    return False

# --- 9. MOSTRAR HISTÓRICO ---
def mostrar_historico(n=10):
    """Mostra as últimas N entradas do histórico"""
    if not os.path.exists(HISTORICO_FILE):
        print("📜 Histórico vazio.")
        return
    
    with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
        conteudo = f.read()
    
    entradas = [e.strip() for e in conteudo.split('---') if e.strip()]
    
    if not entradas:
        print("📜 Histórico vazio.")
        return
    
    print(f"\n📜 Últimas {min(n, len(entradas))} consultas:\n")
    for entrada in entradas[-n:]:
        print(f"  {entrada}")
        print()
    print(f"Total: {len(entradas)} consultas salvas\n")

# --- 10. MOSTRAR STATUS ---
def mostrar_status():
    """Mostra status do provedor e uso"""
    # Limites conhecidos
    limites = {
        'google': {'gemini-2.0-flash': (15, 1500), 'gemini-2.5-flash': (10, 20)},
        'openai': {'gpt-4o-mini': ('?', '?')},
        'anthropic': {'claude-3-haiku': ('?', '?')},
        'groq': {'llama-3.1-8b-instant': (30, 14400)},
    }
    
    modelo = MODELOS.get(PROVEDOR, '?')
    rpm, rpd = limites.get(PROVEDOR, {}).get(modelo, ('?', '?'))
    
    # Contar uso local (do histórico de hoje)
    uso_hoje = 0
    if os.path.exists(HISTORICO_FILE):
        hoje = datetime.datetime.now().strftime("%d/%m")
        with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
            for linha in f:
                if f"[{hoje}" in linha:
                    uso_hoje += 1
    
    print(f"""
📊 Status do Assistente AI

  Provedor:  {PROVEDOR.upper()}
  Modelo:    {modelo}
  
  Limites (tier gratuito):
    RPM: {rpm} req/min
    RPD: {rpd} req/dia
  
  Uso hoje: {uso_hoje} requisições (local)
  
  📈 Ver uso real: https://aistudio.google.com/app/usage
""")

# --- 11. PARSE DE ARGUMENTOS ---
parser = argparse.ArgumentParser(
    description='🤖 Assistente de comandos Linux com IA',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Exemplos:
  ai como listar processos
  ai -x como matar processo por nome
  ai --historico
  ai -c como atualizar sistema
    """
)
parser.add_argument('pergunta', nargs='*', help='Sua dúvida de Linux')
parser.add_argument('-x', '--executar', action='store_true', 
                    help='Perguntar se quer executar o comando')
parser.add_argument('-c', '--copiar', action='store_true',
                    help='Copiar comando para a área de transferência')
parser.add_argument('--historico', action='store_true',
                    help='Mostrar últimas consultas')
parser.add_argument('--status', action='store_true',
                    help='Mostrar status do provedor e uso')
parser.add_argument('-n', type=int, default=10,
                    help='Número de entradas do histórico (padrão: 10)')

args = parser.parse_args()

# Mostrar status se solicitado
if args.status:
    mostrar_status()
    sys.exit(0)

# Mostrar histórico se solicitado
if args.historico:
    mostrar_historico(args.n)
    sys.exit(0)

# Verificar se tem pergunta
prompt = " ".join(args.pergunta)
if not prompt:
    parser.print_help()
    sys.exit(0)

# --- 11. CONFIGURAR A "PERSONALIDADE" (otimizado) ---
contexto_usuario = carregar_contexto()
info_sistema = coletar_info_sistema()

# Instrução compacta para economizar tokens
instrucao = f"""Assistente Linux. Fedora 43, {info_sistema['desktop']}, {info_sistema['session']}.
Data: {info_sistema['data_hora']}. Dir: {info_sistema['pwd']}
REGRAS:
- PT-BR, resposta curta
- Formato: `comando` + explicação de 1 frase
- Use o comando MAIS SIMPLES. Só adicione flags se o usuário pedir explicitamente (ex: "com detalhes", "incluindo ocultos")
{contexto_usuario}"""

# --- 12. GERAR RESPOSTA ---
def gerar_resposta_google(prompt, instrucao):
    import google.generativeai as genai
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODELOS['google'], system_instruction=instrucao)
    response = model.generate_content(prompt)
    return response.text

def gerar_resposta_openai(prompt, instrucao):
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model=MODELOS['openai'],
        messages=[
            {"role": "system", "content": instrucao},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content

def gerar_resposta_anthropic(prompt, instrucao):
    from anthropic import Anthropic
    client = Anthropic(api_key=API_KEY)
    response = client.messages.create(
        model=MODELOS['anthropic'],
        max_tokens=1024,
        system=instrucao,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def gerar_resposta_groq(prompt, instrucao):
    from groq import Groq
    client = Groq(api_key=API_KEY)
    response = client.chat.completions.create(
        model=MODELOS['groq'],
        messages=[
            {"role": "system", "content": instrucao},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content

spinner = Spinner()
try:
    # Iniciar animação
    spinner.start()
    
    # Chamar provedor selecionado
    if PROVEDOR == 'google':
        resposta = gerar_resposta_google(prompt, instrucao)
    elif PROVEDOR == 'openai':
        resposta = gerar_resposta_openai(prompt, instrucao)
    elif PROVEDOR == 'anthropic':
        resposta = gerar_resposta_anthropic(prompt, instrucao)
    elif PROVEDOR == 'groq':
        resposta = gerar_resposta_groq(prompt, instrucao)
    
    # Parar animação
    spinner.stop()
    
    # Visual melhorado
    print()
    print(f"\033[36m❯\033[0m {resposta}")
    print()
    
    # Salvar no histórico
    salvar_historico(prompt, resposta)
    
    # Extrair comando
    comando = extrair_comando(resposta)
    
    if comando:
        # Copiar para clipboard se solicitado
        if args.copiar:
            if copiar_clipboard(comando):
                print("📋 Comando copiado para a área de transferência!")
            else:
                print("⚠️  Não foi possível copiar (instale wl-copy ou xclip)")
        
        # Executar se solicitado
        if args.executar:
            executar_comando(comando)

except Exception as e:
    spinner.stop()
    erro_str = str(e).lower()
    if "quota" in erro_str or "rate" in erro_str:
        print("❌ Erro: Limite de requisições excedido. Aguarde um momento.")
    elif "api_key" in erro_str or "invalid" in erro_str or "unauthorized" in erro_str:
        print(f"❌ Erro: Chave API inválida para {PROVEDOR.upper()}.")
    elif "network" in erro_str or "connection" in erro_str:
        print("❌ Erro: Sem conexão com a internet.")
    elif "no module" in erro_str:
        print(f"❌ Erro: Biblioteca do {PROVEDOR} não instalada.")
        print(f"   Execute: pip install {PROVEDOR if PROVEDOR != 'google' else 'google-generativeai'}")
    else:
        print(f"❌ Erro: {e}")

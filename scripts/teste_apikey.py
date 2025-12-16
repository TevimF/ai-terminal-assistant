#!/usr/bin/env python3
"""Lista os modelos disponíveis para sua API key do Gemini."""
import google.generativeai as genai
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "config")
DOTENV_FILE = os.path.join(CONFIG_DIR, ".env")

# Carregar .env
def carregar_dotenv():
    if os.path.exists(DOTENV_FILE):
        with open(DOTENV_FILE, "r") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#") and "=" in linha:
                    chave, valor = linha.split("=", 1)
                    os.environ.setdefault(chave.strip(), valor.strip())

carregar_dotenv()
key = os.getenv("GOOGLE_API_KEY")

if not key or len(key) < 10:
    print("❌ Erro: GOOGLE_API_KEY não configurada.")
    print(f"   Edite o arquivo: {DOTENV_FILE}")
    sys.exit(1)

try:
    genai.configure(api_key=key)
    
    # Limites conhecidos do tier gratuito (fonte: ai.google.dev/pricing)
    LIMITES_GRATIS = {
        'gemini-2.5-flash': (10, 20),
        'gemini-2.5-pro': (5, 25),
        'gemini-2.0-flash': (15, 1500),
        'gemini-2.0-flash-lite': (30, 1500),
        'gemini-1.5-flash': (15, 1500),
        'gemini-1.5-pro': (2, 50),
    }
    
    print("📋 MODELOS DISPONÍVEIS PARA SUA CHAVE\n")
    print(f"{'Modelo':<42} {'RPM':>6} {'RPD':>8}")
    print("─" * 58)
    
    found = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            nome = m.name.replace("models/", "")
            
            # Buscar limites conhecidos
            rpm, rpd = '-', '-'
            for modelo_base, limites in LIMITES_GRATIS.items():
                if nome.startswith(modelo_base):
                    rpm, rpd = limites
                    break
            
            print(f"{nome:<42} {str(rpm):>6} {str(rpd):>8}")
            found = True
    
    print("─" * 58)
    print("💡 RPM=req/min, RPD=req/dia (tier gratuito)")
    
    if not found:
        print("Nenhum modelo encontrado.")
        print("Verifique se a API 'Generative Language API' está ativada.")

except Exception as e:
    print(f"❌ Erro: {e}")

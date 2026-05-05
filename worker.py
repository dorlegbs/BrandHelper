import time
from datetime import datetime
from monitor import verificar_crise

MARCAS = ["Nike", "Adidas", "Petrobras"]
LIMITE = 20  # %

INTERVALO = 60 * 30  # 30 minutos

print("🚀 Iniciando monitoramento...\n")

while True:
    print(f"\n⏰ {datetime.now()}\n")

    for marca in MARCAS:
        variacao = verificar_crise(marca, LIMITE)
        print(f"{marca}: {variacao:+.1f}%")

    print("\n⏳ Aguardando próxima rodada...\n")
    time.sleep(INTERVALO)

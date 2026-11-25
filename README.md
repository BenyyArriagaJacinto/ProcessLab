# ProcessLab
Simulador educativo de planificación de CPU: FCFS y Round Robin. No modifica el planificador real de Linux. Una CPU, tiempos enteros, sin E/S ni coste de cambio de contexto.

## Ejecución (Python 3.8+; sin dependencias externas)
```bash
python3 main.py --algorithm fcfs
python3 main.py --algorithm rr --quantum 2
python3 main.py --algorithm rr --quantum 3 --process A:0:7 --process B:2:4
python3 -m unittest -v
```

Retorno = finalización - llegada. Espera = retorno - ráfaga. Respuesta = primer inicio - llegada.

## Procedencia
Base inicial generada con asistencia de ChatGPT. El participante debe verificarla, adaptarla y documentar sus propias decisiones. Este repositorio base no acredita revisión de Qodo ni envío al hackathon.

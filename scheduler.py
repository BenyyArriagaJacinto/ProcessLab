"""Simulador educativo de planificación de una CPU (sin coste de cambio de contexto)."""
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Process:
    pid: str
    arrival: int
    burst: int


def _validate(processes):
    if any(not isinstance(p.pid, str) or not p.pid.strip() or p.pid == 'IDLE' for p in processes):
        raise ValueError('Los identificadores deben ser texto no vacío y distintos de IDLE')
    if len({p.pid for p in processes}) != len(processes):
        raise ValueError('Los identificadores deben ser únicos')
    if any(not p.pid or p.pid == 'IDLE' or type(p.arrival) is not int or
           type(p.burst) is not int or p.arrival < 0 or p.burst <= 0 for p in processes):
        raise ValueError('PID válido, llegada entera >= 0 y ráfaga entera > 0')


def schedule(processes, algorithm='fcfs', quantum=2):
    """Devuelve segmentos (inicio, fin, PID) y métricas por proceso.

    Los empates de llegada conservan el orden de entrada. En RR las nuevas
    llegadas al fin del quantum se encolan antes del proceso desalojado.
    """
    processes = list(processes)
    _validate(processes)
    if algorithm not in ('fcfs', 'rr'):
        raise ValueError('Algoritmo desconocido')
    if algorithm == 'rr' and (type(quantum) is not int or quantum <= 0):
        raise ValueError('El quantum debe ser un entero positivo')
    pending = deque(sorted(processes, key=lambda p: p.arrival))
    ready = deque()
    remaining = {p.pid: p.burst for p in processes}
    first, finish = {}, {}
    segments = []
    t = 0
    while pending or ready:
        if not ready and pending and pending[0].arrival > t:
            segments.append((t, pending[0].arrival, 'IDLE'))
            t = pending[0].arrival
        while pending and pending[0].arrival <= t:
            ready.append(pending.popleft())
        p = ready.popleft()
        first.setdefault(p.pid, t)
        duration = remaining[p.pid] if algorithm == 'fcfs' else min(quantum, remaining[p.pid])
        segments.append((t, t + duration, p.pid))
        t += duration
        remaining[p.pid] -= duration
        while pending and pending[0].arrival <= t:
            ready.append(pending.popleft())
        if remaining[p.pid]:
            ready.append(p)
        else:
            finish[p.pid] = t
    metrics = {p.pid: {'finish': finish[p.pid], 'turnaround': finish[p.pid] - p.arrival,
                       'waiting': finish[p.pid] - p.arrival - p.burst,
                       'response': first[p.pid] - p.arrival} for p in processes}
    return segments, metrics

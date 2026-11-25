import argparse
from scheduler import Process, schedule


def main():
    parser = argparse.ArgumentParser(description='ProcessLab | Simulador de planificación')
    parser.add_argument('--algorithm', choices=['fcfs', 'rr'], default='fcfs')
    parser.add_argument('--quantum', type=int, default=2)
    parser.add_argument('--process', action='append', metavar='PID:LLEGADA:RAFAGA',
                        help='Repetir para cada proceso; si se omite, usa ejemplo')
    args = parser.parse_args()
    try:
        processes = [Process(pid, int(a), int(b)) for pid, a, b in
                     (item.split(':') for item in args.process or ['P1:0:5', 'P2:1:3', 'P3:2:1'])]
        segments, metrics = schedule(processes, args.algorithm, args.quantum)
    except ValueError as exc:
        parser.error(str(exc))
    print(f'ProcessLab | {args.algorithm.upper()} | quantum={args.quantum}' if args.algorithm == 'rr'
          else 'ProcessLab | FCFS')
    print('Gantt: ' + ' '.join(f'[{a}-{b}: {pid}]' for a,b,pid in segments))
    print(f'{"PID":<10}{"Fin":>8}{"Retorno":>10}{"Espera":>10}{"Respuesta":>12}')
    for pid, m in metrics.items():
        print(f'{pid:<10}{m["finish"]:>8}{m["turnaround"]:>10}{m["waiting"]:>10}{m["response"]:>12}')
    for key, label in [('waiting', 'Espera'), ('turnaround', 'Retorno'), ('response', 'Respuesta')]:
        print(f'{label} promedio: {sum(m[key] for m in metrics.values()) / len(metrics):.2f}')


if __name__ == '__main__':
    main()

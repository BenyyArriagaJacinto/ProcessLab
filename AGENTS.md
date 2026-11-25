# ProcessLab — agent instructions

## Project
ProcessLab is an educational Python simulator of single-CPU scheduling using FCFS and Round Robin. It models integer time, no I/O and no context-switch overhead. It is not the actual Linux scheduler.

## Setup and verification
Use Python 3.8 or later. No third-party dependencies are required. Run from the repository root:

```bash
python3 main.py --algorithm fcfs
python3 main.py --algorithm rr --quantum 2
python3 -m unittest -v
```

## Project rules

### 1. Reject invalid scheduling inputs
- Applies to: `scheduler.py`, `main.py` and input-related tests.
- Rule: require unique string process IDs containing at least one non-whitespace character (never `IDLE`), integer arrival times >= 0, positive integer bursts, and a positive integer quantum for Round Robin.
- Why: invalid inputs have no valid meaning in this model and may prevent time from advancing.

### 2. Preserve deterministic scheduling
- Applies to: `schedule()` and scheduling tests.
- Rule: keep arrival ties in input order. In Round Robin, enqueue arrivals at a quantum boundary before requeueing the interrupted process.
- Why: the same input must yield the same timeline, and boundary behavior must be explicit for teaching.

### 3. Derive metrics from execution, never from expected output
- Applies to: `scheduler.py` and metric-related output in `main.py`.
- Rule: calculate turnaround as completion minus arrival, waiting as turnaround minus burst, and response as first start minus arrival. Never hard-code a sample result.
- Why: plausible-looking output is not proof of a correct scheduling algorithm.

### 4. Test changes before accepting them
- Applies to: every change affecting behavior in `scheduler.py` or `main.py`.
- Rule: add or update relevant tests and run the full unittest suite. Include edge cases when relevant; do not claim a passing run without executing it.
- Why: automated checks help detect regressions and document expected behavior.

### 5. Keep the simulator portable and educational
- Applies to: the entire repository.
- Rule: use the Python standard library unless an external dependency is explicitly justified and approved. Document any change to the simulation assumptions.
- Why: students should be able to reproduce the results without unnecessary installation or confusion with a real kernel scheduler.

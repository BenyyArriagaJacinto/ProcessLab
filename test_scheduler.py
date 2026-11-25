import unittest
from scheduler import Process, schedule


class SchedulerTests(unittest.TestCase):
    def setUp(self):
        self.items = [Process('P1', 0, 5), Process('P2', 1, 3), Process('P3', 2, 1)]

    def test_fcfs_order_and_metrics(self):
        timeline, metrics = schedule(self.items)
        self.assertEqual(timeline, [(0,5,'P1'), (5,8,'P2'), (8,9,'P3')])
        self.assertEqual([metrics[p]['waiting'] for p in ('P1','P2','P3')], [0,4,6])

    def test_rr_order_and_metrics(self):
        timeline, metrics = schedule(self.items, 'rr', 2)
        self.assertEqual(timeline, [(0,2,'P1'),(2,4,'P2'),(4,5,'P3'),(5,7,'P1'),(7,8,'P2'),(8,9,'P1')])
        self.assertEqual([metrics[p]['waiting'] for p in ('P1','P2','P3')], [4,4,2])
        self.assertEqual([metrics[p]['response'] for p in ('P1','P2','P3')], [0,1,2])

    def test_idle_cpu(self):
        for alg in ('fcfs','rr'):
            with self.subTest(alg=alg):
                self.assertEqual(schedule([Process('A',3,1), Process('B',6,1)], alg)[0],
                                 [(0,3,'IDLE'),(3,4,'A'),(4,6,'IDLE'),(6,7,'B')])

    def test_invalid_quantum(self):
        for q in (0,-1,1.5):
            with self.assertRaises(ValueError):
                schedule(self.items, 'rr', q)

    def test_invalid_process(self):
        for p in (Process('A',-1,2), Process('B',0,0), Process('IDLE',0,1)):
            with self.assertRaises(ValueError):
                schedule([p])

    def test_duplicate_pid(self):
        with self.assertRaises(ValueError):
            schedule([Process('A',0,2), Process('A',1,3)])

    def test_empty(self):
        self.assertEqual(schedule([]), ([],{}))

    def test_stable_ties(self):
        self.assertEqual(schedule([Process('B',0,1), Process('A',0,1)])[0], [(0,1,'B'),(1,2,'A')])

    def test_invalid_pid_types_and_blank(self):
        for pid in (42, [], None, '', '   ', 'IDLE'):
            with self.subTest(pid=pid), self.assertRaises(ValueError):
                schedule([Process(pid, 0, 1)])

    def test_all_metrics(self):
        expected = {
            'fcfs': [(5,5,0,0), (8,7,4,4), (9,7,6,6)],
            'rr': [(9,9,4,0), (8,7,4,1), (5,3,2,2)],
        }
        for algorithm, rows in expected.items():
            with self.subTest(algorithm=algorithm):
                _, metrics = schedule(self.items, algorithm, 2)
                actual = [tuple(metrics[p][k] for k in ('finish','turnaround','waiting','response'))
                          for p in ('P1','P2','P3')]
                self.assertEqual(actual, rows)

    def test_invalid_algorithm_and_boolean_time(self):
        with self.assertRaises(ValueError):
            schedule(self.items, 'unknown')
        for process in (Process('A', True, 1), Process('A', 0, True)):
            with self.assertRaises(ValueError):
                schedule([process])
        with self.assertRaises(ValueError):
            schedule(self.items, 'rr', True)


if __name__ == '__main__':
    unittest.main()

"""
AEGIS CONTINUOUS EVOLUTION LOOP
"""

import time
from datetime import datetime

from elosam.core.offline_evolution_runner import OfflineEvolutionRunner


class ContinuousEvolutionLoop:
    def __init__(self):
        self.runner = OfflineEvolutionRunner()
        self.history = []

    def run(self):
        print("START")

        for i in range(3):
            result = self.runner.run_once()

            self.history.append(result)

            print(result)

            time.sleep(1)


if __name__ == "__main__":
    ContinuousEvolutionLoop().run()
"""
ELOSam AUTONOMOUS LOOP v3 - WITH DECISION LAYER
"""

import time
from elosam.core.offline_evolution_runner import OfflineEvolutionRunner
from elosam.core.decision_engine import DecisionEngine


class AutonomousLoop:
    def __init__(self):
        self.runner = OfflineEvolutionRunner()
        self.decision = DecisionEngine()
        self.history = []

    def run(self):
        print("Ã°Å¸Â§Â  ACTIVE EVOLUTION LOOP STARTED")

        for i in range(5):
            result = self.runner.run_once()

            decision = self.decision.decide(result)

            record = {
                "cycle": i + 1,
                "result": result,
                "decision": decision
            }

            self.history.append(record)

            print("\nÃ°Å¸â€Â CYCLE:", i + 1)
            print("Ã°Å¸â€œÅ  STATUS:", result.get("status"))
            print("Ã°Å¸Â§Â  DECISION:", decision["action"])
            print("Ã¢Å¡â€“ IMPACT:", decision["impact"])

            time.sleep(1)

        print("\nÃ¢Å“â€¦ EVOLUTION LOOP COMPLETE")
        return self.history


if __name__ == "__main__":
    AutonomousLoop().run()

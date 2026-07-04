"""
ELOSam FINAL REPORT ENGINE
Um único ponto de visão do sistema inteiro
"""

from elosam.core.offline_evolution_runner import OfflineEvolutionRunner
from elosam.core.dependency_graph_engine import DependencyGraphEngine


class FinalReport:
    def run(self):
        runner = OfflineEvolutionRunner()
        result = runner.run_once()

        graph = DependencyGraphEngine().build()

        print("\n🧠 ELOSam SYSTEM REPORT\n")
        print("✔ Modules:", graph["total_modules"])
        print("✔ Status:", result["status"])
        print("✔ Impact:", result["impact"]["impact_score"])

        if result["impact"]["impact_score"] < 0.02:
            print("\n📊 System State: STABLE 🟢")
        else:
            print("\n📊 System State: EVOLVING 🔥")

        print("\n🧠 System is operational.")


if __name__ == "__main__":
    FinalReport().run()

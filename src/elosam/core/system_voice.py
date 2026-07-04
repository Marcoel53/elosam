"""
ELOSam SYSTEM VOICE LAYER v1
Transforma estado técnico em leitura compreensível do sistema
"""

from elosam.core.cognitive_evolution_core import CognitiveEvolutionCore


class SystemVoice:
    def __init__(self):
        self.core = CognitiveEvolutionCore()

    def speak(self):
        data = self.core.run()

        analysis = data["analysis"]
        decision = data["decision"]

        print("\n🧠 ELOSam SYSTEM REPORT\n")

        print(f"📦 Modules analyzed: {len(analysis['affected_modules'])}")
        print(f"⚖ Impact score: {analysis['impact_score']}")

        print("\n🧭 Decision Engine:")
        print(f"- Should evolve: {decision['should_evolve']}")
        print(f"- Risk level: {decision['risk']}")
        print(f"- Reason: {decision['reason']}")

        print("\n🧠 Status:")
        if decision["should_evolve"]:
            print("EVOLUTION READY 🔥")
        else:
            print("STABLE STATE 🟢")


if __name__ == "__main__":
    SystemVoice().speak()

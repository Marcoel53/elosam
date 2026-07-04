from elosam.core.code_introspector import CodeIntrospector
from elosam.core.diagnostic_engine import DiagnosticEngine
from elosam.core.change_proposal_engine import ChangeProposalEngine
from elosam.core.patch_simulation_engine import PatchSimulationEngine
from elosam.core.evolution_decision_engine import EvolutionDecisionEngine
from elosam.core.real_patch_generator import RealPatchGenerator
from elosam.core.safe_apply_engine import SafeApplyEngine
from elosam.core.evolution_execution_engine import EvolutionExecutionEngine


def test_full_evolution_flow():

    # ⚙️ camada base (sem observability real aqui)
    introspector = CodeIntrospector()
    diagnostic = DiagnosticEngine(
        observability=__import__("elosam.core.observability_engine").core.observability_engine.ObservabilityEngine()
    )

    # 🧠 proposal engine REAL (faltava isso)
    proposal_engine = ChangeProposalEngine(
        introspector=introspector,
        diagnostic=diagnostic,
    )

    # 🧪 simulação
    simulator = PatchSimulationEngine(
        proposal_engine=proposal_engine
    )

    # 🧭 decisão
    decision_engine = EvolutionDecisionEngine(
        simulator=simulator
    )

    # 🔧 execução
    exec_engine = EvolutionExecutionEngine(decision_engine)

    result = exec_engine.execute()

    assert isinstance(result, dict)

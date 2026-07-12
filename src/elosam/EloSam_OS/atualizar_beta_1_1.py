from pathlib import Path

ROOT = Path.cwd()

APP_FILE = ROOT / "elosam" / "app.py"

APP_CODE = r'''
from contextlib import asynccontextmanager
from datetime import datetime
import uuid

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from elosam.kernel.kernel import Kernel


kernel = Kernel("./bundles")

missions = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kernel.boot()
    yield
    await kernel.shutdown()


def now():
    return datetime.now().isoformat(
        timespec="seconds"
    )


def add_event(mission, event_type, message):
    mission["events"].append(
        {
            "time": now(),
            "type": event_type,
            "message": message,
        }
    )


async def execute_mission(goal):
    mission_id = str(uuid.uuid4())

    mission = {
        "id": mission_id,
        "goal": goal,
        "status": "RECEIVED",
        "created_at": now(),
        "policy": None,
        "plan": None,
        "events": [],
    }

    missions[mission_id] = mission

    add_event(
        mission,
        "mission.received",
        "Missão recebida pelo EloSam.",
    )

    mission["status"] = "POLICY_EVALUATION"

    add_event(
        mission,
        "policy.started",
        "Policy Engine avaliando a missão.",
    )

    policy_result = await kernel.resolver.execute(
        "policy.evaluate",
        request={
            "mission_id": mission_id,
            "goal": goal,
        },
    )

    mission["policy"] = policy_result

    add_event(
        mission,
        "policy.completed",
        (
            "Decisão da Policy: "
            + policy_result.get(
                "decision",
                "UNKNOWN",
            )
        ),
    )

    if policy_result.get("decision") != "ALLOW":
        mission["status"] = "BLOCKED"

        add_event(
            mission,
            "mission.blocked",
            "Missão bloqueada pela Policy.",
        )

        return mission

    mission["status"] = "PLANNING"

    add_event(
        mission,
        "maestro.started",
        "Maestro criando o plano.",
    )

    plan = await kernel.resolver.execute(
        "maestro.plan",
        goal=goal,
    )

    mission["plan"] = plan

    add_event(
        mission,
        "maestro.completed",
        "Plano criado pelo Maestro.",
    )

    mission["status"] = "PLANNED"

    add_event(
        mission,
        "mission.planned",
        "Missão planejada com sucesso.",
    )

    return mission


def create_app():
    app = FastAPI(
        title="EloSam OS",
        version="1.1.0-beta",
        lifespan=lifespan,
    )

    @app.get("/", response_class=HTMLResponse)
    async def dashboard():
        return r'''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >

    <title>EloSam OS</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family:
                "Segoe UI",
                Arial,
                sans-serif;
            background:
                radial-gradient(
                    circle at top,
                    #17294e,
                    #070b14 55%
                );
            color: #eef4ff;
        }

        .container {
            width: min(1100px, 92%);
            margin: auto;
            padding: 45px 0;
        }

        .eyebrow {
            color: #6ea2ff;
            font-weight: 700;
            letter-spacing: 2px;
            font-size: 13px;
        }

        h1 {
            margin: 8px 0;
            font-size: clamp(
                45px,
                7vw,
                76px
            );
        }

        .subtitle {
            color: #b2bfd7;
            font-size: 19px;
        }

        .status {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-top: 18px;
            padding: 10px 16px;
            border-radius: 999px;
            background:
                rgba(
                    45,
                    230,
                    140,
                    0.08
                );
            border:
                1px solid
                rgba(
                    45,
                    230,
                    140,
                    0.3
                );
        }

        .dot {
            width: 11px;
            height: 11px;
            border-radius: 50%;
            background: #35e88d;
            box-shadow:
                0 0 18px #35e88d;
        }

        .panel {
            margin-top: 35px;
            padding: 28px;
            border-radius: 22px;
            background:
                rgba(
                    255,
                    255,
                    255,
                    0.055
                );
            border:
                1px solid
                rgba(
                    255,
                    255,
                    255,
                    0.09
                );
        }

        textarea {
            width: 100%;
            min-height: 130px;
            resize: vertical;
            padding: 18px;
            border-radius: 14px;
            border:
                1px solid
                rgba(
                    255,
                    255,
                    255,
                    0.12
                );
            background: #0a1120;
            color: white;
            font-size: 17px;
            outline: none;
        }

        textarea:focus {
            border-color: #4b86ff;
        }

        button {
            margin-top: 16px;
            padding: 14px 24px;
            border: 0;
            border-radius: 12px;
            background: #397cff;
            color: white;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
        }

        button:disabled {
            opacity: 0.5;
            cursor: wait;
        }

        .mission {
            display: none;
            margin-top: 30px;
        }

        .badge {
            display: inline-block;
            padding: 7px 12px;
            border-radius: 999px;
            background:
                rgba(
                    57,
                    124,
                    255,
                    0.16
                );
            color: #82adff;
            font-weight: 700;
        }

        .event {
            position: relative;
            padding:
                12px
                12px
                12px
                28px;
            border-left:
                2px solid #2a3b59;
        }

        .event::before {
            content: "";
            position: absolute;
            left: -6px;
            top: 18px;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #35e88d;
        }

        .event-time {
            color: #71809a;
            font-size: 12px;
        }

        .plan-step {
            margin-top: 10px;
            padding: 15px;
            border-radius: 12px;
            background:
                rgba(
                    255,
                    255,
                    255,
                    0.045
                );
        }

        .error {
            color: #ff8585;
        }
    </style>
</head>

<body>
    <main class="container">

        <div class="eyebrow">
            SISTEMA OPERACIONAL PARA
            ORGANIZAÇÕES DIGITAIS
        </div>

        <h1>EloSam OS</h1>

        <div class="subtitle">
            Mission Control — Beta 1.1
        </div>

        <div class="status">
            <div class="dot"></div>
            Kernel ONLINE
        </div>

        <section class="panel">
            <h2>Nova Missão</h2>

            <p>
                Diga ao EloSam qual objetivo
                deve ser transformado em missão.
            </p>

            <textarea
                id="goal"
                placeholder="Exemplo: Crie um plano para aumentar a renda da família."
            ></textarea>

            <br>

            <button
                id="startButton"
                onclick="startMission()"
            >
                INICIAR MISSÃO
            </button>
        </section>

        <section
            id="missionPanel"
            class="panel mission"
        >
            <h2>Missão</h2>

            <div
                id="missionStatus"
                class="badge"
            ></div>

            <h3 id="missionGoal"></h3>

            <h3>Plano do Maestro</h3>

            <div id="plan"></div>

            <h3>Linha do Tempo</h3>

            <div id="events"></div>
        </section>

    </main>

    <script>
        async function startMission() {
            const goal =
                document
                    .getElementById("goal")
                    .value
                    .trim();

            if (!goal) {
                alert(
                    "Digite o objetivo da missão."
                );
                return;
            }

            const button =
                document.getElementById(
                    "startButton"
                );

            button.disabled = true;
            button.innerText =
                "ELOSAM PROCESSANDO...";

            try {
                const response = await fetch(
                    "/api/missions",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify({
                            goal: goal
                        })
                    }
                );

                const mission =
                    await response.json();

                renderMission(mission);

            } catch (error) {
                alert(
                    "Erro ao executar missão: "
                    + error
                );

            } finally {
                button.disabled = false;
                button.innerText =
                    "INICIAR MISSÃO";
            }
        }


        function renderMission(mission) {
            const panel =
                document.getElementById(
                    "missionPanel"
                );

            panel.style.display = "block";

            document.getElementById(
                "missionStatus"
            ).innerText =
                mission.status;

            document.getElementById(
                "missionGoal"
            ).innerText =
                mission.goal;

            const plan =
                document.getElementById(
                    "plan"
                );

            plan.innerHTML = "";

            if (
                mission.plan &&
                mission.plan.plan
            ) {
                mission.plan.plan.forEach(
                    (step, index) => {
                        const div =
                            document.createElement(
                                "div"
                            );

                        div.className =
                            "plan-step";

                        div.innerText =
                            (index + 1)
                            + ". "
                            + step.description;

                        plan.appendChild(div);
                    }
                );
            }

            const events =
                document.getElementById(
                    "events"
                );

            events.innerHTML = "";

            mission.events.forEach(
                event => {
                    const div =
                        document.createElement(
                            "div"
                        );

                    div.className = "event";

                    div.innerHTML =
                        "<strong>"
                        + event.message
                        + "</strong>"
                        + "<div class='event-time'>"
                        + event.time
                        + " — "
                        + event.type
                        + "</div>";

                    events.appendChild(div);
                }
            );

            panel.scrollIntoView({
                behavior: "smooth"
            });
        }
    </script>
</body>
</html>
'''

    @app.get("/api/status")
    async def status():
        return kernel.status()

    @app.get("/api/capabilities")
    async def capabilities():
        return {
            "capabilities":
                kernel.registry.list_capabilities()
        }

    @app.post("/api/missions")
    async def create_mission(
        payload: dict,
    ):
        goal = str(
            payload.get(
                "goal",
                "",
            )
        ).strip()

        if not goal:
            return {
                "success": False,
                "error":
                    "O objetivo da missão é obrigatório.",
            }

        return await execute_mission(goal)

    @app.get(
        "/api/missions/{mission_id}"
    )
    async def get_mission(
        mission_id: str,
    ):
        mission = missions.get(
            mission_id
        )

        if mission is None:
            return {
                "found": False,
            }

        return mission

    @app.get("/api/missions")
    async def list_missions():
        return {
            "missions":
                list(missions.values())
        }

    return app
'''

APP_FILE.write_text(
    APP_CODE,
    encoding="utf-8",
)

print("=" * 60)
print("ELOSAM OS BETA 1.1 INSTALADO")
print("=" * 60)
print()
print("Mission Control criado.")
print("UTF-8 corrigido no novo dashboard.")
print()
print("Execute novamente:")
print("INICIAR_ELOSAM.bat")
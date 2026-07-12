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
    return datetime.now().isoformat(timespec="seconds")


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
        "brothers": [],
        "results": [],
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
        "Decisão da Policy: "
        + policy_result.get("decision", "UNKNOWN"),
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
        "Maestro analisando e criando o plano.",
    )

    plan = await kernel.resolver.execute(
        "maestro.plan",
        goal=goal,
    )

    mission["plan"] = plan
    mission["brothers"] = plan.get("brothers", [])

    add_event(
        mission,
        "maestro.completed",
        "Plano e roteamento criados pelo Maestro.",
    )

    mission["status"] = "ROUTING"

    for brother in mission["brothers"]:
        brother_name = brother["brother"]
        capability = brother["capability"]

        add_event(
            mission,
            "brother.selected",
            f"Brother {brother_name} selecionado.",
        )

        mission["status"] = "EXECUTING"

        add_event(
            mission,
            "brother.started",
            f"Brother {brother_name} iniciou o trabalho.",
        )

        try:
            result = await kernel.resolver.execute(
                capability,
                goal=goal,
            )

            mission["results"].append(
                {
                    "brother": brother_name,
                    "capability": capability,
                    "success": True,
                    "result": result,
                }
            )

            add_event(
                mission,
                "brother.completed",
                f"Brother {brother_name} concluiu o trabalho.",
            )

        except Exception as error:
            mission["results"].append(
                {
                    "brother": brother_name,
                    "capability": capability,
                    "success": False,
                    "error": str(error),
                }
            )

            add_event(
                mission,
                "brother.failed",
                f"Brother {brother_name} falhou: {error}",
            )

    mission["status"] = "COMPLETED"

    add_event(
        mission,
        "mission.completed",
        "Missão executada pelos Brothers.",
    )

    return mission


def create_app():
    app = FastAPI(
        title="EloSam OS",
        version="1.3.0-beta",
        lifespan=lifespan,
    )

    @app.get("/", response_class=HTMLResponse)
    async def dashboard():
        return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >

    <title>EloSam OS — Mission Control</title>

    <style>
        * {
            box-sizing: border-box;
        }

        :root {
            --bg: #070c16;
            --surface: #121a29;
            --surface-2: #192335;
            --surface-3: #0a1220;
            --border: #29354a;
            --text: #f3f7ff;
            --muted: #91a2bc;
            --blue: #397cff;
            --blue-light: #78a7ff;
            --green: #36e58c;
            --green-dark: #123e2b;
            --red: #ff6b6b;
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
                    circle at 50% -20%,
                    #182b50,
                    var(--bg) 48%
                );
            color: var(--text);
        }

        .container {
            width: min(1200px, 92%);
            margin: 0 auto;
            padding: 42px 0 80px;
        }

        .eyebrow {
            color: var(--blue-light);
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 2px;
        }

        h1 {
            margin: 8px 0 2px;
            font-size: clamp(46px, 7vw, 78px);
            line-height: 1;
        }

        .subtitle {
            margin-top: 18px;
            color: #c2cee0;
            font-size: 19px;
        }

        .kernel-status {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-top: 18px;
            padding: 10px 16px;
            border: 1px solid rgba(54, 229, 140, 0.35);
            border-radius: 999px;
            background: rgba(54, 229, 140, 0.08);
            font-weight: 700;
        }

        .dot {
            width: 11px;
            height: 11px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 16px var(--green);
        }

        .panel {
            margin-top: 32px;
            padding: 26px;
            border: 1px solid var(--border);
            border-radius: 20px;
            background: rgba(18, 26, 41, 0.96);
        }

        .panel h2 {
            margin-top: 0;
        }

        .mission-input-panel {
            margin-top: 36px;
        }

        textarea {
            width: 100%;
            min-height: 135px;
            padding: 18px;
            resize: vertical;
            border: 1px solid var(--border);
            border-radius: 14px;
            outline: none;
            background: var(--surface-3);
            color: var(--text);
            font-family:
                Consolas,
                "Courier New",
                monospace;
            font-size: 16px;
            line-height: 1.6;
        }

        textarea:focus {
            border-color: var(--blue);
            box-shadow:
                0 0 0 3px rgba(57, 124, 255, 0.12);
        }

        textarea::placeholder {
            color: #71819a;
        }

        .mission-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            min-width: 210px;
            margin-top: 18px;
            padding: 15px 22px;
            border: 0;
            border-radius: 12px;
            background: var(--blue);
            color: white;
            font-size: 15px;
            font-weight: 800;
            cursor: pointer;
            transition:
                transform 0.15s ease,
                opacity 0.15s ease;
        }

        .mission-button:hover {
            transform: translateY(-1px);
        }

        .mission-button:disabled {
            opacity: 0.55;
            cursor: wait;
            transform: none;
        }

        .mission-area {
            display: none;
            margin-top: 24px;
        }

        .mission-grid {
            display: grid;
            grid-template-columns:
                minmax(0, 1fr)
                minmax(0, 1fr);
            gap: 20px;
        }

        .mission-grid .panel {
            margin-top: 0;
        }

        .full-width {
            grid-column: 1 / -1;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            padding: 8px 13px;
            border-radius: 999px;
            background: rgba(54, 229, 140, 0.12);
            border: 1px solid rgba(54, 229, 140, 0.45);
            color: #9affc9;
            font-size: 13px;
            font-weight: 800;
        }

        .mission-goal {
            margin: 20px 0 24px;
            font-size: 18px;
            line-height: 1.5;
        }

        .step {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 10px;
            padding: 15px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.045);
        }

        .step-number {
            display: flex;
            flex: 0 0 28px;
            width: 28px;
            height: 28px;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: rgba(54, 229, 140, 0.18);
            color: #aaffcf;
            font-weight: 800;
        }

        .brother-card {
            margin-top: 12px;
            padding: 18px;
            border: 1px solid var(--border);
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.035);
        }

        .brother-name {
            font-size: 17px;
            font-weight: 800;
        }

        .brother-meta {
            margin-top: 6px;
            color: var(--muted);
        }

        .brother-output {
            margin-top: 16px;
            padding: 16px;
            border-radius: 12px;
            background: var(--surface-3);
            border: 1px solid var(--border);
        }

        .brother-output-title {
            margin-bottom: 10px;
            color: var(--blue-light);
            font-size: 13px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .brother-output ol {
            margin:
                10px
                0
                0
                22px;
            padding: 0;
        }

        .brother-output li {
            margin: 8px 0;
            line-height: 1.5;
        }

        .brother-output pre {
            margin: 10px 0 0;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            color: #cbd8eb;
            font-family:
                Consolas,
                "Courier New",
                monospace;
            font-size: 13px;
            line-height: 1.5;
        }

        .success {
            color: var(--green);
            font-weight: 800;
        }

        .failure {
            color: var(--red);
            font-weight: 800;
        }

        .timeline {
            margin-top: 12px;
            padding-left: 8px;
        }

        .event {
            position: relative;
            padding:
                7px
                0
                17px
                28px;
            border-left:
                2px solid #31425f;
        }

        .event::before {
            content: "";
            position: absolute;
            left: -7px;
            top: 12px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--green);
            box-shadow:
                0 0 12px rgba(54, 229, 140, 0.45);
        }

        .event-message {
            font-weight: 700;
            line-height: 1.4;
        }

        .event-meta {
            margin-top: 4px;
            color: #7186a6;
            font-size: 12px;
        }

        .empty {
            color: var(--muted);
        }

        @media (max-width: 800px) {
            .mission-grid {
                grid-template-columns: 1fr;
            }

            .full-width {
                grid-column: auto;
            }

            .mission-button {
                width: 100%;
            }
        }
    </style>
</head>

<body>
    <main class="container">

        <header>
            <div class="eyebrow">
                SISTEMA OPERACIONAL PARA ORGANIZAÇÕES DIGITAIS
            </div>

            <h1>EloSam OS</h1>

            <div class="subtitle">
                Mission Control — Beta 1.3
            </div>

            <div class="kernel-status">
                <span class="dot"></span>
                Kernel ONLINE
            </div>
        </header>

        <section class="panel mission-input-panel">
            <h2>Nova Missão</h2>

            <p>
                Diga ao EloSam qual objetivo deve ser
                transformado em missão.
            </p>

            <textarea
                id="goal"
                placeholder="Exemplo: Crie um plano para aumentar a renda da família."
            ></textarea>

            <button
                id="startButton"
                class="mission-button"
                type="button"
                onclick="startMission()"
            >
                <span>▶</span>
                <span>INICIAR MISSÃO</span>
            </button>
        </section>

        <section
            id="missionArea"
            class="mission-area"
        >
            <div class="mission-grid">

                <section class="panel">
                    <h2>Missão</h2>

                    <div
                        id="missionStatus"
                        class="badge"
                    >
                        AGUARDANDO
                    </div>

                    <div
                        id="missionGoal"
                        class="mission-goal"
                    ></div>

                    <h3>Plano do Maestro</h3>

                    <div id="plan"></div>
                </section>

                <section class="panel">
                    <h2>Brothers Executados</h2>

                    <div id="results"></div>
                </section>

                <section class="panel full-width">
                    <h2>Linha do Tempo</h2>

                    <div
                        id="events"
                        class="timeline"
                    ></div>
                </section>

            </div>
        </section>

    </main>

    <script>
        async function startMission() {
            const goalElement =
                document.getElementById("goal");

            const goal =
                goalElement.value.trim();

            if (!goal) {
                alert(
                    "Digite o objetivo da missão."
                );
                goalElement.focus();
                return;
            }

            const button =
                document.getElementById(
                    "startButton"
                );

            button.disabled = true;

            button.innerHTML =
                "<span>⏳</span>"
                + "<span>ELOSAM PROCESSANDO...</span>";

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

                if (!response.ok) {
                    throw new Error(
                        "HTTP "
                        + response.status
                    );
                }

                const mission =
                    await response.json();

                if (mission.success === false) {
                    throw new Error(
                        mission.error
                        || "Falha ao criar missão."
                    );
                }

                renderMission(mission);

            } catch (error) {
                alert(
                    "Erro ao executar missão: "
                    + error.message
                );

            } finally {
                button.disabled = false;

                button.innerHTML =
                    "<span>▶</span>"
                    + "<span>INICIAR MISSÃO</span>";
            }
        }


        function renderMission(mission) {
            const area =
                document.getElementById(
                    "missionArea"
                );

            area.style.display = "block";

            document.getElementById(
                "missionStatus"
            ).textContent =
                mission.status;

            document.getElementById(
                "missionGoal"
            ).textContent =
                mission.goal;

            renderPlan(mission);
            renderResults(mission);
            renderEvents(mission);

            area.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }


        function renderPlan(mission) {
            const planElement =
                document.getElementById(
                    "plan"
                );

            planElement.innerHTML = "";

            const steps =
                mission.plan
                && mission.plan.plan
                ? mission.plan.plan
                : [];

            if (steps.length === 0) {
                planElement.innerHTML =
                    "<div class='empty'>"
                    + "Nenhum passo disponível."
                    + "</div>";

                return;
            }

            steps.forEach(
                (step, index) => {
                    const div =
                        document.createElement(
                            "div"
                        );

                    div.className = "step";

                    const number =
                        document.createElement(
                            "span"
                        );

                    number.className =
                        "step-number";

                    number.textContent =
                        index + 1;

                    const description =
                        document.createElement(
                            "span"
                        );

                    description.textContent =
                        step.description;

                    div.appendChild(number);
                    div.appendChild(description);

                    planElement.appendChild(div);
                }
            );
        }


        function renderResults(mission) {
            const resultsElement =
                document.getElementById(
                    "results"
                );

            resultsElement.innerHTML = "";

            const results =
                mission.results || [];

            if (results.length === 0) {
                resultsElement.innerHTML =
                    "<div class='empty'>"
                    + "Nenhum Brother executado."
                    + "</div>";

                return;
            }

            results.forEach(
                item => {
                    const card =
                        document.createElement(
                            "div"
                        );

                    card.className =
                        "brother-card";

                    const name =
                        document.createElement(
                            "div"
                        );

                    name.className =
                        "brother-name";

                    name.textContent =
                        "Brother "
                        + item.brother;

                    const meta =
                        document.createElement(
                            "div"
                        );

                    meta.className =
                        "brother-meta";

                    const capability =
                        document.createElement(
                            "span"
                        );

                    capability.textContent =
                        item.capability
                        + " — ";

                    const status =
                        document.createElement(
                            "span"
                        );

                    status.className =
                        item.success
                        ? "success"
                        : "failure";

                    status.textContent =
                        item.success
                        ? "CONCLUÍDO"
                        : "FALHOU";

                    meta.appendChild(
                        capability
                    );

                    meta.appendChild(
                        status
                    );

                    card.appendChild(name);
                    card.appendChild(meta);

                    if (
                        item.success
                        && item.result
                    ) {
                        const output =
                            document.createElement(
                                "div"
                            );

                        output.className =
                            "brother-output";

                        const title =
                            document.createElement(
                                "div"
                            );

                        title.className =
                            "brother-output-title";

                        title.textContent =
                            "Resultado do trabalho";

                        output.appendChild(title);

                        if (
                            item.result.plan
                            && Array.isArray(
                                item.result.plan
                            )
                        ) {
                            const list =
                                document.createElement(
                                    "ol"
                                );

                            item.result.plan.forEach(
                                step => {
                                    const li =
                                        document.createElement(
                                            "li"
                                        );

                                    if (
                                        typeof step
                                        === "string"
                                    ) {
                                        li.textContent =
                                            step;
                                    } else {
                                        li.textContent =
                                            step.description
                                            || JSON.stringify(
                                                step
                                            );
                                    }

                                    list.appendChild(li);
                                }
                            );

                            output.appendChild(list);

                        } else {
                            const pre =
                                document.createElement(
                                    "pre"
                                );

                            pre.textContent =
                                JSON.stringify(
                                    item.result,
                                    null,
                                    2
                                );

                            output.appendChild(pre);
                        }

                        card.appendChild(output);
                    }

                    resultsElement.appendChild(
                        card
                    );
                }
            );
        }


        function renderEvents(mission) {
            const eventsElement =
                document.getElementById(
                    "events"
                );

            eventsElement.innerHTML = "";

            const events =
                mission.events || [];

            events.forEach(
                event => {
                    const div =
                        document.createElement(
                            "div"
                        );

                    div.className = "event";

                    const message =
                        document.createElement(
                            "div"
                        );

                    message.className =
                        "event-message";

                    message.textContent =
                        event.message;

                    const meta =
                        document.createElement(
                            "div"
                        );

                    meta.className =
                        "event-meta";

                    meta.textContent =
                        event.time
                        + " — "
                        + event.type;

                    div.appendChild(message);
                    div.appendChild(meta);

                    eventsElement.appendChild(div);
                }
            );
        }
    </script>
</body>
</html>
"""

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
    async def create_mission(payload: dict):
        goal = str(
            payload.get("goal", "")
        ).strip()

        if not goal:
            return {
                "success": False,
                "error":
                    "O objetivo da missão é obrigatório.",
            }

        return await execute_mission(goal)

    @app.get("/api/missions")
    async def list_missions():
        return {
            "missions":
                list(missions.values())
        }

    @app.get("/api/missions/{mission_id}")
    async def get_mission(mission_id: str):
        mission = missions.get(mission_id)

        if mission is None:
            return {
                "found": False,
            }

        return mission

    return app

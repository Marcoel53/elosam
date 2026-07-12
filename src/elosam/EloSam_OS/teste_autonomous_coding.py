from elosam.kernel.autonomous_coding_agent import (
    AutonomousCodingAgent,
)
from elosam.kernel.coding_agent import (
    CodingAgent,
)
from elosam.kernel.coding_workspace import (
    CodingWorkspace,
)
from elosam.kernel.local_model_provider import (
    LocalModelProvider,
)


workspace = CodingWorkspace(
    root="./workspace"
)

coding_agent = CodingAgent(
    workspace=workspace
)

model_provider = LocalModelProvider(
    model="qwen2.5-coder:1.5b"
)

agent = AutonomousCodingAgent(
    model_provider=model_provider,
    coding_agent=coding_agent,
    max_plan_attempts=3,
    max_execution_attempts=3,
)


mission = """
Crie um programa Python que receba uma temperatura
em graus Celsius e converta para Fahrenheit.

O programa deve possuir uma função reutilizável.

Crie também testes para validar:
- 0 Celsius deve resultar em 32 Fahrenheit;
- 100 Celsius deve resultar em 212 Fahrenheit;
- -40 Celsius deve resultar em -40 Fahrenheit.

O programa principal deve demonstrar uma conversão
automaticamente, sem solicitar entrada do usuário.
"""


print("=" * 60)
print(
    "ELOSAM OS - MISSAO AUTONOMA "
    "COM CICLO DE AUTOCORRECAO"
)
print("=" * 60)

print(
    "\nAUTONOMOUS CODING AGENT:",
    agent.VERSION,
)

print("\nMISSAO:")
print(
    mission.strip()
)

print(
    "\nELOSAM ESTA GERANDO, "
    "EXECUTANDO E CORRIGINDO "
    "O CODIGO LOCALMENTE..."
)

print(
    "AGUARDE A CONCLUSAO "
    "DE TODAS AS TENTATIVAS...\n"
)


result = agent.run(
    mission,
    mission_id=(
        "primeira_missao_autonoma"
    ),
)


print("=" * 60)
print("RESULTADO FINAL")
print("=" * 60)

print(
    "STATUS:",
    result["status"],
)

print(
    "RESUMO:",
    result["summary"],
)


print(
    "\nHISTORICO DE PLANEJAMENTO:"
)

for index, attempt in enumerate(
    result.get(
        "planning_attempts",
        [],
    ),
    start=1,
):
    print(
        f"- Registro {index}:",
        attempt,
    )


print(
    "\nHISTORICO DE EXECUCOES:"
)

execution_attempts = result.get(
    "execution_attempts",
    [],
)

print(
    "TOTAL DE TENTATIVAS:",
    len(
        execution_attempts
    ),
)

for attempt in execution_attempts:
    print(
        "\n" + "-" * 60
    )

    print(
        "TENTATIVA:",
        attempt.get(
            "attempt"
        ),
    )

    print(
        "STATUS:",
        attempt.get(
            "status"
        ),
    )

    failures = attempt.get(
        "failures",
        [],
    )

    print(
        "FALHAS:",
        len(
            failures
        ),
    )

    for failure in failures:
        print(
            "\nFASE:",
            failure.get(
                "phase"
            ),
        )

        print(
            "ARQUIVO:",
            failure.get(
                "file"
            ),
        )

        print(
            "RETURN CODE:",
            failure.get(
                "returncode"
            ),
        )

        print(
            "TIMEOUT:",
            failure.get(
                "timed_out"
            ),
        )

        stdout = failure.get(
            "stdout",
            "",
        )

        stderr = failure.get(
            "stderr",
            "",
        )

        if stdout:
            print(
                "\nSTDOUT:"
            )
            print(
                stdout.strip()
            )

        if stderr:
            print(
                "\nSTDERR:"
            )
            print(
                stderr.strip()
            )


print(
    "\n" + "=" * 60
)

print(
    "PROJETO FINAL GERADO"
)

print(
    "=" * 60
)

for file_spec in (
    result[
        "generated_plan"
    ][
        "files"
    ]
):
    print(
        "-",
        file_spec[
            "path"
        ],
    )


print(
    "\nVALIDACOES FINAIS:"
)

for validation in (
    result[
        "execution"
    ][
        "validations"
    ]
):
    print(
        validation[
            "file"
        ],
        validation[
            "success"
        ],
    )

    if validation.get(
        "stderr"
    ):
        print(
            validation[
                "stderr"
            ].strip()
        )


print(
    "\nEXECUCOES FINAIS:"
)

for execution in (
    result[
        "execution"
    ][
        "executions"
    ]
):
    print(
        execution[
            "file"
        ],
        execution[
            "success"
        ],
    )

    if execution.get(
        "stdout"
    ):
        print(
            execution[
                "stdout"
            ].strip()
        )

    if execution.get(
        "stderr"
    ):
        print(
            execution[
                "stderr"
            ].strip()
        )


print(
    "\nWORKSPACE:"
)

for file_path in (
    result[
        "execution"
    ][
        "files"
    ]
):
    print(
        "-",
        file_path,
    )


print(
    "\n" + "=" * 60
)

if (
    result[
        "status"
    ]
    == "COMPLETED"
):
    print(
        "MARCO HISTORICO: "
        "ELOSAM GEROU, VALIDOU, "
        "EXECUTOU E CONCLUIU "
        "A MISSAO AUTONOMAMENTE."
    )

else:
    print(
        "O CICLO AUTONOMO FOI EXECUTADO, "
        "MAS O LIMITE DE TENTATIVAS "
        "FOI ATINGIDO."
    )

print(
    "=" * 60
)
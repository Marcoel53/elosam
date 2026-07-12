from elosam.kernel.coding_agent import CodingAgent
from elosam.kernel.coding_workspace import CodingWorkspace


workspace = CodingWorkspace(
    root="./workspace"
)

agent = CodingAgent(
    workspace=workspace
)

mission_id = "primeiro_codigo_elosam"

program_code = '''
def analisar_numeros(numeros):
    if not numeros:
        raise ValueError(
            "A lista não pode estar vazia."
        )

    return {
        "media": sum(numeros) / len(numeros),
        "minimo": min(numeros),
        "maximo": max(numeros),
    }


if __name__ == "__main__":
    resultado = analisar_numeros(
        [10, 20, 30, 40]
    )

    print(resultado)
'''.lstrip()


test_code = '''
from programa import analisar_numeros


def test_analisar_numeros():
    resultado = analisar_numeros(
        [10, 20, 30, 40]
    )

    assert resultado["media"] == 25
    assert resultado["minimo"] == 10
    assert resultado["maximo"] == 40


if __name__ == "__main__":
    test_analisar_numeros()
    print("TESTES: OK")
'''.lstrip()


result = agent.execute_plan(
    mission_id=mission_id,
    files=[
        {
            "path": "programa.py",
            "content": program_code,
        },
        {
            "path": "test_programa.py",
            "content": test_code,
        },
    ],
    validation_files=[
        "programa.py",
        "test_programa.py",
    ],
    execution_files=[
        "programa.py",
        "test_programa.py",
    ],
)


print("STATUS:", result["status"])

print("\nARQUIVOS CRIADOS:")

for file_path in result["files"]:
    print("-", file_path)


print("\nVALIDACOES:")

for validation in result["validations"]:
    print(
        validation["file"],
        validation["success"],
    )

    if validation["stderr"]:
        print(validation["stderr"])


print("\nEXECUCOES:")

for execution in result["executions"]:
    print(
        execution["file"],
        execution["success"],
    )

    if execution["stdout"]:
        print(
            execution["stdout"].strip()
        )

    if execution["stderr"]:
        print(
            execution["stderr"].strip()
        )
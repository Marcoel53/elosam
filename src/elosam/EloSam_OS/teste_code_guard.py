from elosam.kernel.code_guard import CodeGuard


guard = CodeGuard()


print("=" * 60)
print("TESTE 1 - INPUT PROIBIDO")
print("=" * 60)

result = guard.analyze_source(
    source='valor = input("Digite: ")',
    filename="teste_input.py",
)

print(result)


print("\n" + "=" * 60)
print("TESTE 2 - CODIGO PERMITIDO")
print("=" * 60)

result = guard.analyze_source(
    source="print(42)",
    filename="teste_print.py",
)

print(result)


print("\n" + "=" * 60)
print("STATUS DO CODE GUARD")
print("=" * 60)

print(
    guard.status()
)
def celsius_para_fahrenheit(celsius):
    return (celsius * 9/5) + 32

celsius = 0
fahrenheit = celsius_para_fahrenheit(celsius)
print(f'{celsius} graus Celsius é igual a {fahrenheit:.2f} graus Fahrenheit')
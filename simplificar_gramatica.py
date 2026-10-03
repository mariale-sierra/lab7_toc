import re
import sys


e = "ε"

# Una mayúscula, flecha y una o más producciones separadas por |
patron = r"[A-Z]\s*->\s*(?:ε|[A-Za-z0-9]+)(?:\s*\|\s*(?:ε|[A-Za-z0-9]+))*"


def cargar_archivo(nombre):
    prods = {}

    try:
        archivo = open(nombre, "r", encoding="utf-8")
    except OSError:
        print("ERROR: no se pudo abrir el archivo")
        return None

    for num_linea, linea in enumerate(archivo, 1):
        linea = linea.strip()

        if not re.fullmatch(patron, linea):
            print("ERROR en la línea", num_linea, ":", linea)
            archivo.close()
            return None

        izquierda, derecha = re.split(r"\s*->\s*", linea)
        lista = [prod.strip() for prod in derecha.split("|")]

        if izquierda not in prods:
            prods[izquierda] = []

        for prod in lista:
            if prod not in prods[izquierda]:
                prods[izquierda].append(prod)

    archivo.close()

    if not prods:
        print("ERROR: el archivo está vacío")
        return None

    return prods


def buscar_anulables(prods):
    anulables = set()

    for izquierda in prods:
        if e in prods[izquierda]:
            anulables.add(izquierda)
            print(izquierda, "es anulable directamente por", izquierda, "->", e)

    cambio = True
    while cambio:
        cambio = False

        for izquierda in prods:
            if izquierda in anulables:
                continue

            for prod in prods[izquierda]:
                if prod != e and all(simbolo in anulables for simbolo in prod):
                    anulables.add(izquierda)
                    print(
                        izquierda,
                        "es anulable porque",
                        izquierda,
                        "->",
                        prod,
                    )
                    cambio = True
                    break

    return anulables


def crear_casos(prod, anulables):
    casos = [""]

    for simbolo in prod:
        if simbolo in anulables:
            nuevos = []

            # Por cada caso anterior se crean dos:
            # uno con el anulable y otro sin el anulable.
            for caso in casos:
                nuevos.append(caso + simbolo)
                nuevos.append(caso)

            casos = nuevos
        else:
            # Los símbolos no anulables siempre se mantienen.
            for i in range(len(casos)):
                casos[i] += simbolo

    return casos


def elim_e(prods):
    print("\n1. Búsqueda de símbolos anulables")
    anulables = buscar_anulables(prods)
    print("Anulables =", sorted(anulables))

    nuevas_prods = {}

    for izquierda in prods:
        nuevas_prods[izquierda] = []

        for prod in prods[izquierda]:
            if prod == e:
                print("\nSe elimina", izquierda, "->", e)
                continue

            m = sum(1 for simbolo in prod if simbolo in anulables)
            casos = crear_casos(prod, anulables)

            print(
                "\n",
                izquierda,
                "->",
                prod,
                "tiene",
                m,
                "anulable(s):",
                2 ** m,
                "caso(s)",
            )

            for caso in casos:
                if caso == "":
                    print("  ->", e, "(no se agrega)")
                elif caso in nuevas_prods[izquierda]:
                    print("  ->", caso, "(repetida)")
                else:
                    print("  ->", caso)
                    nuevas_prods[izquierda].append(caso)

    return nuevas_prods


def mostrar_prods(prods):
    for izquierda in prods:
        if prods[izquierda]:
            print(izquierda, "->", " | ".join(prods[izquierda]))


def main():
    if len(sys.argv) != 2:
        print("Uso: python simplificar_gramatica.py archivo.txt")
        return

    prods = cargar_archivo(sys.argv[1])

    if prods is None:
        return

    print("Gramática válida:")
    mostrar_prods(prods)

    prods_sin_e = elim_e(prods)

    print("\nGramática sin producciones epsilon:")
    mostrar_prods(prods_sin_e)


main()

def automata_operador(input_string):
    AutomataRelacional = {
        'q0': {'..': 'q1', '/.': 'q2', '+.-': 'q3', '-.': 'q4', '+.': 'q5', '+': 'q6', '-': 'q7'},
        'q1': {},  # Estado de aceptación para '..'
        'q2': {},  # Estado de aceptación para '/.'
        'q3': {},  # Estado de aceptación para '+.-'
        'q4': {},  # Estado de aceptación para '-.'
        'q5': {},  # Estado de aceptación para '+.'
        'q6': {},  # Estado de aceptación para '+'
        'q7': {},  # Estado de aceptación para '-'
    }

    current_state = 'q0'
    if input_string in AutomataRelacional[current_state]:
        current_state = AutomataRelacional[current_state][input_string]
    else:
        return False  # Si la cadena no es válida, no es un operador relacional
    # Verificar si el último estado es un estado de aceptación
    if current_state in {'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7'}:
        return True
    else:
        return False

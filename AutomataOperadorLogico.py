def automata_logico(input_string):
    AutomataPattern = {
        'q0': {'Y': 'q1', 'O': 'q2', 'N': 'q3'},
        'q1': {'Y': 'q4'},
        'q2': {'O': 'q5'},
        'q3': {'N': 'q6'},
        'q4': {},  # Estado de aceptación para 'YY'
        'q5': {},  # Estado de aceptación para 'OO'
        'q6': {},  # Estado de aceptación para 'NN'
    }

    current_state = 'q0'
    for char in input_string:
        if char in AutomataPattern[current_state]:
            current_state = AutomataPattern[current_state][char]
        else:
            return False  # Si el carácter no es válido para el estado actual, la cadena no es válida
    # Verificar si el último estado es un estado de aceptación
    if current_state in {'q4', 'q5', 'q6'}:
        return True
    else:
        return False


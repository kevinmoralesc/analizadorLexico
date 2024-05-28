def automata_clase(input_string):
    AutomataReservedWords = {
        'q0': {'C': 'q1', 'I': 'q6'},
        'q1': {'A': 'q2'},
        'q2': {'J': 'q3'},
        'q3': {'A': 'q4'},
        'q4': {},  # Estado de aceptación para "CAJA"
        'q6': {'N': 'q7'},
        'q7': {'T': 'q8'},
        'q8': {'E': 'q9'},
        'q9': {'R': 'q10'},
        'q10': {'N': 'q11'},
        'q11': {'O': 'q12'},
        'q12': {},  # Estado de aceptación para "INTERNO"
    }

    current_state = 'q0'
    for char in input_string:
        if char in AutomataReservedWords[current_state]:
            current_state = AutomataReservedWords[current_state][char]
        else:
            return False  # Si el carácter no es válido para el estado actual, la cadena no es válida
    # Verificar si el último estado es un estado de aceptación
    if current_state in {'q4', 'q12'}:
        return True
    else:
        return False

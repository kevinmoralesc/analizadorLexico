def automata_ciclo(input_string):
    AutomataReservedWords = {
        'q0': {'C': 'q1', 'I': 'q7'},
        'q1': {'I': 'q2'},
        'q2': {'R': 'q3'},
        'q3': {'C': 'q4'},
        'q4': {'L': 'q5'},
        'q5': {'E': 'q6'},
        'q6': {},  # Estado de aceptación para "circle"
        'q7': {'N': 'q8'},
        'q8': {'F': 'q9'},
        'q9': {'I': 'q10'},
        'q10': {'N': 'q11'},
        'q11': {'I': 'q12'},
        'q12': {'T': 'q13'},
        'q13': {'E': 'q14'},
        'q14': {},  # Estado de aceptación para "infinite"
    }

    current_state = 'q0'
    for char in input_string:
        if char in AutomataReservedWords[current_state]:
            current_state = AutomataReservedWords[current_state][char]
        else:
            return False  # Si el carácter no es válido para el estado actual, la cadena no es válida
    # Verificar si el último estado es un estado de aceptación
    if current_state in {'q6', 'q14'}:
        return True
    else:
        return False
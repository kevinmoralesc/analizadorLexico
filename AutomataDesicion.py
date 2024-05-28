def automata_Desicion(input_string):
    AutomataReservedWords = {
        'q0': {'C': 'q1', 'S': 'q7'},
        'q1': {'U': 'q2'},
        'q2': {'M': 'q3'},
        'q3': {'P': 'q4'},
        'q4': {'L': 'q5'},
        'q5': {'E': 'q6'},
        'q6': {},  # Estado de aceptación para "CUMPLE"
        'q7': {'E': 'q8'},
        'q8': {'G': 'q9'},
        'q9': {'U': 'q10'},
        'q10': {'I': 'q11'},
        'q11': {'R': 'q12'},
        'q12': {},  # Estado de aceptación para "SEGUIR"
    }

    current_state = 'q0'
    for char in input_string:
        if char in AutomataReservedWords[current_state]:
            current_state = AutomataReservedWords[current_state][char]
        else:
            return False  # Si el carácter no es válido para el estado actual, la cadena no es válida
    # Verificar si el último estado es un estado de aceptación
    if current_state in {'q6', 'q12'}:
        return True
    else:
        return False

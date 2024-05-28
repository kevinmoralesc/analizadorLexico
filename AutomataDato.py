def automata_tipoDato(input_string):
    keyword_automaton = {
        'q0': {'T': 'q1', 'L': 'q5', 'N': 'q9', 'D': 'q13'},
        'q1': {'E': 'q2'},
        'q2': {'X': 'q3'},
        'q3': {'T': 'q4'},
        'q4': {},  # Estado de aceptación para 'TEXT'

        'q5': {'E': 'q6'},
        'q6': {'T': 'q7'},
        'q7': {},  # Estado de aceptación para 'LET'

        'q9': {'A': 'q10'},
        'q10': {'T': 'q11'},
        'q11': {'U': 'q12'},
        'q12': {},  # Estado de aceptación para 'NATU'

        'q13': {'E': 'q14'},
        'q14': {'C': 'q15'},
        'q15': {'I': 'q16'},
        'q16': {},  # Estado de aceptación para 'DECI'
    }

    current_state = 'q0'
    for char in input_string:
        if char in keyword_automaton[current_state]:
            current_state = keyword_automaton[current_state][char]
        else:
            return False  # Si el carácter no es válido para el estado actual, la cadena no es válida
    # Verificar si el último estado es un estado de aceptación
    if current_state in {'q4', 'q7', 'q12', 'q16'}:
        
        return True
    else:
        return False

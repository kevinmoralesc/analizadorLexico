def automata_operator(input_string):
    AutomataAritmetico = {
        'q0': {'SUM': 'q_sum', 'REST': 'q_rest', 'MULT': 'q_mult', 'DIV': 'q_div', 'POT': 'q_pot', 'EXP': 'q_exp'},
        'q_sum': {},
        'q_rest': {},
        'q_mult': {},
        'q_div': {},
        'q_pot': {},
        'q_exp': {},
    }

    current_state = 'q0'
    if input_string in AutomataAritmetico[current_state]:
        current_state = AutomataAritmetico[current_state][input_string]
    else:
        return False  # Si la cadena no es válida, no es un operador aritmético
    # Verificar si el último estado es un estado de aceptación
    if current_state in {'q_sum', 'q_rest', 'q_mult', 'q_div', 'q_pot', 'q_exp'}:
        return True
    else:
        return False

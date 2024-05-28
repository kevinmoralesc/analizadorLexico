def recognize_pattern_abrir(input_string):
    AutomataPattern = {
        'q0': {'{': 'q1', '[': 'q2'},
        'q1': {'{': 'q3'},
        'q2': {'[': 'q4'},
        'q3': {},  # Estado de aceptación para '{{'
        'q4': {},  # Estado de aceptación para '[['
    }

    current_state = 'q0'
    for char in input_string:
        if char in AutomataPattern[current_state]:
            current_state = AutomataPattern[current_state][char]
        else:
            return False  # Si el carácter no es válido para el estado actual, la cadena no es válida
    # Verificar si el último estado es un estado de aceptación
    if current_state in {'q3', 'q4'}:
        return True
    else:
        return False

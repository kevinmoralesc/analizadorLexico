import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter.ttk import Button, Frame, Scrollbar, Treeview
import re
import graphviz
from AutomataAritmetico import automata_operator
from AutomataOperadorRelacional import automata_operador
from AutomataOperadorLogico import automata_logico
from AutomataAbrir import recognize_pattern_abrir
from AutomataCierre import automata_cierre
from AutomataCliclos import automata_ciclo
from AutomataDesicion import automata_Desicion
from AutomataClase import automata_clase
from AutomataDato import automata_tipoDato

# Definición de los tokens
TOKEN_SPECIFICATION = [
    ('COMMENT', r'#\*\*.*'),  # Comentario de línea
    ('TER',   r'\?'),
    ('SEP',   r'\|'),
    ('NUMBER',   r'\d+(\.\d*)?'), 
    ('REL_OP',   r'(\.\.|/\.|\+\.-|\-\.|\+\.|\+|-)'),  # Modificado para incluir '-' como operador relacional
    ('ARITH_OP', r'(SUM|REST|MULT|DIV|POT|EXP)'),  # Operadores aritméticos
    ('ABR_OP',   r'(\{\{|\[\[)'),
    ('CR_OP',   r'(\}\}|\]\])'),
    ('LOG_OP',   r'(YY|OO|NN)'),
    ('CICLOS',   r'(INFINITE|CIRCLE)'),  # Operadores lógicos
    ('ASSIGN',   r'\.'),          # Operador de asignación modificado
    ('END',      r';'),           # Fin de la instrucción
    ('ID_VAR', r'\$[A-Za-z_]\w*'),  # Identificadores que inician con "$"
    ('ID_MET', r'\#[A-Za-z_]\w*'), 
    ('ID_CLASS', r'\%[A-Za-z_]\w*'), 
    ('ID', r'[A-Za-z_]\w*'),  # Modificado para capturar identificadores no precedidos por "$", "#" o "%"
    ('NEWLINE',  r'\n'),          # Línea nueva
    ('SKIP',     r'[ \t]+'),      # Espacios y tabuladores
    ('MISMATCH', r'.'),           # Cualquier otro carácter
]

# Compilar las expresiones regulares
token_re = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
get_token = re.compile(token_re).match

# Toma una cadena de caracteres como entrada y escanea esta cadena para 
# identificar y clasificar los diferentes tokens que encuentra según
# las especificaciones definidas en la lista
def escaner(characters):
    line_num = 1
    line_start = 0
    match = get_token(characters)
    tokens = []
    while match is not None:
        type = match.lastgroup
        if type == 'NEWLINE':
            line_start = match.end()
            line_num += 1
        elif type == 'SKIP':
            pass
        elif type == 'MISMATCH':
            raise RuntimeError(f'{characters[match.start()]} inesperado en la línea {line_num}')
        else:
            value = match.group(type)
            column = match.start() - line_start
            tokens.append((type, value, line_num, column))
        match = get_token(characters, match.end())
    if match is None:
        tokens.append(('EOF', '', line_num, 0))
    return tokens

# Toma un tipo de token y su valor como entrada y devuelve una 
# clasificación descriptiva del token 
def clasificar_token(type, value):
    if type == 'SEP':
        return 'Separador de sentencia'
    elif type == 'TER':
        return 'Símbolo terminal'
    elif type == 'COMMENT':
        return 'Comentario de línea'
    elif type == 'ID_VAR':
        return 'identificador variable'
    elif type == 'ID_MET':
        return 'identificador método'
    elif type == 'ID_CLASS':
        return 'identificador clase'
    elif type == 'ASSIGN':
        return 'operador de asignación'
    elif type == 'END':
        return 'fin de la instrucción ;'
    elif type == 'NUMBER':
        if '.' in value:
            return 'número decimal'
        else:
            return 'número entero'
    
    if automata_tipoDato(value):
        return 'palabra reservada tipo dato'
    elif automata_ciclo(value):
        return 'palabra reservada para ciclo'
    elif automata_Desicion(value):
        return 'palabra reservada para decisión'
    elif automata_clase(value):
        return 'palabra reservada para clase'
    elif automata_operator(value):
        return 'operador aritmético'
    elif automata_operador(value):
        return 'operador relacional'
    elif automata_logico(value):
        return 'operador lógico'
    elif recognize_pattern_abrir(value):
        return 'símbolo apertura'
    elif automata_cierre(value):
        return 'símbolo cierre'
    
    return 'Desconocido'

# Toma un texto como entrada y lo procesa línea por línea, identificando y clasificando
# los tokens encontrados en cada línea
def procesar_texto(data):
    tokens = []
    lines = data.split('\n')
    for line in lines:
        if line.startswith('#**'):
            tokens.append((line, 'COMMENT'))  # Comentario de línea
        elif re.match(r'^#[^\s]+', line):  # Verificar si la línea comienza con '#'
            match = re.match(r'^#([^\s]+)', line)  # Capturar el texto después del '#'
            if match:
                method_name = match.group(1)
                method_with_symbol = '#' + method_name  # Agregar el símbolo '#' al identificador de método
                tokens.append((method_with_symbol, 'ID_MET'))  # Identificador de método
        else:
            # Dividir la línea en palabras (tokens)
            words = line.split()
            for word in words:
                # Identificar y clasificar cada palabra
                if word.startswith('%'):
                    tokens.append((word, 'ID_CLASS'))  # Identificador de clase
                elif word.startswith('$'):
                    tokens.append((word, 'ID_VAR'))  # Identificador de variable
                elif word.isdigit():
                    tokens.append((word, 'NUMBER'))  # Número
                elif re.match(r'^\?$', word):
                    tokens.append((word, 'TER'))  # Símbolo terminal
                elif re.match(r'^\|\|$', word):
                    tokens.append((word, 'LOG_OP'))  # Operador lógico
                elif re.match(r'^\{', word):
                    tokens.append((word, 'ABR_OP'))  # Símbolo de apertura
                elif re.match(r'^\}', word):
                    tokens.append((word, 'CR_OP'))  # Símbolo de cierre
                else:
                    tokens.append((word, 'Desconocido'))  # Token desconocido
    return tokens

#Carga un archivo de texto para clasificar su contenido
def cargar_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, data)
            mostrar_texto()
            
# Limpia la tabla de visualización, obtiene el texto del widget text_box,
# lo procesa para extraer tokens y tipos de tokens, 
# y luego llama a una función para controlar esos tokens
def mostrar_texto():
    # Limpiar la tabla antes de actualizarla
    for item in tree.get_children():
        tree.delete(item)
    
    data = text_box.get(1.0, tk.END)
    tokens = procesar_texto(data)
    controlar_tokens(tokens)

# Recorre la lista de tokens y, para cada uno, determina su tipo utilizando 
# la función clasificar_token(type, token). 
# Luego, verifica si el tipo del token ya ha sido mostrado previamente en la tabla
def controlar_tokens(tokens):
    displayed_tokens = {}  # Diccionario para almacenar los tokens mostrados, agrupados por tipo
    for token, type in tokens:
        friendly_type = clasificar_token(type, token)
        if friendly_type not in displayed_tokens:
            displayed_tokens[friendly_type] = set()  # Inicializar un conjunto para cada tipo si es nuevo
        displayed_tokens[friendly_type].add(token)

    # Insertar tokens en la tabla
    for type, tokens_set in displayed_tokens.items():
        tokens_list = list(tokens_set)
        tokens_list.sort()  # Ordenar tokens para una mejor presentación en la tabla
        tree.insert("", "end", values=((", ").join(tokens_list), type))

#  Se encarga de generar autómatas para cada sesión de
#  tokens proporcionada en el diccionario tokens_por_sesion
def generar_automatas_por_sesiones(tokens_por_sesion):
    for sesion, tokens in tokens_por_sesion.items():
        if tokens:  # Verificar que haya tokens en la sesión
            dot = graphviz.Digraph(comment=f'Autómatas para la sesión de {sesion}')
            start_state = 'p0'
            processed_tokens = set()  # Conjunto para almacenar tokens ya procesados
            state_count = 0  # Contador para generar nombres de estado genéricos

            for token in tokens:
                if token not in processed_tokens:  # Verificar si el token ya ha sido procesado
                    transition_table = {}
                    accept_state = f'p{state_count}_accept'  # Estado de aceptación genérico

                    # Construir la tabla de transición para el autómata del token actual
                    previous_state = start_state
                    for i, char in enumerate(token):
                        current_state = f'p{state_count}_{i}'
                        if i == len(token) - 1:
                            transition_table[previous_state] = {char: accept_state}
                        else:
                            transition_table[previous_state] = {char: current_state}
                        previous_state = current_state

                    # Crear y renderizar el autómata para el token actual
                    crear_automata(transition_table, start_state, {accept_state}, f'Autómatas para {token}', dot)

                    processed_tokens.add(token)  # Agregar el token al conjunto de tokens procesados
                    state_count += 1  # Incrementar el contador de estados

            filename = f'Automatas/automatas_{sesion.replace(" ", "_").lower()}'
            dot.render(filename, format='png', cleanup=True)

# Esta función realiza el análisis léxico del texto ingresado, clasifica los tokens encontrados, 
# agrupa los tokens por categoría y genera autómatas para cada categoría de tokens.
def analizar_generar_automata():
    # Limpiar la tabla antes de actualizarla
    for item in tree.get_children():
        tree.delete(item)
    
    data = text_box.get(1.0, tk.END)
    tokens = procesar_texto(data)
    controlar_tokens(tokens)

    # Agrupar tokens por sesiones
    tokens_por_sesion = {
        'Comentario de línea': [],
        'operador aritmético': [],
        'operador relacional': [],
        'operador lógico': [],
        'operador de asignación': [],
        'símbolo apertura': [],
        'símbolo cierre': [],
        'Símbolo terminal': [],
        'Separador de sentencia': [],
        'palabra reservada para ciclo': [],
        'palabra reservada para decisión': [],
        'palabra reservada para clase': [],
        'identificador variable': [],
        'identificador método': [],
        'identificador clase': [],
        'palabra reservada tipo dato': []
    }

    # Clasificar tokens y agregarlos a sus sesiones correspondientes
    for token, categoria in tokens:
        clasificacion = clasificar_token(categoria, token)
        if clasificacion in tokens_por_sesion:
            tokens_por_sesion[clasificacion].append(token)

    # Generar y mostrar los autómatas por sesiones
    generar_automatas_por_sesiones(tokens_por_sesion)

# Función para crear un autómata 
def crear_automata(transition_table, start_state, accept_states, title, dot):
    for state, transitions in transition_table.items():
        for symbol, next_state in transitions.items():
            dot.edge(state, next_state, label=symbol)

    for state in accept_states:
        dot.node(state, shape='doublecircle')

    dot.node(start_state, shape='circle')


# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Analizador Léxico")

frame = Frame(root)
frame.pack(pady=10, padx=10)

btn_load = Button(frame, text="Cargar Archivo", command=cargar_archivo)
btn_load.pack(side=tk.LEFT, padx=5)

btn_analyze = Button(frame, text="Analizar Texto", command=mostrar_texto)
btn_analyze.pack(side=tk.LEFT, padx=5)

btn_generate_automatas = Button(frame, text="Generar Autómatas", command=analizar_generar_automata)
btn_generate_automatas.pack(side=tk.LEFT, padx=5)

text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
text_box.pack(pady=10, padx=10)

# Crear el Treeview para mostrar los tokens
tree_frame = Frame(root)
tree_frame.pack(pady=10, padx=10)

tree_columns = ("Valor", "Clasificación")
tree = Treeview(tree_frame, columns=tree_columns, show="headings")
tree.heading("Valor", text="Valor")
tree.heading("Clasificación", text="Clasificación")
tree.pack(side=tk.LEFT, fill=tk.BOTH)

# Añadir scrollbar
scrollbar = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
tree.configure(yscrollcommand=scrollbar.set)

root.mainloop()

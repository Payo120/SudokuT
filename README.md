# SudokuT
🎲 Juego de Sudoku con Python y Tkinter
Este proyecto es una aplicación de escritorio interactiva para jugar Sudoku, desarrollada en Python utilizando la biblioteca gráfica tkinter. Permite a los usuarios solicitar la generación de nuevos puzzles de diferentes dificultades, introducir sus propias soluciones, y verificar su progreso.

✨ Características
Generación de Puzzles: Crea Sudokus completamente nuevos con una solución única garantizada.

Niveles de Dificultad: Elige entre Fácil, Medio y Difícil, que ajustan la cantidad de números pre-rellenados.

Interfaz Gráfica (GUI): Desarrollada con tkinter para una experiencia de usuario intuitiva.

Validación de Entrada: Solo permite la introducción de números del 1 al 9 en las celdas editables.

Feedback Visual: Resalta en rojo los números introducidos por el usuario que violan las reglas del Sudoku en su fila, columna o bloque 3x3.

Funcionalidades del Juego:

"Resolver": Muestra la solución completa del Sudoku.

"Reiniciar": Restablece el tablero a su estado inicial, borrando las entradas del usuario.

"Comprobar": Verifica si la solución actual del usuario es correcta y muestra un mensaje de victoria o error.

🚀 Instalación
Para ejecutar este juego, solo necesitas tener Python instalado en tu sistema.

Asegúrate de tener Python: Si no lo tienes, puedes descargarlo desde python.org.

Tkinter:
tkinter suele venir incluido con las instalaciones estándar de Python. No deberías necesitar instalarlo por separado.

Descarga el código:
Guarda el código proporcionado en un archivo llamado, por ejemplo, sudoku_app.py.

🎮 Uso
Para iniciar el juego, abre una terminal o línea de comandos, navega hasta el directorio donde guardaste sudoku_app.py y ejecuta el siguiente comando:

python sudoku_app.py

Interacción en el Juego:
Botones de Dificultad (Fácil, Medio, Difícil): Haz clic en uno para generar un nuevo puzzle con la dificultad seleccionada.

Celdas del Tablero:

Las celdas con números negros son las pistas iniciales y no se pueden editar.

Las celdas vacías (o con números azules/rojos) son editables. Haz clic en ellas y escribe un número del 1 al 9.

Si introduces un número que rompe las reglas, se pondrá en rojo.

Botón "Resolver": Rellena el tablero con la solución correcta y cambia el color de las celdas resueltas.

Botón "Reiniciar": Borra todas tus entradas y devuelve el tablero al estado inicial del puzzle.

Botón "Comprobar": Verifica si tu solución actual es correcta. Si el tablero está lleno y es correcto, te felicitará. Si no, te indicará que hay errores o que el tablero está incompleto.

📂 Estructura del Código
El proyecto está organizado en dos clases principales:

SudokuGenerator: Contiene toda la lógica para generar un Sudoku completo, validar números en el tablero y contar el número de soluciones posibles (para asegurar la unicidad del puzzle).

SudokuApp: Gestiona la interfaz gráfica de usuario (GUI) utilizando tkinter, maneja la interacción del usuario con el tablero y los botones, y coordina las llamadas a SudokuGenerator.

# QA Project: Urban Routes (qa-project-Urban-Routes-es)

## Descripción del proyecto
Este proyecto contiene un conjunto de pruebas automatizadas diseñadas para validar diversas funcionalidades de la aplicación Urban Routes. Las pruebas verifican flujos clave como la selección de rutas, modos de transporte, ingreso de datos, y funcionalidades adicionales como pedir helados y mantas.

## Tecnologías y técnicas utilizadas
- **Python**: Lenguaje principal para la automatización.
- **Selenium WebDriver**: Para interactuar con la interfaz gráfica de la aplicación.
- **Pytest**: Framework para la ejecución y manejo de pruebas.
- **Espera explícita e implícita**: Utilizadas para sincronizar las pruebas con el estado de los elementos en la aplicación.

## Estructura del proyecto
```
qa-project-Urban-Routes-es/
├── main.py                   # Archivo principal de las pruebas
├── pages.py                  # Contiene las clases y métodos relacionados con las páginas
├── data.py                   # Configuración y datos como URL o credenciales
├── README.md                 # Documentación del proyecto
```

## Instrucciones para ejecutar las pruebas

1. **Clonar el repositorio**:
   ```bash
   git clone <url_del_repositorio>
   ```

2. **Configurar el archivo `data.py`**:
   Modifica el archivo `data.py` para incluir la URL de la aplicación y otros datos relevantes como direcciones o números de teléfono para las pruebas.

3. **Ejecutar las pruebas**:
   Ejecuta las pruebas usando `pytest`:
   ```bash
   pytest tests/test_urban_routes.py
   ```
   
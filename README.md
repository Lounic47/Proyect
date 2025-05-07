# Optimizador de Equipo de Escalada 🏔️

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0.x-%23000.svg?logo=flask)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1-%23563D7C.svg?logo=bootstrap)](https://getbootstrap.com/)

Aplicación web para determinar la combinación óptima de elementos de escalada, optimizando peso y calorías.

![Demo Interface](/screenshots/demo.png) <!-- Añade captura en /screenshots/demo.png -->

## 🚀 Características

- **Algoritmo Avanzado**: Resuelve el problema de la mochila con programación dinámica
- **Interfaz Intuitiva**: Formulario interactivo con validación en tiempo real
- **Persistencia de Datos**: SQLite para historial de cálculos
- **Principios SOLID**: Código mantenible y escalable
- **Multiplataforma**: Funciona en Windows, Linux y macOS

## ⚙️ Requisitos

- Python 3.8+
- pip
- Navegador web moderno

## 🛠️ Instalación

```bash
# Clonar repositorio
git clone https://github.com/TuUsuario/optimizador-riesgo.git
cd optimizador-riesgo

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py

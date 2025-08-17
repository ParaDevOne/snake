#!/usr/bin/env python3
"""
Setup script para construir el ejecutable del juego Snake.
Desarrollado por ParaDevOne - Snake Game v1.4.0

Este script utiliza PyInstaller para crear un ejecutable independiente
del juego Snake con todas sus dependencias incluidas.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


class Colors:
    """Colores para output en consola."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_colored(message, color=Colors.ENDC):
    """Imprime mensaje con color si la terminal lo soporta."""
    system = platform.system()
    if system == "Windows":
        # Habilitar colores en Windows 10+
        try:
            os.system("color")
        except ImportError:
            # Si falla, continuar sin colores
            pass
    print(f"{color}{message}{Colors.ENDC}")


def clean_build_files():
    """Limpia archivos y carpetas de builds anteriores."""
    print_colored("🧹 Limpiando archivos de builds anteriores...", Colors.OKCYAN)

    folders_to_clean = ["build", "dist", "__pycache__"]
    cleaned_items = []

    # Limpiar carpetas
    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                if os.path.isdir(folder):
                    shutil.rmtree(folder)
                    cleaned_items.append(f"📁 {folder}/")
                else:
                    os.remove(folder)
                    cleaned_items.append(f"📄 {folder}")
            except PermissionError:
                print_colored(
                    f"⚠️  No se pudo eliminar {folder} (permisos)", Colors.WARNING
                )
            except ImportError as e:
                print_colored(f"❌ Error eliminando {folder}: {e}", Colors.FAIL)

    # Limpiar archivos .spec
    for spec_file in Path(".").glob("*.spec"):
        try:
            spec_file.unlink()
            cleaned_items.append(f"📄 {spec_file}")
        except ImportError as e:
            print_colored(f"❌ Error eliminando {spec_file}: {e}", Colors.FAIL)

    # Limpiar archivos .pyc recursivamente
    for pyc_file in Path(".").rglob("*.pyc"):
        try:
            pyc_file.unlink()
            cleaned_items.append(f"📄 {pyc_file}")
        except ImportError as e:
            print_colored(f"❌ Error eliminando {pyc_file}: {e}", Colors.FAIL)

    if cleaned_items:
        print_colored(
            f"✅ Limpieza completada. Eliminados {len(cleaned_items)} elementos.",
            Colors.OKGREEN,
        )
    else:
        print_colored("✅ No hay archivos que limpiar.", Colors.OKGREEN)


def check_dependencies():
    """Verifica que PyInstaller esté instalado."""
    print_colored("🔍 Verificando dependencias...", Colors.OKCYAN)

    try:
        # Verificar PyInstaller mediante subprocess para evitar import directo
        result = subprocess.run(
            ["pyinstaller", "--version"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print_colored(f"✅ PyInstaller {version} encontrado.", Colors.OKGREEN)
            return True
        else:
            raise FileNotFoundError("PyInstaller no encontrado")
    except (FileNotFoundError, subprocess.SubprocessError):
        print_colored(
            "❌ PyInstaller no está instalado o no está en PATH.", Colors.FAIL
        )
        print_colored("💡 Instálalo con: pip install pyinstaller", Colors.WARNING)
        return False


def check_main_file():
    """Verifica que el archivo main.py exista."""
    if not os.path.exists("main.py"):
        print_colored("❌ Archivo main.py no encontrado.", Colors.FAIL)
        print_colored(
            "💡 Asegúrate de estar en el directorio correcto del proyecto.",
            Colors.WARNING,
        )
        return False
    print_colored("✅ Archivo main.py encontrado.", Colors.OKGREEN)
    return True


def create_build_directory():
    """Crea el directorio de salida si no existe."""
    output_dir = Path("dist")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def build_executable():
    """Construye el ejecutable usando PyInstaller."""
    print_colored("🔨 Iniciando construcción del ejecutable...", Colors.HEADER)

    # Configuración específica por sistema operativo
    system = platform.system()

    if system == "Windows":
        exe_name = "SnakeGame.exe"
        separator = ";"
    elif system == "Darwin":  # macOS
        exe_name = "SnakeGame"
        separator = ":"
    else:  # Linux y otros Unix-like
        exe_name = "SnakeGame"
        separator = ":"

    # Configuración base de PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",  # Un solo archivo ejecutable
        "--windowed",  # Sin ventana de consola
        "--name",
        exe_name,  # Nombre del ejecutable
        "--clean",  # Limpiar cache
        "--noconfirm",  # No pedir confirmación
        "--distpath",
        "dist",  # Directorio de salida
        "--workpath",
        "build",  # Directorio de trabajo
    ]

    # Agregar icono si existe (específico por SO)
    icon_files = {
        "Windows": "icon.ico",
        "Darwin": "icon.icns",  # macOS usa .icns
        "Linux": "icon.png",  # Linux puede usar .png
    }

    icon_file = icon_files.get(system, "icon.ico")
    if os.path.exists(icon_file):
        cmd.extend(["--icon", icon_file])
        print_colored(f"🎨 Usando icono: {icon_file}", Colors.OKBLUE)

    # Configuraciones específicas por SO
    if system == "Darwin":  # macOS
        cmd.extend(
            [
                "--osx-bundle-identifier",
                "com.paradevone.snakegame",
                "--target-arch",
                "universal2",  # Soporte para Intel y Apple Silicon
            ]
        )
    elif system == "Linux":
        # En Linux, asegurar que el ejecutable tenga permisos
        cmd.extend(["--strip"])  # Reducir tamaño removiendo símbolos de debug

    # Datos adicionales si existen
    data_folders = ["Data", "assets", "sounds", "images", "fonts", "config"]
    for folder in data_folders:
        if os.path.exists(folder):
            cmd.extend(["--add-data", f"{folder}{separator}{folder}"])
            print_colored(f"📦 Incluyendo carpeta: {folder}", Colors.OKBLUE)

    # Agregar archivo principal
    cmd.append("main.py")

    print_colored(f"🚀 Ejecutando: {' '.join(cmd)}", Colors.OKBLUE)
    print_colored("⏳ Esto puede tomar unos minutos...", Colors.WARNING)

    try:
        # Ejecutar PyInstaller
        process_result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Verificar que el proceso terminó correctamente
        if process_result.returncode == 0:
            print_colored("✅ Construcción exitosa!", Colors.OKGREEN)

            # En Linux/macOS, asegurar permisos de ejecución
            if system in ["Linux", "Darwin"]:
                exe_path = Path("dist") / exe_name
                if exe_path.exists():
                    os.chmod(exe_path, 0o755)  # rwxr-xr-x
                    print_colored(
                        "🔐 Permisos de ejecución configurados", Colors.OKGREEN
                    )

            return True
        else:
            print_colored(
                f"❌ PyInstaller terminó con código: {process_result.returncode}",
                Colors.FAIL,
            )
            return False

    except subprocess.CalledProcessError as e:
        print_colored("❌ Error durante la construcción:", Colors.FAIL)
        print_colored(f"Código de salida: {e.returncode}", Colors.FAIL)
        if e.stdout:
            print_colored("STDOUT:", Colors.WARNING)
            print(e.stdout)
        if e.stderr:
            print_colored("STDERR:", Colors.WARNING)
            print(e.stderr)
        return False
    except FileNotFoundError:
        print_colored("❌ PyInstaller no encontrado en PATH", Colors.FAIL)
        print_colored("💡 Instálalo con: pip install pyinstaller", Colors.WARNING)
        return False


def show_build_info():
    """Muestra información del ejecutable creado."""
    dist_dir = Path("dist")
    if not dist_dir.exists():
        return

    print_colored("\n📊 Información del build:", Colors.HEADER)
    print_colored("=" * 50, Colors.HEADER)

    system = platform.system()
    system_names = {"Windows": "🪟 Windows", "Darwin": "🍎 macOS", "Linux": "🐧 Linux"}

    print_colored(
        f"💻 Sistema: {system_names.get(system, f'🖥️ {system}')}", Colors.OKBLUE
    )
    print_colored(f"🏗️ Arquitectura: {platform.machine()}", Colors.OKBLUE)

    for exe_file in dist_dir.glob("*"):
        if exe_file.is_file() and not exe_file.name.startswith("."):
            size_mb = exe_file.stat().st_size / (1024 * 1024)
            print_colored(f"📄 Archivo: {exe_file.name}", Colors.OKGREEN)
            print_colored(f"📏 Tamaño: {size_mb:.2f} MB", Colors.OKBLUE)
            print_colored(f"📍 Ubicación: {exe_file.absolute()}", Colors.OKBLUE)

            # Verificar si es ejecutable
            is_executable = False
            if system == "Windows" and exe_file.suffix == ".exe":
                is_executable = True
            elif system in ["Linux", "Darwin"] and os.access(exe_file, os.X_OK):
                is_executable = True

            if is_executable:
                print_colored("✅ Ejecutable listo para usar", Colors.OKGREEN)

                # Instrucciones específicas por SO
                if system == "Windows":
                    print_colored(
                        "💡 Ejecutar con: .\\dist\\SnakeGame.exe", Colors.OKCYAN
                    )
                else:
                    print_colored("💡 Ejecutar con: ./dist/SnakeGame", Colors.OKCYAN)


def main():
    """Función principal del script de setup."""
    print_colored("🐍 Snake Game - Build Script v1.4.0", Colors.HEADER)
    print_colored("🔧 Desarrollado por ParaDevOne", Colors.HEADER)
    print_colored("=" * 50, Colors.HEADER)

    # Verificaciones previas
    if not check_main_file():
        sys.exit(1)

    if not check_dependencies():
        sys.exit(1)

    # Proceso de construcción
    try:
        clean_build_files()
        create_build_directory()

        if build_executable():
            show_build_info()
            print_colored("\n🎉 ¡Build completado exitosamente!", Colors.OKGREEN)
            print_colored(
                "🚀 Tu ejecutable está listo en la carpeta 'dist/'", Colors.OKGREEN
            )
        else:
            print_colored("\n❌ Build falló. Revisa los errores arriba.", Colors.FAIL)
            sys.exit(1)

    except KeyboardInterrupt:
        print_colored("\n⏹️  Build cancelado por el usuario.", Colors.WARNING)
        sys.exit(1)
    except ImportError as e:
        print_colored(f"\n❌ Error inesperado: {e}", Colors.FAIL)
        sys.exit(1)


if __name__ == "__main__":
    main()

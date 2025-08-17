#!/usr/bin/env python3
"""
Setup script para construir el ejecutable del juego Snake.
Desarrollado por ParaDevOne - Snake Game v1.5.0

Este script utiliza PyInstaller para crear un ejecutable independiente
del juego Snake con todas sus dependencias incluidas.
Incluye soporte para UPX local en Windows (lib/upx.exe).
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


class Colors:
    """Colores para output en consola."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
                print_colored(f"⚠️  No se pudo eliminar {folder} (permisos)", Colors.WARNING)
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
        print_colored(f"✅ Limpieza completada. Eliminados {len(cleaned_items)} elementos.", Colors.OKGREEN)
    else:
        print_colored("✅ No hay archivos que limpiar.", Colors.OKGREEN)


def check_dependencies():
    """Verifica que PyInstaller y UPX estén disponibles."""
    print_colored("🔍 Verificando dependencias...", Colors.OKCYAN)

    dependencies_ok = True

    # Verificar PyInstaller
    try:
        result = subprocess.run(["pyinstaller", "--version"],
                                capture_output=True, text=True, check=False)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_colored(f"✅ PyInstaller {version} encontrado.", Colors.OKGREEN)
        else:
            raise FileNotFoundError("PyInstaller no encontrado")
    except (FileNotFoundError, subprocess.SubprocessError):
        print_colored("❌ PyInstaller no está instalado o no está en PATH.", Colors.FAIL)
        print_colored("💡 Instálalo con: pip install pyinstaller", Colors.WARNING)
        dependencies_ok = False

    # Verificar UPX (primero en lib/, luego en PATH)
    upx_path = None
    system = platform.system()

    # Buscar UPX local en carpeta lib/ (solo Windows)
    if system == "Windows":
        local_upx = Path("lib") / "upx.exe"
        if local_upx.exists():
            try:
                result = subprocess.run([str(local_upx), "--version"],
                                        capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0] if result.stdout else "upx"
                    print_colored(f"✅ UPX local encontrado: {version_line}", Colors.OKGREEN)
                    print_colored(f"📂 Ubicación: {local_upx.absolute()}", Colors.OKBLUE)
                    return dependencies_ok, str(local_upx.absolute())
            except ImportError as e:
                print_colored(f"⚠️  UPX local no funciona: {e}", Colors.WARNING)

    # Si no hay UPX local o no es Windows, buscar en PATH
    try:
        upx_cmd = "upx.exe" if system == "Windows" else "upx"
        result = subprocess.run([upx_cmd, "--version"],
                                capture_output=True, text=True, check=False)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0] if result.stdout else "upx"
            print_colored(f"✅ UPX del sistema encontrado: {version_line}", Colors.OKGREEN)
            return dependencies_ok, upx_cmd
        else:
            raise FileNotFoundError("UPX no encontrado en PATH")
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    # UPX no encontrado
    print_colored("⚠️  UPX no está disponible - el ejecutable será más grande", Colors.WARNING)

    if system == "Windows":
        print_colored("💡 Para usar UPX en Windows:", Colors.WARNING)
        print_colored("   1. Descarga UPX desde: https://upx.github.io/", Colors.OKCYAN)
        print_colored("   2. Extrae upx.exe a la carpeta 'lib/' del proyecto", Colors.OKCYAN)
        print_colored("   3. O instálalo globalmente con:", Colors.OKCYAN)
        print_colored("      - Scoop: scoop install upx", Colors.OKCYAN)
        print_colored("      - Chocolatey: choco install upx", Colors.OKCYAN)
    else:
        print_colored("💡 Para instalar UPX:", Colors.WARNING)
        if system == "Darwin":  # macOS
            print_colored("   - Homebrew: brew install upx", Colors.OKCYAN)
            print_colored("   - MacPorts: sudo port install upx", Colors.OKCYAN)
        else:  # Linux
            print_colored("   - Ubuntu/Debian: sudo apt install upx-ucl", Colors.OKCYAN)
            print_colored("   - Fedora: sudo dnf install upx", Colors.OKCYAN)
            print_colored("   - Arch: sudo pacman -S upx", Colors.OKCYAN)

    return dependencies_ok, None


def check_main_file():
    """Verifica que el archivo main.py exista."""
    if not os.path.exists("main.py"):
        print_colored("❌ Archivo main.py no encontrado.", Colors.FAIL)
        print_colored("💡 Asegúrate de estar en el directorio correcto del proyecto.", Colors.WARNING)
        return False
    print_colored("✅ Archivo main.py encontrado.", Colors.OKGREEN)
    return True


def create_lib_directory():
    """Crea el directorio lib/ si no existe y muestra información."""
    lib_dir = Path("lib")

    if not lib_dir.exists():
        lib_dir.mkdir(exist_ok=True)
        print_colored("📁 Directorio 'lib/' creado", Colors.OKGREEN)

        # Solo mostrar información en Windows
        if platform.system() == "Windows":
            print_colored("💡 Para usar UPX local en Windows:", Colors.OKCYAN)
            print_colored("   1. Descarga UPX desde: https://upx.github.io/", Colors.OKCYAN)
            print_colored("   2. Extrae 'upx.exe' a la carpeta 'lib/'", Colors.OKCYAN)
            print_colored("   3. Vuelve a ejecutar este script", Colors.OKCYAN)

    return lib_dir


def create_build_directory():
    """Crea el directorio de salida si no existe."""
    output_dir = Path("dist")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def build_executable(upx_path=None):
    """Construye el ejecutable usando PyInstaller y opcionalmente UPX."""
    print_colored("🔨 Iniciando construcción del ejecutable...", Colors.HEADER)

    # Configuración específica por sistema operativo
    system = platform.system()

    if system == "Windows":
        exe_name = "Snake Game.exe"
        separator = ";"
    elif system == "Darwin":  # macOS
        exe_name = "Snake Game"
        separator = ":"
    else:  # Linux y otros Unix-like
        exe_name = "Snake Game"
        separator = ":"

    # Configuración base de PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin ventana de consola
        "--name", exe_name,             # Nombre del ejecutable
        "--clean",                      # Limpiar cache
        "--noconfirm",                  # No pedir confirmación
        "--distpath", "dist",           # Directorio de salida
        "--workpath", "build",          # Directorio de trabajo
        "--optimize", "2",              # Optimización máxima de Python
    ]

    # Configurar UPX si está disponible
    if upx_path:
        if system == "Windows" and upx_path.endswith("upx.exe"):
            # UPX local en Windows - configurar directorio
            upx_dir = str(Path(upx_path).parent)
            cmd.extend([
                "--upx-dir", upx_dir,       # Directorio donde está upx.exe
                "--upx-exclude", "vcruntime140.dll",  # Excluir DLLs problemáticas
                "--upx-exclude", "api-ms-*.dll",      # Excluir DLLs del sistema
                "--upx-exclude", "msvcp140.dll",      # Excluir más DLLs de Visual C++
            ])
            print_colored(f"📦 UPX local configurado: {upx_dir}", Colors.OKGREEN)
        else:
            # UPX del sistema
            cmd.extend([
                "--upx-dir", ".",           # Buscar UPX en PATH
            ])
            if system == "Windows":
                cmd.extend([
                    "--upx-exclude", "vcruntime140.dll",
                    "--upx-exclude", "api-ms-*.dll",
                ])
            else:
                cmd.extend([
                    "--upx-exclude", "libc.so.*",
                ])
            print_colored("📦 UPX del sistema configurado", Colors.OKGREEN)

        print_colored("🗜️  El ejecutable será comprimido con UPX", Colors.OKGREEN)
    else:
        cmd.append("--noupx")           # Explícitamente deshabilitar UPX
        print_colored("📦 UPX deshabilitado - ejecutable sin comprimir", Colors.WARNING)

    # Agregar icono si existe (específico por SO)
    icon_files = {
        "Windows": ["icon.ico", "assets/icon.ico"],
        "Darwin": ["icon.icns", "assets/icon.icns"],  # macOS usa .icns
        "Linux": ["icon.png", "assets/icon.png"]      # Linux puede usar .png
    }

    icon_found = False
    for icon_file in icon_files.get(system, ["icon.ico"]):
        if os.path.exists(icon_file):
            cmd.extend(["--icon", icon_file])
            print_colored(f"🎨 Usando icono: {icon_file}", Colors.OKBLUE)
            icon_found = True
            break

    if not icon_found:
        print_colored("ℹ️  No se encontró icono específico para el SO", Colors.OKCYAN)

    # Configuraciones específicas por SO
    if system == "Darwin":  # macOS
        cmd.extend([
            "--osx-bundle-identifier", "com.paradevone.snakegame",
            "--target-arch", "universal2"  # Soporte para Intel y Apple Silicon
        ])
        print_colored("🍎 Configuración macOS: Bundle universal", Colors.OKBLUE)
    elif system == "Linux":
        # En Linux, optimizaciones adicionales
        cmd.extend([
            "--strip",                  # Reducir tamaño removiendo símbolos de debug
            "--exclude-module", "_tkinter",  # Excluir módulos innecesarios
        ])
        print_colored("🐧 Configuración Linux: Strip + optimizaciones", Colors.OKBLUE)
    elif system == "Windows":
        # Optimizaciones específicas para Windows
        cmd.extend([
            "--exclude-module", "_tkinter",      # Excluir tkinter
            "--exclude-module", "matplotlib",   # Excluir matplotlib si no se usa
            "--exclude-module", "numpy",        # Excluir numpy si no se usa (snake no lo necesita)
        ])
        print_colored("🪟 Configuración Windows: Exclusiones optimizadas", Colors.OKBLUE)

    # Datos adicionales si existen
    data_folders = ["Data", "assets", "sounds", "images", "fonts", "config"]
    included_folders = []
    for folder in data_folders:
        if os.path.exists(folder) and os.path.isdir(folder):
            # Verificar que la carpeta no esté vacía
            try:
                if any(Path(folder).iterdir()):
                    cmd.extend(["--add-data", f"{folder}{separator}{folder}"])
                    included_folders.append(folder)
            except (OSError, PermissionError):
                print_colored(f"⚠️  No se puede acceder a la carpeta {folder}", Colors.WARNING)

    # No incluir lib/ si contiene UPX local
    lib_folder = "lib"
    if os.path.exists(lib_folder) and os.path.isdir(lib_folder):
        if not (upx_path and upx_path.startswith(str(Path(lib_folder).absolute()))):
            try:
                if any(Path(lib_folder).iterdir()):
                    cmd.extend(["--add-data", f"{lib_folder}{separator}{lib_folder}"])
                    included_folders.append(lib_folder)
            except (OSError, PermissionError):
                print_colored(f"⚠️  No se puede acceder a la carpeta {lib_folder}", Colors.WARNING)
        else:
            print_colored(f"⏭️  Excluyendo carpeta lib (contiene UPX local)", Colors.OKCYAN)

    if included_folders:
        print_colored(f"📦 Carpetas incluidas: {', '.join(included_folders)}", Colors.OKBLUE)

    # Agregar archivo principal
    cmd.append("main.py")

    print_colored(f"🚀 Comando PyInstaller:", Colors.OKBLUE)
    print_colored(f"   {' '.join(cmd[:5])} ... [+{len(cmd)-5} argumentos más]", Colors.OKCYAN)
    print_colored("⏳ Esto puede tomar varios minutos...", Colors.WARNING)
    if upx_path:
        print_colored("⏳ UPX añadirá tiempo extra de compresión...", Colors.WARNING)

    try:
        # Ejecutar PyInstaller con timeout
        print_colored("🔄 Iniciando PyInstaller...", Colors.OKCYAN)
        process_result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minutos máximo
        )

        # Verificar que el proceso terminó correctamente
        if process_result.returncode == 0:
            print_colored("✅ PyInstaller completado exitosamente!", Colors.OKGREEN)

            # En Linux/macOS, asegurar permisos de ejecución
            if system in ["Linux", "Darwin"]:
                exe_path = Path("dist") / exe_name
                if exe_path.exists():
                    os.chmod(exe_path, 0o755)  # rwxr-xr-x
                    print_colored("🔐 Permisos de ejecución configurados", Colors.OKGREEN)

            # Mostrar información de compresión UPX si se usó
            if upx_path and process_result.stdout:
                upx_lines = [line for line in process_result.stdout.split('\n')
                            if 'upx' in line.lower() and ('compressed' in line.lower() or 'packed' in line.lower())]
                if upx_lines:
                    print_colored("📊 Información de compresión UPX:", Colors.OKBLUE)
                    for line in upx_lines[-2:]:  # Mostrar últimas 2 líneas relevantes
                        if line.strip():
                            print_colored(f"   {line.strip()}", Colors.OKCYAN)

            return True
        else:
            print_colored(f"❌ PyInstaller terminó con código: {process_result.returncode}", Colors.FAIL)
            return False

    except subprocess.TimeoutExpired:
        print_colored("❌ PyInstaller excedió el tiempo límite (30 min)", Colors.FAIL)
        print_colored("💡 Intenta sin UPX o con menos optimizaciones", Colors.WARNING)
        return False
    except subprocess.CalledProcessError as e:
        print_colored("❌ Error durante la construcción:", Colors.FAIL)
        print_colored(f"Código de salida: {e.returncode}", Colors.FAIL)

        # Verificar si el error es relacionado con UPX
        if upx_path and e.stderr:
            error_lower = e.stderr.lower()
            if any(word in error_lower for word in ['upx', 'compress', 'pack']):
                print_colored("🔄 Error relacionado con UPX - intentando sin compresión...", Colors.WARNING)
                return build_executable(upx_path=None)  # Reintentar sin UPX

        if e.stdout:
            print_colored("STDOUT (últimas líneas):", Colors.WARNING)
            stdout_lines = e.stdout.strip().split('\n')
            for line in stdout_lines[-10:]:  # Mostrar últimas 10 líneas
                if line.strip():
                    print_colored(f"  {line}", Colors.OKCYAN)
        if e.stderr:
            print_colored("STDERR (últimas líneas):", Colors.WARNING)
            stderr_lines = e.stderr.strip().split('\n')
            for line in stderr_lines[-10:]:  # Mostrar últimas 10 líneas
                if line.strip():
                    print_colored(f"  {line}", Colors.OKCYAN)
        return False
    except FileNotFoundError:
        print_colored("❌ PyInstaller no encontrado en PATH", Colors.FAIL)
        print_colored("💡 Instálalo con: pip install pyinstaller", Colors.WARNING)
        return False
    except ImportError as e:
        print_colored(f"❌ Error inesperado durante la construcción: {e}", Colors.FAIL)
        return False


def show_build_info():
    """Muestra información del ejecutable creado."""
    dist_dir = Path("dist")
    if not dist_dir.exists():
        return

    print_colored("\n📊 Información del build:", Colors.HEADER)
    print_colored("=" * 50, Colors.HEADER)

    system = platform.system()
    system_names = {
        "Windows": "🪟 Windows",
        "Darwin": "🍎 macOS",
        "Linux": "🐧 Linux"
    }

    print_colored(f"💻 Sistema: {system_names.get(system, f'🖥️ {system}')}", Colors.OKBLUE)
    print_colored(f"🏗️ Arquitectura: {platform.machine()}", Colors.OKBLUE)

    for exe_file in dist_dir.glob("*"):
        if exe_file.is_file() and not exe_file.name.startswith('.'):
            size_bytes = exe_file.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            size_kb = size_bytes / 1024

            # Mostrar tamaño en formato apropiado
            if size_mb >= 1:
                size_str = f"{size_mb:.2f} MB"
            else:
                size_str = f"{size_kb:.1f} KB"

            print_colored(f"📄 Archivo: {exe_file.name}", Colors.OKGREEN)
            print_colored(f"📏 Tamaño: {size_str} ({size_bytes:,} bytes)", Colors.OKBLUE)
            print_colored(f"📍 Ubicación: {exe_file.absolute()}", Colors.OKBLUE)

            # Verificar si es ejecutable
            is_executable = False
            if system == "Windows" and exe_file.suffix == '.exe':
                is_executable = True
            elif system in ["Linux", "Darwin"] and os.access(exe_file, os.X_OK):
                is_executable = True

            if is_executable:
                print_colored("✅ Ejecutable listo para usar", Colors.OKGREEN)

                # Calcular ratio de compresión estimado
                if size_mb < 20:  # Típico para ejecutables con UPX
                    print_colored("🗜️  Ejecutable probablemente comprimido con UPX", Colors.OKCYAN)
                    estimated_original = size_mb * 2.5  # UPX típicamente comprime ~60%
                    print_colored(f"📈 Tamaño estimado sin UPX: ~{estimated_original:.1f} MB", Colors.OKCYAN)
                    print_colored(f"💾 Espacio ahorrado: ~{estimated_original - size_mb:.1f} MB", Colors.OKGREEN)

                # Instrucciones específicas por SO
                if system == "Windows":
                    print_colored("💡 Ejecutar con: .\\dist\\SnakeGame.exe", Colors.OKCYAN)
                    print_colored("💡 O hacer doble click en el archivo", Colors.OKCYAN)
                else:
                    print_colored("💡 Ejecutar con: ./dist/SnakeGame", Colors.OKCYAN)
                    print_colored("💡 O desde terminal: cd dist && ./SnakeGame", Colors.OKCYAN)

    # Información adicional sobre UPX
    print_colored("\n🛠️  Notas sobre UPX:", Colors.HEADER)
    if platform.system() == "Windows":
        lib_upx = Path("lib") / "upx.exe"
        if lib_upx.exists():
            print_colored("✅ UPX local disponible en lib/upx.exe", Colors.OKGREEN)
        else:
            print_colored("💡 Para usar UPX local: coloca upx.exe en lib/", Colors.OKCYAN)

    print_colored("   • Reduce significativamente el tamaño del ejecutable", Colors.OKCYAN)
    print_colored("   • Puede aumentar ligeramente el tiempo de inicio", Colors.OKCYAN)
    print_colored("   • Algunos antivirus pueden marcar falsos positivos", Colors.WARNING)
    print_colored("   • El ejecutable se descomprime automáticamente al ejecutarse", Colors.OKCYAN)


def main():
    """Función principal del script de setup."""
    print_colored("🐍 Snake Game - Build Script v1.5.0", Colors.HEADER)
    print_colored("🔧 Desarrollado por ParaDevOne", Colors.HEADER)
    print_colored("=" * 50, Colors.HEADER)

    # Solo mostrar información de UPX en Windows
    system = platform.system()
    if system == "Windows":
        print_colored("💡 En Windows: UPX se busca primero en lib/upx.exe", Colors.OKCYAN)
        print_colored("   Si no está ahí, se busca en PATH del sistema", Colors.OKCYAN)
    else:
        print_colored("💡 En este SO: UPX se busca en PATH del sistema", Colors.OKCYAN)

    print_colored("-" * 50, Colors.OKCYAN)

    # Verificaciones previas
    if not check_main_file():
        sys.exit(1)

    pyinstaller_ok, upx_path = check_dependencies()
    if not pyinstaller_ok:
        sys.exit(1)

    # Proceso de construcción
    try:
        clean_build_files()
        create_lib_directory()  # Crear directorio lib/ si no existe
        create_build_directory()

        if build_executable(upx_path=upx_path):
            show_build_info()
            print_colored("\n🎉 ¡Build completado exitosamente!", Colors.OKGREEN)
            print_colored("🚀 Tu ejecutable está listo en la carpeta 'dist/'", Colors.OKGREEN)

            if upx_path:
                if system == "Windows" and "lib" in upx_path:
                    print_colored("🗜️  Ejecutable comprimido con UPX local (lib/upx.exe)", Colors.OKGREEN)
                else:
                    print_colored("🗜️  Ejecutable comprimido con UPX del sistema", Colors.OKGREEN)
            else:
                print_colored("💡 Para obtener ejecutables más pequeños:", Colors.WARNING)
                if system == "Windows":
                    print_colored("   - Coloca upx.exe en la carpeta lib/", Colors.OKCYAN)
                    print_colored("   - O instala UPX globalmente", Colors.OKCYAN)
                else:
                    print_colored("   - Instala UPX con tu gestor de paquetes", Colors.OKCYAN)
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

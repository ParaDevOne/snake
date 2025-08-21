# setup.py
"""
Setup script para construir el ejecutable del juego Snake
y la aplicacion externa para la gestion de configuraciones.
Desarrollado por ParaDevOne - Snake Game v1.7.0
"""

import ctypes
import os
import platform
import shutil
import subprocess
import sys
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
    if platform.system() == "Windows":
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except ImportError:
            # No fallar si no se puede cambiar modo de consola
            pass
    print(f"{color}{message}{Colors.ENDC}")

def clean_build_files():
    """Limpia archivos y carpetas de builds anteriores."""
    print_colored("🧹 Limpiando archivos de builds anteriores...", Colors.OKCYAN)

    folders_to_clean = ["build", "dist", "__pycache__"]
    cleaned_items = []

    for folder in folders_to_clean:
        if os.path.exists(folder):
            was_dir = os.path.isdir(folder)
            try:
                if was_dir:
                    shutil.rmtree(folder)
                    cleaned_items.append(f"📁 {folder}/")
                else:
                    os.remove(folder)
                    cleaned_items.append(f"📄 {folder}")
            except ImportError as e:
                print_colored(f"⚠️  Error eliminando {folder}: {str(e)}", Colors.WARNING)

    # Limpiar archivos .spec y .pyc
    for pattern in ["*.spec", "*.pyc"]:
        for file_path in Path(".").rglob(pattern):
            try:
                file_path.unlink()
                cleaned_items.append(f"📄 {file_path}")
            except ImportError as e:
                print_colored(
                    f"⚠️  Error eliminando {file_path}: {str(e)}", Colors.WARNING
                )

    if cleaned_items:
        print_colored(
            f"✅ Limpieza completada. Eliminados {len(cleaned_items)} elementos.",
            Colors.OKGREEN,
        )
    else:
        print_colored("✅ No hay archivos que limpiar.", Colors.OKGREEN)

def find_upx_windows():
    """Busca UPX solo en Windows en ubicaciones específicas."""
    upx_locations = [
        Path("lib/upx.exe"),  # Directorio lib/ del proyecto
        Path("C:/Program Files/upx/upx.exe"),
        Path("C:/Program Files (x86)/upx/upx.exe"),
        Path.home() / "AppData/Local/upx/upx.exe",
        Path("Data/lib/upx.exe"),  # Directorio Data/upx/ del proyecto
    ]

    for path in upx_locations:
        if path.exists():
            try:
                # Verificar que UPX funciona
                result = subprocess.run(
                    [str(path), "--version"], capture_output=True, text=True, check=True
                )
                if result.returncode == 0:
                    return str(path), f"ubicación: {path}"
            except (
                FileNotFoundError,
                subprocess.CalledProcessError,
                PermissionError,
            ):
                # Si falló la ejecución, seguir buscando en otras rutas
                continue
            except ImportError:
                continue

    return None, None

def check_dependencies():
    """Verifica que PyInstaller y UPX (solo en Windows) estén disponibles."""
    print_colored("🔍 Verificando dependencias...", Colors.OKCYAN)
    dependencies_ok = True
    system = platform.system()

    # Verificar PyInstaller
    try:
        result = subprocess.run(
            ["pyinstaller", "--version"], capture_output=True, text=True, check=True
        )
        version = result.stdout.strip()
        print_colored(f"✅ PyInstaller {version} encontrado.", Colors.OKGREEN)
    except FileNotFoundError:
        print_colored(
            "❌ PyInstaller no está instalado o no está en PATH.", Colors.FAIL
        )
        print_colored("💡 Instálalo con: pip install pyinstaller", Colors.WARNING)
        dependencies_ok = False
    except subprocess.CalledProcessError as e:
        # PyInstaller ejecutó pero falló al devolver versión por alguna razón
        print_colored(f"❌ Error ejecutando pyinstaller: {e}", Colors.FAIL)
        dependencies_ok = False
    except ImportError as e:
        print_colored(f"❌ Error inesperado comprobando PyInstaller: {e}", Colors.FAIL)
        dependencies_ok = False

    # Buscar UPX solo en Windows
    upx_path, upx_location = None, None
    if system == "Windows":
        upx_path, upx_location = find_upx_windows()

        if upx_path:
            print_colored(f"✅ UPX encontrado en {upx_location}", Colors.OKGREEN)
            print_colored(f"📂 Ruta: {upx_path}", Colors.OKBLUE)
        else:
            print_colored(
                "⚠️  UPX no encontrado - el ejecutable será más grande", Colors.WARNING
            )
            print_colored("\n💡 Para instalar UPX en Windows:", Colors.WARNING)
            print_colored(
                "   1. Descarga UPX desde: https://upx.github.io/", Colors.OKCYAN
            )
            print_colored(
                "   2. Extrae el ejecutable a una carpeta permanente", Colors.OKCYAN
            )
            print_colored(
                "   3. Coloca upx.exe en el directorio 'lib/' del proyecto",
                Colors.OKCYAN,
            )
            print_colored(
                "   4. O agrega la carpeta de UPX al PATH del sistema", Colors.OKCYAN
            )
    else:
        print_colored(
            "ℹ️  UPX no se usará (solo disponible para Windows)", Colors.OKCYAN
        )

    return dependencies_ok, upx_path

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

def create_lib_directory():
    """Crea el directorio lib/ si no existe."""
    lib_dir = Path("lib")
    lib_dir.mkdir(exist_ok=True)
    return lib_dir

def build_executable(upx_path=None):
    """Construye el ejecutable usando PyInstaller."""
    print_colored("🔨 Iniciando construcción del ejecutable...", Colors.HEADER)

    # Configuración específica por sistema operativo
    system = platform.system()
    exe_name = "Snake Game.exe" if system == "Windows" else "Snake Game"
    separator = ";" if system == "Windows" else ":"

    # Configuración base de PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name",
        exe_name,
        "--clean",
        "--noconfirm",
        "--distpath",
        "dist",
        "--workpath",
        "build",
        "--optimize",
        "2",
    ]

    # Configurar UPX solo en Windows si está disponible
    upx_enabled = False
    if system == "Windows" and upx_path:
        cmd.extend(["--upx-dir", str(Path(upx_path).parent)])
        cmd.extend(
            [
                "--upx-exclude",
                "vcruntime140.dll",
                "--upx-exclude",
                "api-ms-*.dll",
                "--upx-exclude",
                "msvcp140.dll",
            ]
        )
        print_colored("🗜️  El ejecutable será comprimido con UPX", Colors.OKGREEN)
        upx_enabled = True
    elif system == "Windows":
        cmd.append("--noupx")
        print_colored("📦 UPX deshabilitado - ejecutable sin comprimir", Colors.WARNING)

    # Configurar icono
    icon_ext = "ico" if system == "Windows" else "icns" if system == "Darwin" else "png"
    icon_files = [
        f"./icon.{icon_ext}",
        f"./Data/assets/icon.{icon_ext}",
        "./icon.ico",
        "./Data/assets/icon.ico",
    ]

    for icon_file in icon_files:
        if os.path.exists(icon_file):
            cmd.extend(["--icon", icon_file])
            print_colored(f"🎨 Usando icono: {icon_file}", Colors.OKBLUE)
            break
    else:
        print_colored("ℹ️  No se encontró un icono específico", Colors.OKCYAN)

    # Configuraciones específicas por SO
    if system == "Darwin":  # macOS
        cmd.extend(
            [
                "--osx-bundle-identifier",
                "com.paradevone.snakegame",
                "--target-arch",
                "x86_64,arm64",
            ]
        )
        print_colored("🍎 Configuración macOS: Soporte universal", Colors.OKBLUE)
    elif system == "Linux":
        cmd.extend(
            [
                "--strip",
                "--exclude-module",
                "_tkinter",
            ]
        )
        print_colored("🐧 Configuración Linux: Strip + optimizaciones", Colors.OKBLUE)
    elif system == "Windows":
        cmd.extend(
            [
                "--exclude-module",
                "_tkinter",
                "--exclude-module",
                "matplotlib",
                "--exclude-module",
                "numpy",
            ]
        )
        print_colored(
            "🪟 Configuración Windows: Exclusiones optimizadas", Colors.OKBLUE
        )

    # Agregar datos adicionales
    data_folders = ["Data", "assets", "sounds", "images", "fonts", "config"]
    included_folders = []

    for folder in data_folders:
        folder_path = Path(folder)
        if folder_path.exists() and folder_path.is_dir() and any(folder_path.iterdir()):
            cmd.extend(["--add-data", f"{folder}{separator}{folder}"])
            included_folders.append(folder)

    if included_folders:
        print_colored(
            f"📦 Carpetas incluidas: {', '.join(included_folders)}", Colors.OKBLUE
        )

    # Agregar archivo principal
    cmd.append("main.py")

    print_colored("🚀 Comando PyInstaller:", Colors.OKBLUE)
    print_colored(f"   {' '.join(cmd)}", Colors.OKCYAN)
    print_colored("⏳ Esto puede tomar varios minutos...", Colors.WARNING)
    if upx_enabled:
        print_colored("⏳ UPX añadirá tiempo extra de compresión...", Colors.WARNING)

    try:
        print_colored("🔄 Ejecutando PyInstaller...", Colors.OKCYAN)
        result = subprocess.run(
            cmd, check=True, text=True, timeout=1800  # 30 minutos máximo
        )

        # En general, con check=True, si no hay excepción, el returncode es 0
        if isinstance(result, subprocess.CompletedProcess) and result.returncode == 0:
            print_colored("✅ PyInstaller completado exitosamente!", Colors.OKGREEN)

            # Establecer permisos de ejecución en Unix
            if system in ["Linux", "Darwin"]:
                exe_path = Path("dist") / exe_name
                if exe_path.exists():
                    try:
                        os.chmod(exe_path, 0o755)
                        print_colored(
                            "🔐 Permisos de ejecución configurados", Colors.OKGREEN
                        )
                    except ImportError as e:
                        print_colored(
                            f"⚠️  No se pudieron cambiar permisos: {e}", Colors.WARNING
                        )

            return True
        else:
            # Fallback: si por alguna razón no es CompletedProcess o returncode != 0
            print_colored(
                f"❌ PyInstaller terminó con código: {getattr(result, 'returncode', 'desconocido')}",
                Colors.FAIL,
            )
            return False

    except subprocess.TimeoutExpired:
        print_colored("❌ PyInstaller excedió el tiempo límite (30 min)", Colors.FAIL)
        return False
    except subprocess.CalledProcessError as e:
        print_colored("❌ Error durante la construcción:", Colors.FAIL)

        # Intentar sin UPX si el error está relacionado
        if upx_enabled and any(
            keyword in str(e).lower() for keyword in ["upx", "compress", "pack"]
        ):
            print_colored(
                "🔄 Error relacionado con UPX - intentando sin compresión...",
                Colors.WARNING,
            )
            return build_executable(upx_path=None)

        # Mostrar detalles del error
        try:
            if e.stdout:
                print_colored("STDOUT (últimas líneas):", Colors.WARNING)
                for line in e.stdout.splitlines()[-10:]:
                    if line.strip():
                        print_colored(f"  {line}", Colors.OKCYAN)
            if e.stderr:
                print_colored("STDERR (últimas líneas):", Colors.WARNING)
                for line in e.stderr.splitlines()[-10:]:
                    if line.strip():
                        print_colored(f"  {line}", Colors.OKCYAN)
        except ImportError:
            # En algunos entornos e.stdout/e.stderr podrían no estar presentes
            pass

        return False
    except ImportError as e:
        print_colored(f"❌ Error inesperado: {str(e)}", Colors.FAIL)
        return False

def show_build_info(upx_used=False):
    """Muestra información del ejecutable creado."""
    dist_dir = Path("dist")
    if not dist_dir.exists() or not any(dist_dir.iterdir()):
        return

    print_colored("\n📊 Información del build:", Colors.HEADER)
    print_colored("=" * 50, Colors.HEADER)

    system = platform.system()
    system_icon = "🪟" if system == "Windows" else "🍎" if system == "Darwin" else "🐧"
    print_colored(f"{system_icon} Sistema: {system}", Colors.OKBLUE)
    print_colored(f"🏗️ Arquitectura: {platform.machine()}", Colors.OKBLUE)

    for exe_file in dist_dir.iterdir():
        if exe_file.is_file() and not exe_file.name.startswith("."):
            try:
                size_bytes = exe_file.stat().st_size
                size_mb = size_bytes / (1024 * 1024)
            except ImportError as e:
                print_colored(f"⚠️  No se pudo obtener tamaño: {e}", Colors.WARNING)
                continue

            print_colored(f"\n📄 Archivo: {exe_file.name}", Colors.OKGREEN)
            print_colored(
                f"📏 Tamaño: {size_mb:.2f} MB ({size_bytes:,} bytes)", Colors.OKBLUE
            )
            print_colored(f"📍 Ubicación: {exe_file.absolute()}", Colors.OKBLUE)

            # Verificar si es ejecutable
            try:
                executable_ready = system == "Windows" or (
                    system != "Windows" and os.access(exe_file, os.X_OK)
                )
            except ImportError:
                executable_ready = False

            if executable_ready:
                print_colored("✅ Ejecutable listo para usar", Colors.OKGREEN)
                print_colored(
                    f"💡 Ejecutar con: {'./' if system != 'Windows' else ''}dist/{exe_file.name}",
                    Colors.OKCYAN,
                )

                if upx_used:
                    try:
                        estimated_original = size_mb * 2.5
                        print_colored("🗜️  Comprimido con UPX", Colors.OKGREEN)
                        print_colored(
                            f"📈 Tamaño estimado sin UPX: ~{estimated_original:.1f} MB",
                            Colors.OKCYAN,
                        )
                        print_colored(
                            f"💾 Espacio ahorrado: ~{estimated_original - size_mb:.1f} MB",
                            Colors.OKGREEN,
                        )
                    except ImportError:
                        pass
            else:
                print_colored("⚠️  Permisos de ejecución faltantes", Colors.WARNING)
                if system != "Windows":
                    print_colored(f"💡 Ejecutar: chmod +x '{exe_file}'", Colors.OKCYAN)

def main():
    """Función principal del script de setup."""
    print_colored("\n🐍 Snake Game - Build Script v1.7.0", Colors.HEADER)
    print_colored("🔧 Desarrollado por ParaDevOne", Colors.HEADER)
    print_colored("=" * 50, Colors.HEADER)

    system = platform.system()
    if system == "Windows":
        print_colored("💡 UPX se usará solo para compresión en Windows", Colors.OKCYAN)
        print_colored("   - Se buscará en Data/lib/ y ubicaciones comunes", Colors.OKCYAN)
    else:
        print_colored(
            "💡 UPX no se usará (solo disponible para Windows)", Colors.OKCYAN
        )

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
        create_lib_directory()

        success = build_executable(upx_path=upx_path)
        if success:
            show_build_info(upx_used=bool(upx_path))
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
        print_colored(f"\n❌ Error inesperado: {str(e)}", Colors.FAIL)
        sys.exit(1)

if __name__ == "__main__":
    main()

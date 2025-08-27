# setup.py
"""
Setup script para construir el ejecutable del juego Snake
y la aplicacion externa para la gestion de configuraciones.
Desarrollado por ParaDevOne - Snake Game v1.8.1
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

class IconSelector:
    """Manejador para la selección de iconos."""

    def __init__(self):
        self.available_icons = {}
        self.scan_available_icons()

    def scan_available_icons(self):
        """Escanea los iconos disponibles en el proyecto."""
        system = platform.system()
        icon_ext = "ico" if system == "Windows" else "icns" if system == "Darwin" else "png"

        # Definir ubicaciones posibles para iconos
        icon_locations = {
            "normal": [
                f"./icon.{icon_ext}",
                f"./Data/assets/icon.{icon_ext}",
                f"./assets/icon.{icon_ext}",
                "./icon.ico",  # Fallback para Windows
                "./Data/assets/icon.ico",
                "./assets/icon.ico",
            ],
            "retro": [
                f"./icon_retro.{icon_ext}",
                f"./Data/assets/icon_retro.{icon_ext}",
                f"./assets/icon_retro.{icon_ext}",
                f"./retro_icon.{icon_ext}",
                f"./Data/assets/retro_icon.{icon_ext}",
                f"./assets/retro_icon.{icon_ext}",
                "./icon_retro.ico",  # Fallback para Windows
                "./Data/assets/icon_retro.ico",
                "./assets/icon_retro.ico",
                "./retro_icon.ico",
                "./Data/assets/retro_icon.ico",
                "./assets/retro_icon.ico",
            ]
        }

        # Buscar iconos disponibles
        for icon_type, locations in icon_locations.items():
            for location in locations:
                if os.path.exists(location):
                    self.available_icons[icon_type] = location
                    break

    def show_available_icons(self):
        """Muestra los iconos disponibles (solo para debugging/info)."""
        if not self.available_icons:
            return False

        print_colored("📍 Iconos encontrados:", Colors.OKBLUE)
        for icon_type, path in self.available_icons.items():
            icon_emoji = "🎮" if icon_type == "normal" else "👾"
            print_colored(f"   {icon_emoji} {icon_type.capitalize()}: {path}", Colors.OKCYAN)

        return True

    def select_icon(self):
        """Permite al usuario seleccionar un icono. Por defecto usa normal."""
        # Siempre intentar usar el icono normal por defecto
        if "normal" in self.available_icons:
            normal_path = self.available_icons["normal"]
            print_colored("🎮 Icono normal configurado por defecto", Colors.OKGREEN)

            # Solo preguntar si hay icono retro disponible
            if "retro" in self.available_icons:
                print_colored(f"   📍 Normal: {normal_path}", Colors.OKBLUE)
                print_colored(f"   📍 Retro disponible: {self.available_icons['retro']}", Colors.OKBLUE)
                print_colored("\n👾 ¿Cambiar al icono retro? (y/N): ", Colors.OKCYAN, end="")

                try:
                    choice = input().strip().lower()
                    if choice in ['y', 'yes', 'si', 's']:
                        print_colored("👾 Cambiado al icono retro", Colors.OKGREEN)
                        return self.available_icons["retro"]
                    else:
                        print_colored("🎮 Manteniendo icono normal", Colors.OKGREEN)
                        return normal_path
                except KeyboardInterrupt:
                    print_colored("\n⏹️ Selección cancelada, usando normal", Colors.WARNING)
                    return normal_path
            else:
                print_colored("   (No hay icono retro disponible)", Colors.OKCYAN)
                return normal_path

        # Si no hay icono normal, buscar retro
        elif "retro" in self.available_icons:
            retro_path = self.available_icons["retro"]
            print_colored("⚠️  No se encontró icono normal, usando retro", Colors.WARNING)
            print_colored(f"👾 Usando icono retro: {retro_path}", Colors.OKGREEN)
            return retro_path

        # No hay iconos disponibles
        else:
            print_colored("❌ No se encontraron iconos disponibles", Colors.FAIL)
            return None

def print_colored(message, color=Colors.ENDC, end='\n'):
    """Imprime mensaje con color si la terminal lo soporta."""
    if platform.system() == "Windows":
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except (ImportError, AttributeError):
            # No fallar si no se puede cambiar modo de consola
            pass
    print(f"{color}{message}{Colors.ENDC}", end=end)

def clean_build_files():
    """Limpia archivos y carpetas de builds anteriores."""
    print_colored("🧹 Limpiando archivos de builds anteriores...", Colors.OKCYAN)

    folders_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = []

    # Buscar archivos .spec y .pyc
    for pattern in ["*.spec", "*.pyc"]:
        files_to_clean.extend(Path(".").rglob(pattern))

    cleaned_items = []

    # Limpiar carpetas
    for folder in folders_to_clean:
        folder_path = Path(folder)
        if folder_path.exists():
            try:
                if folder_path.is_dir():
                    shutil.rmtree(folder_path)
                    cleaned_items.append(f"📁 {folder}/")
                else:
                    folder_path.unlink()
                    cleaned_items.append(f"📄 {folder}")
            except (OSError, PermissionError) as e:
                print_colored(f"⚠️  Error eliminando {folder}: {str(e)}", Colors.WARNING)

    # Limpiar archivos
    for file_path in files_to_clean:
        try:
            file_path.unlink()
            cleaned_items.append(f"📄 {file_path}")
        except (OSError, PermissionError) as e:
            print_colored(f"⚠️  Error eliminando {file_path}: {str(e)}", Colors.WARNING)

    if cleaned_items:
        print_colored(f"✅ Limpieza completada. Eliminados {len(cleaned_items)} elementos.", Colors.OKGREEN)
        # Mostrar solo los primeros 5 elementos si hay muchos
        if len(cleaned_items) <= 5:
            for item in cleaned_items:
                print_colored(f"   {item}", Colors.OKCYAN)
        else:
            for item in cleaned_items[:3]:
                print_colored(f"   {item}", Colors.OKCYAN)
            print_colored(f"   ... y {len(cleaned_items) - 3} elementos más", Colors.OKCYAN)
    else:
        print_colored("✅ No hay archivos que limpiar.", Colors.OKGREEN)

def find_upx_windows():
    """Busca UPX solo en Windows en ubicaciones específicas."""
    upx_locations = [
        Path("lib/upx.exe"),  # Directorio lib/ del proyecto
        Path("Data/lib/upx.exe"),  # Directorio Data/lib/ del proyecto
        Path("C:/Program Files/upx/upx.exe"),
        Path("C:/Program Files (x86)/upx/upx.exe"),
        Path.home() / "AppData/Local/upx/upx.exe",
        Path("upx.exe"),  # En el directorio actual
    ]

    for path in upx_locations:
        if path.exists():
            try:
                # Verificar que UPX funciona
                result = subprocess.run(
                    [str(path), "--version"],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return str(path), f"ubicación: {path}"
            except (FileNotFoundError, subprocess.CalledProcessError, PermissionError, subprocess.TimeoutExpired):
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
            ["pyinstaller", "--version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=15
        )
        version = result.stdout.strip()
        print_colored(f"✅ PyInstaller {version} encontrado.", Colors.OKGREEN)
    except FileNotFoundError:
        print_colored("❌ PyInstaller no está instalado o no está en PATH.", Colors.FAIL)
        print_colored("💡 Instálalo con: pip install pyinstaller", Colors.WARNING)
        dependencies_ok = False
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Error ejecutando pyinstaller: {e}", Colors.FAIL)
        dependencies_ok = False
    except subprocess.TimeoutExpired:
        print_colored("❌ Timeout verificando PyInstaller", Colors.FAIL)
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
            print_colored("⚠️  UPX no encontrado - el ejecutable será más grande", Colors.WARNING)
            print_colored("\n💡 Para instalar UPX en Windows:", Colors.WARNING)
            print_colored("   1. Descarga UPX desde: https://upx.github.io/", Colors.OKCYAN)
            print_colored("   2. Extrae el ejecutable a una carpeta permanente", Colors.OKCYAN)
            print_colored("   3. Coloca upx.exe en el directorio 'lib/' del proyecto", Colors.OKCYAN)
            print_colored("   4. O agrega la carpeta de UPX al PATH del sistema", Colors.OKCYAN)
    else:
        print_colored("ℹ️  UPX no se usará (solo disponible para Windows)", Colors.OKCYAN)

    return dependencies_ok, upx_path

def check_main_file():
    """Verifica que el archivo main.py exista."""
    main_file = Path("__main__.py")
    if not main_file.exists():
        print_colored("❌ Archivo __main__.py no encontrado.", Colors.FAIL)
        print_colored("💡 Asegúrate de estar en el directorio correcto del proyecto.", Colors.WARNING)
        return False

    # Verificar que el archivo no esté vacío
    try:
        if main_file.stat().st_size == 0:
            print_colored("⚠️  El archivo __main__.py está vacío.", Colors.WARNING)
            return False
    except OSError as e:
        print_colored(f"⚠️  Error verificando __main__.py: {e}", Colors.WARNING)

    print_colored("✅ Archivo __main__.py encontrado y válido.", Colors.OKGREEN)
    return True

def create_lib_directory():
    """Crea el directorio lib/ si no existe."""
    lib_dir = Path("lib")
    lib_dir.mkdir(exist_ok=True)
    return lib_dir

def get_build_configuration():
    """Permite al usuario configurar opciones del build."""
    print_colored("\n⚙️  Configuración del Build:", Colors.HEADER)
    print_colored("-" * 30, Colors.OKCYAN)

    # Selección de icono (normal por defecto, opción de cambiar a retro)
    icon_selector = IconSelector()
    if icon_selector.available_icons:
        icon_selector.show_available_icons()
    selected_icon = icon_selector.select_icon()

    # Configuración de compresión UPX (solo Windows)
    use_upx = True
    if platform.system() == "Windows":
        print_colored("🗜️  ¿Usar compresión UPX si está disponible? (Y/n): ", Colors.OKCYAN, end="")
        upx_choice = input().strip().lower()
        use_upx = upx_choice not in ['n', 'no', 'false']

        if use_upx:
            print_colored("✅ UPX habilitado (si está disponible)", Colors.OKGREEN)
        else:
            print_colored("❌ UPX deshabilitado", Colors.WARNING)

    return {
        'icon_path': selected_icon,
        'use_upx': use_upx
    }

def build_executable(upx_path=None, config=None):
    """Construye el ejecutable usando PyInstaller."""
    print_colored("🔨 Iniciando construcción del ejecutable...", Colors.HEADER)

    if config is None:
        config = {}

    # Configuración específica por sistema operativo
    system = platform.system()
    exe_name = "Snake Game.exe" if system == "Windows" else "Snake Game"
    separator = ";" if system == "Windows" else ":"

    # Configuración base de PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", exe_name,
        "--clean",
        "--noconfirm",
        "--distpath", "dist",
        "--workpath", "build",
        "--optimize", "2",
    ]

    # Configurar UPX solo en Windows si está disponible y habilitado
    upx_enabled = False
    if system == "Windows" and upx_path and config.get('use_upx', True):
        cmd.extend(["--upx-dir", str(Path(upx_path).parent)])
        cmd.extend([
            "--upx-exclude", "vcruntime140.dll",
            "--upx-exclude", "api-ms-*.dll",
            "--upx-exclude", "msvcp140.dll",
            "--upx-exclude", "ucrtbase.dll",
        ])
        print_colored("🗜️  El ejecutable será comprimido con UPX", Colors.OKGREEN)
        upx_enabled = True
    elif system == "Windows":
        cmd.append("--noupx")
        reason = "deshabilitado por usuario" if not config.get('use_upx', True) else "no disponible"
        print_colored(f"📦 UPX {reason} - ejecutable sin comprimir", Colors.WARNING)

    # Configurar icono
    icon_path = config.get('icon_path')
    if icon_path and os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
        icon_type = "retro" if "retro" in str(icon_path).lower() else "normal"
        icon_emoji = "👾" if icon_type == "retro" else "🎮"
        print_colored(f"{icon_emoji} Usando icono {icon_type}: {icon_path}", Colors.OKBLUE)
    else:
        print_colored("ℹ️  No se encontró un icono válido", Colors.OKCYAN)

    # Configuraciones específicas por SO
    if system == "Darwin":  # macOS
        cmd.extend([
            "--osx-bundle-identifier", "com.paradevone.snakegame",
            "--target-arch", "universal2",  # Soporte universal
        ])
        print_colored("🍎 Configuración macOS: Soporte universal", Colors.OKBLUE)
    elif system == "Linux":
        cmd.extend([
            "--strip",
            "--exclude-module", "_tkinter",
            "--exclude-module", "tkinter",
        ])
        print_colored("🐧 Configuración Linux: Strip + optimizaciones", Colors.OKBLUE)
    elif system == "Windows":
        cmd.extend([
            "--exclude-module", "_tkinter",
            "--exclude-module", "tkinter",
            "--exclude-module", "matplotlib",
            "--exclude-module", "numpy",
            "--exclude-module", "scipy",
        ])
        print_colored("🪟 Configuración Windows: Exclusiones optimizadas", Colors.OKBLUE)

    # Agregar datos adicionales
    data_folders = ["Data", "assets", "sounds", "images", "fonts", "config", "resources"]
    included_folders = []

    for folder in data_folders:
        folder_path = Path(folder)
        if folder_path.exists() and folder_path.is_dir():
            # Verificar que la carpeta no esté vacía
            try:
                if any(folder_path.iterdir()):
                    cmd.extend(["--add-data", f"{folder}{separator}{folder}"])
                    included_folders.append(folder)
            except (OSError, PermissionError):
                continue

    if included_folders:
        print_colored(f"📦 Carpetas incluidas: {', '.join(included_folders)}", Colors.OKBLUE)
    else:
        print_colored("ℹ️  No se encontraron carpetas de datos adicionales", Colors.OKCYAN)

    # Agregar archivo principal
    cmd.append("__main__.py")

    print_colored("\n🚀 Comando PyInstaller:", Colors.OKBLUE)
    print_colored(f"   {' '.join(cmd[:8])} ...", Colors.OKCYAN)  # Mostrar solo parte del comando
    print_colored("⏳ Esto puede tomar varios minutos...", Colors.WARNING)
    if upx_enabled:
        print_colored("⏳ UPX añadirá tiempo extra de compresión...", Colors.WARNING)

    try:
        print_colored("🔄 Ejecutando PyInstaller...", Colors.OKCYAN)
        subprocess.run(
            cmd,
            check=True,
            text=True,
            timeout=1800,  # 30 minutos máximo
            capture_output=True
        )

        print_colored("✅ PyInstaller completado exitosamente!", Colors.OKGREEN)

        # Establecer permisos de ejecución en Unix
        if system in ["Linux", "Darwin"]:
            exe_path = Path("dist") / exe_name
            if exe_path.exists():
                try:
                    os.chmod(exe_path, 0o755)
                    print_colored("🔐 Permisos de ejecución configurados", Colors.OKGREEN)
                except OSError as e:
                    print_colored(f"⚠️  No se pudieron cambiar permisos: {e}", Colors.WARNING)

        return True

    except subprocess.TimeoutExpired:
        print_colored("❌ PyInstaller excedió el tiempo límite (30 min)", Colors.FAIL)
        return False
    except subprocess.CalledProcessError as e:
        print_colored("❌ Error durante la construcción:", Colors.FAIL)

        # Intentar sin UPX si el error está relacionado
        if upx_enabled and any(keyword in str(e).lower() for keyword in ["upx", "compress", "pack"]):
            print_colored("🔄 Error relacionado con UPX - intentando sin compresión...", Colors.WARNING)
            new_config = config.copy()
            new_config['use_upx'] = False
            return build_executable(upx_path=None, config=new_config)

        # Mostrar detalles del error
        if hasattr(e, 'stderr') and e.stderr:
            print_colored("❌ Errores encontrados:", Colors.FAIL)
            for line in e.stderr.splitlines()[-5:]:
                if line.strip():
                    print_colored(f"  {line}", Colors.OKCYAN)

        return False
    except ImportError as e:
        print_colored(f"❌ Error inesperado: {str(e)}", Colors.FAIL)
        return False

def show_build_info(upx_used=False, config=None):
    """Muestra información del ejecutable creado."""
    dist_dir = Path("dist")
    if not dist_dir.exists() or not any(dist_dir.iterdir()):
        print_colored("❌ No se encontraron archivos en el directorio dist/", Colors.FAIL)
        return

    print_colored("\n📊 Información del build:", Colors.HEADER)
    print_colored("=" * 50, Colors.HEADER)

    system = platform.system()
    system_icon = "🪟" if system == "Windows" else "🍎" if system == "Darwin" else "🐧"
    print_colored(f"{system_icon} Sistema: {system} ({platform.release()})", Colors.OKBLUE)
    print_colored(f"🏗️ Arquitectura: {platform.machine()}", Colors.OKBLUE)

    # Mostrar información del icono usado
    if config and config.get('icon_path'):
        icon_path = config['icon_path']
        icon_type = "retro" if "retro" in str(icon_path).lower() else "normal"
        icon_emoji = "👾" if icon_type == "retro" else "🎮"
        print_colored(f"{icon_emoji} Icono: {icon_type} ({Path(icon_path).name})", Colors.OKBLUE)

    exe_files = [f for f in dist_dir.iterdir() if f.is_file() and not f.name.startswith(".")]

    if not exe_files:
        print_colored("❌ No se encontraron ejecutables en dist/", Colors.FAIL)
        return

    for exe_file in exe_files:
        try:
            size_bytes = exe_file.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
        except OSError as e:
            print_colored(f"⚠️  No se pudo obtener tamaño de {exe_file.name}: {e}", Colors.WARNING)
            continue

        print_colored(f"\n📄 Archivo: {exe_file.name}", Colors.OKGREEN)
        print_colored(f"📏 Tamaño: {size_mb:.2f} MB ({size_bytes:,} bytes)", Colors.OKBLUE)
        print_colored(f"📍 Ubicación: {exe_file.absolute()}", Colors.OKBLUE)

        # Verificar si es ejecutable
        try:
            executable_ready = system == "Windows" or (system != "Windows" and os.access(exe_file, os.X_OK))
        except OSError:
            executable_ready = False

        if executable_ready:
            print_colored("✅ Ejecutable listo para usar", Colors.OKGREEN)
            run_command = f"./{exe_file.name}" if system != "Windows" else f"{exe_file.name}"
            print_colored(f"💡 Ejecutar con: cd dist && {run_command}", Colors.OKCYAN)

            if upx_used:
                try:
                    estimated_original = size_mb * 2.5
                    print_colored("🗜️  Comprimido con UPX", Colors.OKGREEN)
                    print_colored(f"📈 Tamaño estimado sin UPX: ~{estimated_original:.1f} MB", Colors.OKCYAN)
                    print_colored(f"💾 Espacio ahorrado: ~{estimated_original - size_mb:.1f} MB", Colors.OKGREEN)
                except ImportError:
                    pass
        else:
            print_colored("⚠️  Permisos de ejecución faltantes", Colors.WARNING)
            if system != "Windows":
                print_colored(f"💡 Ejecutar: chmod +x 'dist/{exe_file.name}'", Colors.OKCYAN)

def main():
    """Función principal del script de setup."""
    print_colored("\n🐍 Snake Game - Build Script v1.8.1", Colors.HEADER)
    print_colored("🔧 Desarrollado por ParaDevOne", Colors.HEADER)
    print_colored("=" * 50, Colors.HEADER)

    system = platform.system()
    print_colored(f"💻 Sistema detectado: {system}", Colors.OKBLUE)

    if system == "Windows":
        print_colored("💡 UPX se puede usar para compresión en Windows", Colors.OKCYAN)
        print_colored("   - Se buscará en lib/, Data/lib/ y ubicaciones comunes", Colors.OKCYAN)
    else:
        print_colored("💡 UPX no se usará (solo disponible para Windows)", Colors.OKCYAN)

    print_colored("-" * 50, Colors.OKCYAN)

    # Verificaciones previas
    if not check_main_file():
        print_colored("\n❌ Archivo principal no encontrado. Abortando build.", Colors.FAIL)
        sys.exit(1)

    pyinstaller_ok, upx_path = check_dependencies()
    if not pyinstaller_ok:
        print_colored("\n❌ Dependencias faltantes. Abortando build.", Colors.FAIL)
        sys.exit(1)

    # Configuración del build
    try:
        config = get_build_configuration()

        if config['icon_path'] is None:
            print_colored("⚠️  No se encontraron iconos. ¿Continuar sin icono? (Y/n): ", Colors.WARNING, end="")
            continue_choice = input().strip().lower()
            if continue_choice in ['n', 'no', 'false']:
                print_colored("❌ Build cancelado por el usuario.", Colors.WARNING)
                sys.exit(0)
            else:
                print_colored("✅ Continuando sin icono personalizado", Colors.OKGREEN)

    except KeyboardInterrupt:
        print_colored("\n⏹️  Configuración cancelada por el usuario.", Colors.WARNING)
        sys.exit(0)

    # Proceso de construcción
    try:
        clean_build_files()
        create_lib_directory()

        # Ajustar UPX según configuración
        final_upx_path = upx_path if config.get('use_upx', True) else None

        success = build_executable(upx_path=final_upx_path, config=config)

        if success:
            show_build_info(upx_used=bool(final_upx_path), config=config)
            print_colored("\n🎉 ¡Build completado exitosamente!", Colors.OKGREEN)
            print_colored("🚀 Tu ejecutable está listo en la carpeta 'dist/'", Colors.OKGREEN)

            if config.get('icon_path'):
                icon_type = "retro" if "retro" in str(config['icon_path']).lower() else "normal"
                icon_emoji = "👾" if icon_type == "retro" else "🎮"
                print_colored(f"{icon_emoji} Con icono {icon_type} aplicado", Colors.OKGREEN)
        else:
            print_colored("\n❌ Build falló. Revisa los errores arriba.", Colors.FAIL)
            print_colored("💡 Intenta ejecutar el script nuevamente o verifica las dependencias.", Colors.WARNING)
            sys.exit(1)

    except KeyboardInterrupt:
        print_colored("\n⏹️  Build cancelado por el usuario.", Colors.WARNING)
        sys.exit(1)
    except ImportError as e:
        print_colored(f"\n❌ Error inesperado: {str(e)}", Colors.FAIL)
        print_colored("💡 Si el problema persiste, verifica tu instalación de Python y PyInstaller.", Colors.WARNING)
        sys.exit(1)

if __name__ == "__main__":
    main()

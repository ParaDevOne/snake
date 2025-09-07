"""
Ultimate Project Cleaner - Versión Mejorada
Limpieza BRUTAL y EFICIENTE de proyectos
"""

import os
import sys
import shutil
import json
import hashlib
import concurrent.futures
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import time


class UltimateProjectCleaner:
    """Limpiador de proyectos DEFINITIVO - Sin piedad"""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = (
            Path(project_root)
            if project_root
            else Path(os.path.dirname(os.path.dirname(__file__)))
        )
        self.cleaned_files = 0
        self.cleaned_dirs = 0
        self.freed_space = 0
        self.errors = []
        self.duplicates_removed = 0
        self.large_files_found = []
        self.config = self.load_config()

        # Patrones mejorados y más completos
        self.patterns = {
            "python_cache": ["__pycache__/", "*.pyc", "*.pyo", "*.pyd", ".Python"],
            "build_artifacts": [
                "build/",
                "dist/",
                ".eggs/",
                "*.egg-info/",
                ".tox/",
                "venv/",
                "env/",
            ],
            "logs": ["*.log", "*.log.*", "logs/", "Data/logs.txt", "*.out", "*.err"],
            "temp_files": [
                "*.tmp",
                "*.temp",
                "*~",
                ".DS_Store",
                "Thumbs.db",
                "*.swp",
                "*.swo",
                ".coverage",
                "htmlcov/",
                ".pytest_cache/",
                ".mypy_cache/",
                "*.backup",
                "core.*",
                "*.core",
                "*.pid",
            ],
            "version_control": [
                ".git/logs/",
                ".git/refs/remotes/",
                ".git/refs/stash",
                ".svn/",
            ],
            "documentation": ["docs/_build/", "site/", ".readthedocs.yml.bak"],
            "media_cache": [".thumbnails/", "*.cache", "cached_*"],
            "package_managers": [
                "node_modules/",
                "bower_components/",
                ".npm/",
                ".yarn/",
                "vendor/",
                "Pipfile.lock.bak",
                "yarn.lock.bak",
            ],
            "databases": ["*.sqlite-journal", "*.db-wal", "*.db-shm"],
        }

    def load_config(self) -> Dict:
        """Cargar configuración personalizada si existe"""
        config_file = self.project_root / ".cleaner_config.json"
        default_config = {
            "max_file_size_mb": 100,
            "keep_recent_days": 1,
            "parallel_workers": min(4, os.cpu_count() or 1),
            "safe_mode": True,
            "auto_confirm": False,
            "exclude_patterns": [".git/", ".env", "*.key", "*.pem"],
        }

        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                self.log(f"Config cargada mal, usando defaults: {e}", "WARN")

        return default_config

    def log(self, message: str, status: str = "INFO", color: bool = True):
        """Logging mejorado con timestamps y colores"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        if color:
            status_colors = {
                "CLEAN": "\033[92m🧹 LIMPIO\033[0m",
                "SKIP": "\033[93m⏭ OMITIDO\033[0m",
                "INFO": "\033[94mℹ INFO\033[0m",
                "WARN": "\033[93m⚠ CUIDADO\033[0m",
                "ERROR": "\033[91m❌ ERROR\033[0m",
                "FOUND": "\033[96m🔍 ENCONTRADO\033[0m",
                "BRUTAL": "\033[95m💥 BRUTAL\033[0m",
            }
            status_text = status_colors.get(status, status)
        else:
            status_text = status

        print(f"[{timestamp}] {status_text} {message}")

    def get_size(self, path: Path) -> int:
        """Obtener tamaño optimizado con manejo de errores"""
        try:
            if path.is_file():
                return path.stat().st_size
            elif path.is_dir():
                return sum(
                    f.stat().st_size
                    for f in path.rglob("*")
                    if f.is_file() and not f.is_symlink()
                )
        except (OSError, PermissionError):
            pass
        return 0

    def format_size(self, bytes_size: int) -> str:
        """Formato de tamaño mejorado"""
        if bytes_size == 0:
            return "0 B"

        units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0
        size = float(bytes_size)

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024.0
            unit_index += 1

        return f"{size:.1f} {units[unit_index]}"

    def get_system_stats(self) -> Tuple[str, str]:
        """Obtener estadísticas del sistema usando métodos nativos"""
        try:
            # Espacio en disco usando shutil (nativo en Python 3.3+)
            disk_usage = shutil.disk_usage(str(self.project_root))
            disk_free = self.format_size(disk_usage.free)
            disk_info = f"• Espacio libre en disco: {disk_free}"
        except (OSError, AttributeError):
            disk_info = "• Espacio en disco: N/A"

        # Información básica del sistema
        try:
            if hasattr(os, "getloadavg"):  # Unix/Linux
                load_avg = os.getloadavg()[0]
                system_info = f"• Load average: {load_avg:.2f}"
            elif sys.platform == "win32":
                # Windows - usar información básica
                system_info = f"• Plataforma: {sys.platform}"
            else:
                system_info = f"• Plataforma: {sys.platform}"
        except (OSError, AttributeError):
            system_info = "• Sistema: N/A"

        return disk_info, system_info

    def is_safe_to_delete(self, path: Path) -> bool:
        """Verificar si es seguro borrar - MODO BRUTAL"""
        path_str = str(path).lower()

        # Patrones que NUNCA se borran
        protected = [
            ".git",
            ".env",
            "requirements.txt",
            "setup.py",
            "readme",
            "license",
            "dockerfile",
            "makefile",
            ".gitignore",
        ]

        for pattern in self.config["exclude_patterns"]:
            if pattern.lower() in path_str:
                return False

        for protected_file in protected:
            if protected_file in path_str:
                return False

        return True

    def find_duplicates(self) -> List[Tuple[str, List[Path]]]:
        """Encontrar archivos duplicados usando hash MD5"""
        self.log("Buscando archivos duplicados...", "BRUTAL")

        file_hashes = {}
        duplicates = []

        for file_path in self.project_root.rglob("*"):
            if (
                file_path.is_file() and file_path.stat().st_size > 1024
            ):  # Solo archivos > 1KB
                try:
                    with open(file_path, "rb") as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()

                    if file_hash in file_hashes:
                        file_hashes[file_hash].append(file_path)
                    else:
                        file_hashes[file_hash] = [file_path]

                except (OSError, PermissionError):
                    continue

        # Encontrar grupos de duplicados
        for paths in file_hashes.values():
            if len(paths) > 1:
                duplicates.append(("duplicate_group", paths))

        return duplicates

    def remove_duplicates(self) -> int:
        """Eliminar duplicados manteniendo el más reciente"""
        duplicates = self.find_duplicates()
        removed_count = 0

        for _, paths in duplicates:
            # Ordenar por fecha de modificación (más reciente primero)
            paths.sort(key=lambda p: p.stat().st_mtime, reverse=True)

            # Mantener el primero, borrar el resto
            keep_file = paths[0]
            to_remove = paths[1:]

            total_size = sum(self.get_size(p) for p in to_remove)

            self.log(
                f"Duplicado encontrado: {len(paths)} copias de {keep_file.name}",
                "FOUND",
            )

            if not self.config["auto_confirm"]:
                response = input(
                    f"¿Borrar {len(to_remove)} duplicados? Libera {self.format_size(total_size)} (y/N): "
                )
                if response.lower() != "y":
                    continue

            for duplicate_file in to_remove:
                try:
                    size = self.get_size(duplicate_file)
                    duplicate_file.unlink()
                    self.log(
                        f"Duplicado eliminado: {duplicate_file} ({self.format_size(size)})",
                        "CLEAN",
                    )
                    self.cleaned_files += 1
                    self.freed_space += size
                    removed_count += 1
                except (OSError, IOError, PermissionError) as e:
                    self.log(f"Error borrando duplicado {duplicate_file}: {e}", "ERROR")

        return removed_count

    def find_large_files(self, min_size_mb: int = 10) -> List[Tuple[Path, int, bool]]:
        """Encontrar archivos grandes que podrían no ser necesarios"""
        large_files = []
        min_size = min_size_mb * 1024 * 1024

        suspicious_extensions = [
            ".zip",
            ".tar",
            ".gz",
            ".bz2",
            ".7z",
            ".rar",
            ".iso",
            ".img",
            ".dmg",
            ".exe",
            ".msi",
            ".deb",
            ".rpm",
            ".apk",
            ".ipa",
            ".jar",
        ]

        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    if size >= min_size:
                        # Priorizar archivos sospechosos
                        is_suspicious = any(
                            str(file_path).endswith(ext)
                            for ext in suspicious_extensions
                        )
                        large_files.append((file_path, size, is_suspicious))
                except (OSError, PermissionError):
                    continue

        # Ordenar por tamaño (más grande primero) y priorizar sospechosos
        large_files.sort(key=lambda x: (not x[2], -x[1]))
        return large_files

    def clean_pattern_parallel(
        self, pattern_name: str, patterns: List[str]
    ) -> Tuple[int, int, int]:
        """Limpiar patrones usando procesamiento paralelo"""
        self.log(f"Limpiando {pattern_name}...", "BRUTAL")

        files_removed = 0
        dirs_removed = 0
        space_freed = 0

        all_matches = []

        # Recopilar todas las coincidencias
        for pattern in patterns:
            matches = list(self.project_root.rglob(pattern))
            all_matches.extend(matches)

        # Procesar en paralelo
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.config["parallel_workers"]
        ) as executor:
            future_to_path = {
                executor.submit(self._remove_path, path): path for path in all_matches
            }

            for future in concurrent.futures.as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    removed, size, is_dir = future.result()
                    if removed:
                        if is_dir:
                            dirs_removed += 1
                        else:
                            files_removed += 1
                        space_freed += size
                        self.log(
                            f"Eliminado: {path} ({self.format_size(size)})", "CLEAN"
                        )
                except (OSError, PermissionError) as e:
                    self.log(f"Error procesando {path}: {e}", "ERROR")
                    self.errors.append(f"{path}: {e}")

        return files_removed, dirs_removed, space_freed

    def _remove_path(self, path: Path) -> Tuple[bool, int, bool]:
        """Función auxiliar para remover paths de forma thread-safe"""
        if not path.exists() or not self.is_safe_to_delete(path):
            return False, 0, False

        try:
            size = self.get_size(path)
            is_dir = path.is_dir()

            if is_dir:
                shutil.rmtree(path)
            else:
                path.unlink()

            return True, size, is_dir
        except (OSError, FileNotFoundError, PermissionError):
            return False, 0, False

    def clean_old_files(self, days: Optional[int] = None) -> int:
        """Limpiar archivos antiguos basado en fecha de modificación"""
        days = days or self.config["keep_recent_days"]
        cutoff_date = datetime.now() - timedelta(days=days)

        self.log(
            f"Limpiando archivos anteriores a {cutoff_date.strftime('%Y-%m-%d')}",
            "BRUTAL",
        )

        old_files_removed = 0
        temp_extensions = [".tmp", ".temp", ".bak", ".old", ".cache"]

        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                try:
                    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mod_time < cutoff_date:
                        # Solo borrar archivos con extensiones temporales o en directorios temp
                        path_str = str(file_path).lower()
                        is_temp = any(ext in path_str for ext in temp_extensions)
                        is_temp_dir = any(
                            temp_dir in path_str
                            for temp_dir in ["temp", "tmp", "cache"]
                        )

                        if is_temp or is_temp_dir:
                            size = self.get_size(file_path)
                            file_path.unlink()
                            self.log(f"Archivo antiguo eliminado: {file_path}", "CLEAN")
                            old_files_removed += 1
                            self.freed_space += size

                except (OSError, PermissionError):
                    continue

        return old_files_removed

    def optimize_git_repo(self):
        """Optimizar repositorio git si existe"""
        git_dir = self.project_root / ".git"
        if git_dir.exists():
            self.log("Optimizando repositorio Git...", "BRUTAL")

            try:
                # Limpiar referencias y logs innecesarios
                refs_dir = git_dir / "refs" / "remotes"
                if refs_dir.exists():
                    size_before = self.get_size(refs_dir)
                    # Aquí podrías implementar limpieza más específica de git
                    self.log(f"Git refs size: {self.format_size(size_before)}", "INFO")
            except (OSError, PermissionError) as e:
                self.log(f"Error optimizando git: {e}", "ERROR")

    def interactive_large_files_cleanup(self):
        """Revisión interactiva de archivos grandes"""
        large_files = self.find_large_files(self.config["max_file_size_mb"])

        if not large_files:
            self.log("No se encontraron archivos grandes sospechosos", "INFO")
            return

        self.log(f"Encontrados {len(large_files)} archivos grandes:", "FOUND")

        for i, (file_path, size, is_suspicious) in enumerate(
            large_files[:20]
        ):  # Mostrar top 20
            status = "🔴 SOSPECHOSO" if is_suspicious else "ℹ️ GRANDE"
            self.log(
                f"{i + 1}. {status} {file_path.name}: {self.format_size(size)}", "FOUND"
            )

            if not self.config["auto_confirm"]:
                response = input("¿Eliminar este archivo? (y/N/s=skip_all): ")
                if response.lower() == "s":
                    break
                elif response.lower() == "y":
                    try:
                        file_path.unlink()
                        self.log(f"Archivo grande eliminado: {file_path.name}", "CLEAN")
                        self.cleaned_files += 1
                        self.freed_space += size
                    except (OSError, PermissionError) as e:
                        self.log(f"Error: {e}", "ERROR")

    def generate_report(self, duration: float) -> str:
        """Generar reporte detallado de limpieza"""
        # Generar estadísticas del sistema
        disk_info, system_info = self.get_system_stats()

        report = f"""
{"=" * 60}
🧹 REPORTE DE LIMPIEZA BRUTAL 🧹
{"=" * 60}

📊 ESTADÍSTICAS:
• Archivos eliminados: {self.cleaned_files}
• Directorios eliminados: {self.cleaned_dirs}
• Duplicados eliminados: {self.duplicates_removed}
• Espacio liberado: {self.format_size(self.freed_space)}
• Tiempo transcurrido: {duration:.2f} segundos
• Errores encontrados: {len(self.errors)}

💾 SISTEMA:
{disk_info}
{system_info}

⚡ RENDIMIENTO:
• Archivos/segundo: {self.cleaned_files / duration:.1f}
• MB/segundo: {(self.freed_space / 1024 / 1024) / duration:.1f}

"""

        if self.errors:
            report += f"\n❌ ERRORES ({len(self.errors)}):\n"
            for error in self.errors[:5]:  # Mostrar primeros 5
                report += f"• {error}\n"
            if len(self.errors) > 5:
                report += f"• ... y {len(self.errors) - 5} errores más\n"

        return report

    def clean_ultimate(self, **options):
        """Limpieza ULTIMATE - Sin piedad, máxima eficiencia"""
        self.log("🚀 INICIANDO LIMPIEZA ULTIMATE", "BRUTAL")
        self.log("🔥 MODO: SIN PIEDAD ACTIVADO", "BRUTAL")

        start_time = time.time()

        # 1. Limpiar patrones básicos en paralelo
        for pattern_name, patterns in self.patterns.items():
            if options.get(pattern_name, True):
                files, dirs, space = self.clean_pattern_parallel(pattern_name, patterns)
                self.cleaned_files += files
                self.cleaned_dirs += dirs
                self.freed_space += space

        # 2. Buscar y eliminar duplicados
        if options.get("remove_duplicates", True):
            self.duplicates_removed = self.remove_duplicates()

        # 3. Limpiar archivos antiguos
        if options.get("clean_old_files", True):
            self.clean_old_files()

        # 4. Revisar archivos grandes
        if options.get("review_large_files", True):
            self.interactive_large_files_cleanup()

        # 5. Optimizar Git
        if options.get("optimize_git", True):
            self.optimize_git_repo()

        # Generar y mostrar reporte
        duration = time.time() - start_time
        report = self.generate_report(duration)
        print(report)

        # Guardar reporte
        report_file = (
            self.project_root
            / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)

        self.log(f"Reporte guardado: {report_file}", "INFO")

        if self.freed_space > 0:
            self.log("💥 LIMPIEZA BRUTAL COMPLETADA! 💥", "BRUTAL")
        else:
            self.log("✨ Proyecto ya estaba limpio", "INFO")


def main():
    """Función principal mejorada con más opciones"""

    parser = argparse.ArgumentParser(
        description="🧹 Ultimate Project Cleaner - Versión BRUTAL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python clean.py --all --auto-confirm          # Limpieza completa automática
  python clean.py --duplicates --large-files    # Solo duplicados y archivos grandes
  python clean.py --custom-config config.json   # Usar configuración personalizada
  python clean.py --brutal                      # Modo BRUTAL (todo sin preguntar)
        """,
    )

    parser.add_argument("--all", action="store_true", help="Limpieza completa")
    parser.add_argument(
        "--brutal", action="store_true", help="Modo BRUTAL - Sin confirmaciones"
    )
    parser.add_argument(
        "--duplicates", action="store_true", help="Solo eliminar duplicados"
    )
    parser.add_argument(
        "--large-files", action="store_true", help="Revisar archivos grandes"
    )
    parser.add_argument(
        "--old-files",
        type=int,
        metavar="DAYS",
        help="Eliminar archivos temporales de X días",
    )
    parser.add_argument(
        "--auto-confirm", action="store_true", help="No pedir confirmación"
    )
    parser.add_argument("--project-root", type=str, help="Ruta del proyecto a limpiar")
    parser.add_argument(
        "--config", type=str, help="Archivo de configuración personalizado"
    )
    parser.add_argument(
        "--workers", type=int, default=4, help="Número de workers paralelos"
    )

    args = parser.parse_args()

    # Configurar cleaner
    cleaner = UltimateProjectCleaner(args.project_root)

    if args.brutal:
        args.all = True
        args.auto_confirm = True
        cleaner.config["auto_confirm"] = True
        cleaner.config["safe_mode"] = False

    if args.auto_confirm:
        cleaner.config["auto_confirm"] = True

    if args.workers:
        cleaner.config["parallel_workers"] = args.workers

    # Opciones de limpieza
    options = {}

    if args.all:
        options = {k: True for k in cleaner.patterns}
        options.update(
            {
                "remove_duplicates": True,
                "clean_old_files": True,
                "review_large_files": True,
                "optimize_git": True,
            }
        )
    else:
        options = {
            "remove_duplicates": args.duplicates,
            "review_large_files": args.large_files,
            "clean_old_files": args.old_files is not None,
        }

        if args.old_files:
            cleaner.config["keep_recent_days"] = args.old_files

    # ¡EJECUTAR LIMPIEZA BRUTAL!
    cleaner.clean_ultimate(**options)


if __name__ == "__main__":
    main()

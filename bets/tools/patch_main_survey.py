
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # assume /tools/ inside repo root
main_path = ROOT / "backend" / "app" / "main.py"
app_init = ROOT / "backend" / "app" / "__init__.py"
routes_init = ROOT / "backend" / "app" / "routes" / "__init__.py"

if not main_path.exists():
    raise SystemExit(f"[ERRO] Não encontrei {main_path}. Extraia o zip na raiz do projeto.")

# Garantir pacotes Python
app_init.parent.mkdir(parents=True, exist_ok=True)
routes_init.parent.mkdir(parents=True, exist_ok=True)
app_init.touch(exist_ok=True)
routes_init.touch(exist_ok=True)

src = main_path.read_text(encoding="utf-8")
changed = False

# 1) Inserir import se faltar
if 'from app.routes import survey' not in src:
    lines = src.splitlines()
    last_import_idx = -1
    for i, ln in enumerate(lines):
        if ln.strip().startswith('from ') or ln.strip().startswith('import '):
            last_import_idx = i
    insert_at = last_import_idx + 1 if last_import_idx >= 0 else 0
    lines.insert(insert_at, 'from app.routes import survey')
    src = '\n'.join(lines)
    changed = True
    print('[OK] Inserido: from app.routes import survey')

# 2) Inserir include_router se faltar
if 'app.include_router(survey.router' not in src:
    lines = src.splitlines()
    last_include = -1
    app_decl = -1
    for i, ln in enumerate(lines):
        if 'include_router(' in ln:
            last_include = i
        if 'FastAPI(' in ln and 'app' in ln and '=' in ln:
            app_decl = i
    insert_at = last_include + 1 if last_include >= 0 else (app_decl + 1 if app_decl >= 0 else len(lines))
    lines.insert(insert_at, 'app.include_router(survey.router, prefix="/api")')
    src = '\n'.join(lines)
    changed = True
    print('[OK] Inserido: app.include_router(survey.router, prefix="/api")')

if changed:
    main_path.write_text(src, encoding='utf-8')
    print(f'[SUCESSO] {main_path} atualizado.')
else:
    print('[INFO] Nada a fazer: main.py já está configurado.')

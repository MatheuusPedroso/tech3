
Patch — correção automática do erro + novas funcionalidades
==========================================================

O que há neste pacote
---------------------
1) frontend/streamlit_app.py  -> tela principal atualizada (simulador multimodal + PDF + pesquisa anônima)
2) backend/app/routes/survey.py -> novas rotas para salvar e consultar a pesquisa
3) tools/patch_main_survey.py  -> *aplica automaticamente* a inclusão do router `survey` no seu backend
4) README_patch.txt (este arquivo)

Como aplicar (sem editar arquivos manualmente)
----------------------------------------------
1) Extraia este ZIP na **raiz do seu projeto** (onde existem as pastas `backend/` e `frontend/`).

2) Rode o patch que corrige o erro de `from app.routes import survey` e adiciona a linha do router automaticamente:
   Windows (PowerShell):
       python tools\patch_main_survey.py
   Linux/Mac:
       python3 tools/patch_main_survey.py

   O script vai:
   - localizar `backend/app/main.py`
   - garantir `backend/app/__init__.py` e `backend/app/routes/__init__.py`
   - inserir:
         from app.routes import survey
         app.include_router(survey.router, prefix="/api")
     se ainda não existirem.

3) Garanta `reportlab==3.6.13` no `frontend/requirements.txt` (para o PDF).

4) Suba os serviços:
   Backend:
       cd backend
       uvicorn app.main:app --reload
   Frontend:
       cd frontend
       streamlit run streamlit_app.py

5) Teste rápido:
   - Docs: http://127.0.0.1:8000/docs  (veja o grupo "survey")
   - GET  http://127.0.0.1:8000/api/survey/stats
   - No front, a página "Previsão (principal)" já exibe o botão de PDF e a pesquisa.

from pathlib import Path
import pytest
pytest.importorskip('streamlit')
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1]
def test_app_default_and_physical_error(tmp_path,monkeypatch):
 from core import database as db
 monkeypatch.setattr(db,'DB_PATH',tmp_path/'app.db')
 monkeypatch.setenv('EFICIAGRO_ENABLE_HISTORY','1')
 at=AppTest.from_file(str(ROOT/'app.py')).run(timeout=40)
 assert not at.exception and not at.error
 next(x for x in at.number_input if x.label=='Potência elétrica ativa de entrada (kW)').set_value(.1)
 at.run(timeout=40)
 assert not at.exception and any('100%' in e.value for e in at.error)

def test_app_save_and_pdf(tmp_path,monkeypatch):
 from core import database as db
 monkeypatch.setattr(db,'DB_PATH',tmp_path/'app.db')
 monkeypatch.setenv('EFICIAGRO_ENABLE_HISTORY','1')
 at=AppTest.from_file(str(ROOT/'app.py')).run(timeout=40)
 next(x for x in at.button if x.label=='Salvar análise no histórico local').click().run(timeout=40)
 assert not at.exception and at.success
 next(x for x in at.button if x.label=='Preparar relatório PDF').click().run(timeout=40)
 assert not at.exception

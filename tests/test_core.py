
from core.models import InputData
from core.validation import validate_inputs
from core.scenarios import generate_scenarios, best_scenario

def sample():
    return InputData("Teste","Ilhéus/BA","Café arábica","Gotejamento",5,5.5,6,20,0.95,30)

def test_validacao():
    assert validate_inputs(sample()) == []

def test_consumo_base():
    s = generate_scenarios(sample())[0]
    assert round(s.consumo_anual_kwh, 2) == 7920.00
    assert round(s.custo_anual_rs, 2) == 7524.00

def test_cenarios():
    scenarios = generate_scenarios(sample())
    assert len(scenarios) == 5
    assert best_scenario(scenarios).custo_anual_rs <= scenarios[0].custo_anual_rs

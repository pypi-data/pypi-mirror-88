import pytest
import solary

def test_ast_size():

    ast_radius1 = solary.asteroid.physp.ast_size(albedo=0.05, abs_mag=10.0)
    assert pytest.approx(ast_radius1) == 29.71734

    ast_radius2 = solary.asteroid.physp.ast_size(albedo=0.3, abs_mag=20.0)
    assert pytest.approx(ast_radius2) == 0.12132055
    
    ast_radius3 = solary.asteroid.physp.ast_size(albedo=0.15, abs_mag=26.0)
    assert pytest.approx(ast_radius3) == 0.010825535
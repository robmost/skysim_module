def test_module_import():
    try:
        import skysim_module
    except Exception as e:
        raise AssertionError("Failed to import skysim_module")
    return
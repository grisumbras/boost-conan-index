def update_data(lib, lib_dir, registry):
    for target in lib.targets:
        if target['name'] == 'math':
            target['kind'] = 'header-library'

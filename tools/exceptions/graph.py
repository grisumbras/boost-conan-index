def update_data(lib, lib_dir, registry):
    for i, dep in enumerate(lib.dependencies):
        if dep[0].name == 'geometry':
            del lib.dependencies[i]

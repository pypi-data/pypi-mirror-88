import black
import configparser


def read_config_file():
    config_path = ''
    if not config_path:
        root = black.find_project_root(ctx.params.get("src", ()))
        path = root / "setup.cfg"
        if path.is_file():
            config_path = str(path)
        else:
            return None

    config = configparser.ConfigParser()
    config.read(config_path)
    found = False
    expected_keys = "blacked", "tool:blacked"
    for key in expected_keys:
        try:
            config = config[key]
        except KeyError:
            continue
        else:
            if found:
                black.err(f"Expected only one of {expected_keys} in {config_path}")
            found = True

    if not found or not config:
        return

    for k, v in config.items():
        for command_param in black.main.params:
            if command_param.name == k:
                if command_param.multiple:
                    v = list(map(str.strip, v.split(",")))
                break

        ctx.default_map[k] = v

    return config_path

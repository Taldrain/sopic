# using a new settings (dict) overwrite the values of the default settings (dict)
def overwrite_settings_values(default_settings, settings):
    for key, value in default_settings.items():
        if key in settings:
            default_settings[key]["value"] = settings[key]["value"]

    return default_settings


# extract only the value key to ease the use by the steps
def step_settings(settings):
    res = dict()
    for key, value in settings.items():
        res[key] = value["value"]
    return res

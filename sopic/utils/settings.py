# using a new settings (dict) overwrite the values of the default settings (dict)
def overwrite_settings_values(default_settings, settings):
    for key, value in default_settings.items():
        if key in settings:
            default_settings[key]["value"] = settings[key]["value"]

    return default_settings

# create a new object that will be used for the json settings file. This object
# only contains the value field
def filter_settings_json(settings):
    res = {}
    for key, value in settings.items():
        res[key] = { "value": value["value"] }
    return res

# extract only the value key to ease the use by the steps
def step_settings(settings):
    res = dict()
    for key, value in settings.items():
        res[key] = value["value"]
    return res

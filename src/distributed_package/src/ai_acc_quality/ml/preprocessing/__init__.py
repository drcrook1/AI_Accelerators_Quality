from ...data_models.widget import Widget

COLUMNS = ["voltage", "amperage", "ambient_temp", "ambient_humidity", "flux_capacitance"]

def widget_to_input(widget:Widget):
    if not widget.telemetry:
        return []
    t = widget.telemetry[0].to_dict()[1]
    tcols = [t[i] for i in COLUMNS]
    return [tcols]

def score_preprocessing(model, widget:Widget):
    tcols = widget_to_input(widget)
    preprocessed = model.transform(tcols) #np.array(tcols).reshape(1, -1))
    return preprocessed

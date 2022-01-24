import sounddevice as sd


def get_default_input_device(logger):
    """Attempt to get the default input device."""
    default_input_device = None
    try:
        default_input_device = sd.query_devices(kind='input')['name']
    except Exception as e:
        logger.error("Failed to query input devices, there may be none available; " + str(e), exc_info=False)

    return default_input_device
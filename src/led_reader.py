"""Read PiJuice LED settings without changing hardware state."""

from pijuice_reader import PiJuice


def read_leds(pj=None):
    if pj is None:
        pj = PiJuice(1, 0x14)

    result = {}

    for led in ("D1", "D2"):
        entry = {}

        for field, method in (
            ("state", "GetLedState"),
            ("blink", "GetLedBlink"),
        ):
            try:
                response = getattr(pj.status, method)(led)

                if response.get("error") != "NO_ERROR":
                    raise RuntimeError(response.get("error", "Unknown error"))

                entry[field] = response.get("data")
            except Exception as exc:
                entry[field] = None
                entry[field + "_error"] = str(exc)

        result[led] = entry

    return result

class MotozemError(Exception):
    """
    Základní třída pro všechny vlastní výjimky v projektu Motozem.
    Dědí z ní všechny ostatní, takže můžeme odchytávat 'except MotozemError'.
    """

    pass


class ElementNotVisibleError(MotozemError):
    """
    Vyvolá se, když element není viditelný na stránce v daném časovém limitu.
    """

    def __init__(self, element_name: str, timeout: int):
        self.message = f"Element '{element_name}' nebyl viditelný ani po {timeout} ms."
        super().__init__(self.message)


class TextMismatchError(MotozemError):
    """
    Vyvolá se, když text v elementu neodpovídá očekávání.
    """

    def __init__(self, element_name: str, expected: str, actual: str):
        self.message = f"Element '{element_name}' má text '{actual}', ale očekáváno bylo '{expected}'."
        super().__init__(self.message)


class NetworkResponseError(MotozemError):
    """
    Vyvolá se, když síťový požadavek (API) selže nebo nepřijde včas.
    """

    def __init__(self, url_pattern: str, status: int = None):
        if status:
            self.message = f"Požadavek na '{url_pattern}' vrátil chybu (Status: {status})."
        else:
            self.message = f"Požadavek na '{url_pattern}' nebyl zachycen včas (Timeout)."
        super().__init__(self.message)

class TopAmountExceeded(Exception):
    """Exception raised for errors in generating top graphs.

    Attributes:
        amount -- amount of countries requested
    """
    def __init__(self,amount):
        self.amount = amount
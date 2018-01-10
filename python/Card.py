class Card:
    """ Generic Card class from which all other card classes inherit
    """
    text_string = ""    
    def __init__(self, card_string):
        self.text_string = card_string

    def __str__(self):
        return text_string
        

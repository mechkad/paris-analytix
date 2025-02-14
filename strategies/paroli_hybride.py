class ParoliHybride:
    def __init__(self, capital=1000):
        self.capital = capital
        self.mise = 0.03 * capital
        self.plafond = 0.12
        self.stop_loss = 0.85 * capital
        self.gains_consecutifs = 0

    def parier(self, cote, resultat):
        # ... (coller le reste du code)

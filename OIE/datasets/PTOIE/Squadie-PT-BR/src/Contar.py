class Contar:

    def __init__(self):
        self.explicitas = 0
        self.implicitas = 0
        self.geral = 0

    def increment_explicitas(self):
        self.explicitas+= 1
        self.geral+=1

    def increment_implicitas(self):
        self.implicitas+= 1
        self.geral+=1

    def __str__(self):
        return f"Qnt Explicitas: {self.explicitas}\nQnt Implicitas: {self.implicitas}\nQnt Geral: {self.geral}"
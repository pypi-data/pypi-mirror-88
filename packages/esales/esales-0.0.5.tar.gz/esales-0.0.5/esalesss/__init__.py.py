import random

esales = ['Marlijn', 'Ilona', 'Godelieve', 'Jelmer', 'Hok', 'Angelique', 'Twan']

def allenamen():
  for x in range(len(esales)):
      print(esales[x])
      x += 1


def wiebetaaltmijnlunch():
  print(random.choice(esales))


def verliefd():
  print(random.choice(esales) + " is verliefd op " + random.choice(esales))

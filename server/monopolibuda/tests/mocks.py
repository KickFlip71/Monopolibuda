class MockDice:
  def __init__(self, value):
    self.value = value

  def roll(self):
    return self.value
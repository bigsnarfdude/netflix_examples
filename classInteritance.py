class SplitData1:
    def __init__(self, numbers):
        self.numbers = numbers 
    def split_top(self):
        l = len(self.numbers)
        half = l/2
        top = self.numbers[:half]
        return top

class SplitData2(SplitData1):
    def __init__(self, numbers):
        self.numbers = numbers
    def split_bottom(self):
        l = len(self.numbers)
        half = l/2
        bottom = self.numbers[half:]
        return bottom

numbers = range(10)
x = SplitData2(numbers)

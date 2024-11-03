class Quiz:
    def __init__(self, quiz):
        self.answer = quiz["answer"]
        self.sign = quiz["sign"]
        self.instructions = quiz["instructions"]
        self.combinations = quiz["combinations"]
        self.current_combination = 0

    def is_correct(self, x, y):
        for item in self.combinations:
            if x == item[0] and y == item[1]:
                return True
            
        return False
    
    def get_answer(self):
        return self.answer
    
    def get_sign(self):
        return self.sign
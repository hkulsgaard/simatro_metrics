class MatElement():
    def __init__(self,mat):
        super().__init__()
        self.mat = mat

    def get(self,attribute):
        return self.mat[0][attribute][0][0][:]
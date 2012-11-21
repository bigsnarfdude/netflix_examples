def closed():
    closed.x = 5
    def set_x(xx):
        closed.x = xx
    def get_x():
        return closed.x
        closed.set_x = set_x
        closed.get_x = get_x
        return closed

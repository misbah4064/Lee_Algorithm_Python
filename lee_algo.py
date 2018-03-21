from Queue import *
import Board
import threading
import time

class Field(object):

    def __init__(self, len, start, finish, barriers):
        self._len = len
        self.__start = start
        self.finish = finish
        self._barriers = barriers
        self.__field = None
        self._build()

    def __call__(self, *args, **kwargs):
        self._show()

    def __getitem__(self, item):
        return self.__field[item]

    def _build(self):
        self.__field = [[0 for i in range(self._len)] for i in range(self._len)]
        for b in self._barriers:
            self[b[0]][b[1]] = -1
        self[self.__start[0]][self.__start[1]] = 1

    def emit(self):
        q = Queue()
        q.put(self.__start)
        while not q.empty():
            index = q.get()
            l = (index[0]-1, index[1])
            r = (index[0]+1, index[1])
            u = (index[0], index[1]-1)
            d = (index[0], index[1]+1)

            if l[0] >= 0 and self[l[0]][l[1]] == 0:
                self[l[0]][l[1]] += self[index[0]][index[1]] + 1
                q.put(l)
            if r[0] < self._len and self[r[0]][r[1]] == 0:
                self[r[0]][r[1]] += self[index[0]][index[1]] + 1
                q.put(r)
            if u[1] >= 0 and self[u[0]][u[1]] == 0:
                self[u[0]][u[1]] += self[index[0]][index[1]] + 1
                q.put(u)
            if d[1] < self._len and self[d[0]][d[1]] == 0:
                self[d[0]][d[1]] += self[index[0]][index[1]] + 1
                q.put(d)

    def get_path(self):
        if self[self.finish[0]][self.finish[1]] == 0 or \
                self[self.finish[0]][self.finish[1]] == -1:
            raise

        path = []
        item = self.finish
        while not path.append(item) and item != self.__start:
            l = (item[0]-1, item[1])
            if l[0] >= 0 and self[l[0]][l[1]] == self[item[0]][item[1]] - 1:
                item = l
                continue
            r = (item[0]+1, item[1])
            if r[0] < self._len and self[r[0]][r[1]] == self[item[0]][item[1]] - 1:
                item = r
                continue
            u = (item[0], item[1]-1)
            if u[1] >= 0 and self[u[0]][u[1]] == self[item[0]][item[1]] - 1:
                item = u
                continue
            d = (item[0], item[1]+1)
            if d[1] < self._len and self[d[0]][d[1]] == self[item[0]][item[1]] - 1:
                item = d
                continue
        return path

    def update(self):
        self.__field = [[0 for i in range(self._len)] for i in range(self._len)]

    def _show(self):
        for i in self:
            for j in i:
                print j,
            print

#initialization
lenB = Board.size
startB = Board.player
finishB = Board.end
barriersB = Board.Walls
field = Field(len=lenB, start=startB, finish=finishB, barriers=barriersB)
field.emit() #processes the maze
path = field.get_path()
path.reverse()

def run():
    global path
    for i in range(lenB):
        for j in range(lenB):
            if (field[i][j]>0):
                Board.render_block((i,j),"gray"+str(100-field[i][j])) #send gradient color information
                time.sleep(0.01)
    Board.render_block(finishB,"red") #mark the end point
    Board.render_path(path)

t = threading.Thread(target=run)
t.daemon = True
t.start()
Board.start_game()

import copy as cp


class Node:

    def __init__(self, moves):
        self.obj = None
        self.distance = None
        self.moves = cp.deepcopy(moves)

    def compute_distance(self, data):
        self.distance = self.obj.compare_to_data(data)
        # print("Did", self.distance)
        # self.obj.print_arg()
        # print(self.obj.R)

    def do_move(self, data):
        move = self.moves.pop(0)
        new = Node(self.moves)
        new.obj = cp.deepcopy(self.obj)
        added = new.obj.add(move)
        new.update_moves(move, added)
        new.compute_distance(data)
        """print("MOVESSSSS")
        print(id(self))
        print(self.moves)
        print(new.moves)
        print(self.obj.R)
        print(new.obj.R)
        print(move)
        print(added)"""
        return new

    def can_move(self):
        return len(self.moves) > 0

    def update_moves(self, move, added):
        if added:
            for a in self.obj.A:
                if a.name != move[0] and a.name != 'T':
                    self.moves.append((a.name, move[0]))


class AStar:

    def __init__(self, root, data):
        self.nodes = [root]
        self.data = data
        self.nodes[0].distance = len(data)

    def add_node(self):
        self.nodes = sorted(self.nodes, key=lambda x: x.distance +
                            100 * (1 - int(len(x.moves) > 0)) + (len(x.obj.A) + len(x.obj.R)) / 100.0)
        if self.nodes[0].can_move():
            self.nodes.append(self.nodes[0].do_move(self.data))
            return True
        return False

    def run(self, max_loop=None):
        good = True
        count = 0
        while good:
            good = self.add_node()
            if count % 100 == 0:
                print("Step:", count)
                print("\tDistance:", self.nodes[0].distance)
                if count % 1000 == 0:
                    print("BEST:")
                    self.nodes = sorted(self.nodes, key=lambda x: x.distance)
                    print(self.nodes[0].distance)
                    self.nodes[0].obj.print_arg()
                    print(self.nodes[0].obj.R)

            count += 1
            if max_loop is not None and count >= max_loop:
                good = False

        print("BEST:")
        self.nodes = sorted(self.nodes, key=lambda x: x.distance)
        print(self.nodes[0].distance)
        self.nodes[0].obj.print_arg()
        print(self.nodes[0].obj.R)



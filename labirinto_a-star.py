from pyamaze import COLOR, maze, agent, textLabel
from queue import PriorityQueue

def h(cell1, cell2): # heuristica
    x1, y1 = cell1
    x2, y2 = cell2
    return (abs(x1 - x2) + abs(y1 - y2))

def aStar(m):
    start = (m.rows, m.cols)

    open = PriorityQueue()
    open.put((h(start, m._goal), h(start, m._goal), start))  # f(n), h(n), cell

    aPath = {}

    g_score = {cell: float('inf') for cell in m.grid} # custo do caminho do inicio ate o no atual
    g_score[start] = 0

    f_score = {cell: float('inf') for cell in m.grid} # custo total - heuristica
    f_score[start] = h(start, m._goal)
    
    searchPath = [start]
    while not open.empty():
        currentCell = open.get()[2]
        # print(currentCell)
        searchPath.append(currentCell)

        if currentCell == m._goal:
            break

        for d in 'ESNW':
            if m.maze_map[currentCell][d] == True:  # {(1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0}} -> se for 1 é igual a True
                if d == 'E':
                    childCell = (currentCell[0], currentCell[1] + 1)
                elif d == 'W':
                    childCell = (currentCell[0], currentCell[1] - 1)
                elif d == 'S':
                    childCell = (currentCell[0] + 1, currentCell[1])
                elif d == 'N':
                    childCell = (currentCell[0] - 1, currentCell[1])
                
                temp_g_score = g_score[currentCell] + 1
                temp_f_score = temp_g_score + h(childCell, m._goal) # temporaria, para comparar com o f_score

                if temp_f_score < f_score[childCell]:
                    aPath[childCell] = currentCell
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((f_score[childCell], h(childCell, m._goal), childCell))
                    
    fwd_path = {}
    cell = m._goal

    while cell != start:
        fwd_path[aPath[cell]] = cell
        cell = aPath[cell]

    return fwd_path, searchPath

if __name__ == '__main__':
    m = maze(10, 10)
    m.CreateMaze()
    path, searchPath = aStar(m)

    ponto = agent(m, footprints = True, color=COLOR.red) # pontinho azul
    pensamento = agent(m, footprints = True, color = COLOR.blue, filled = True)
    m.tracePath({pensamento: searchPath}, delay=100)
    m.tracePath({ponto: path}, delay=100)

    l = textLabel(m, 'A*', len(path) + 1)

    # print(m.maze_map)

    m.run()
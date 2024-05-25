from pyamaze import COLOR, maze, agent, textLabel
from queue import PriorityQueue

def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

def aStar(m):
    start = (m.rows, m.cols)

    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0

    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, (1, 1))

    open = PriorityQueue()
    open.put((h(start, (1, 1)), h(start, (1, 1)), start))

    aPath = {}
    searchPath = [start]
    while not open.empty():
        currentCell = open.get()[2]
        searchPath.append(currentCell)

        if currentCell == (1, 1):
            break

        for d in 'ESNW':
            if m.maze_map[currentCell][d] == True:
                if d == 'E':
                    childCell = (currentCell[0], currentCell[1] + 1)
                if d == 'W':
                    childCell = (currentCell[0], currentCell[1] - 1)
                if d == 'S':
                    childCell = (currentCell[0] + 1, currentCell[1])
                if d == 'N':
                    childCell = (currentCell[0] - 1, currentCell[1])
                
                temp_g_score = g_score[currentCell] + 1
                temp_f_score = temp_g_score + h(childCell, (1, 1)) # temporaria, para comparar com o f_score

                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, h(childCell, (1, 1)), childCell))
                    aPath[childCell] = currentCell
    fwd_path = {}
    cell = (1, 1)

    while cell != start:
        fwd_path[aPath[cell]] = cell
        cell = aPath[cell]

    return fwd_path, searchPath

if __name__ == '__main__':
    m = maze(20, 20)
    m.CreateMaze()
    path, searchPath = aStar(m)

    ponto = agent(m, footprints = True, color=COLOR.red) # pontinho azul
    pensamento = agent(m, footprints = True, color = COLOR.blue, filled = True)
    m.tracePath({pensamento: searchPath}, delay=100)
    m.tracePath({ponto: path}, delay=100)

    l = textLabel(m, 'A*', len(path) + 1)

    # print(m.maze_map)

    m.run()
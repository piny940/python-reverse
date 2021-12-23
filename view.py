import tkinter as tk

window = tk.Tk()
window.title("Revrese")
window.geometry("500x500")

canvas = tk.Canvas(window, width = 500, height = 500)
canvas.grid(row = 0, column = 0)

CellSize = 50
BoardMargin = 50

canvas.create_line(250, 50, 250, 450, width = 400, fill = "green")
for i in range(9):   
    canvas.create_line(BoardMargin+i*CellSize, BoardMargin,
        BoardMargin+i*CellSize, CellSize*8+ BoardMargin, fill = "black")
    canvas.create_line(BoardMargin, BoardMargin+i*CellSize, 
        CellSize*8+BoardMargin, BoardMargin+i*CellSize, fill = "black")

window.mainloop()
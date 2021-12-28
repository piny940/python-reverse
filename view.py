import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Revresi")
window.geometry("800x550")

# Menu
# TODO: several functions to be called when submenu is clicked
def temporaryFunction(): # <- temporary
    messagebox.showinfo(title = "info", message = "submenu was clicked.")

mainmenu = tk.Menu(window)
submenu = tk.Menu(mainmenu, tearoff = 0)

mainmenu.add_cascade(label = "Menu", menu = submenu)
submenu.add_command(label = "New game", command = temporaryFunction)
submenu.add_command(label = "Switch mode", command = temporaryFunction)
window.config(menu = mainmenu)

# Show game title.
label1 = tk.Label(window, text = "Reversi", font = "Times 25",
    width= 8,height= 1)
label1.grid(row = 0, column = 0)

# Show game mode.
# TODO: I need to know game-mode and set opponent.
opponent = "Player" # <- temporary

label2 = tk.Label(window, text = "vs "+opponent, font = "Times 25",
    width= 10, height= 1)
label2.grid(row = 0, column = 1)

# Show number of stones.
# TODO: I need to know the number of black and white stone.
NumberOfBlackStone = str(0) # <- temporary
NumberOfWhiteStone = str(0) # <- temporary

NumberOfStonesLabel = tk.Label(window, font = "Times 25",
    text = f"Black:{NumberOfBlackStone}\nWhite:{NumberOfWhiteStone}")
NumberOfStonesLabel.grid(row = 3, column = 1)

# Show Pass-button.
#def temporaryPassFunction(): # <- temporary
#    messagebox.showinfo(title = "info", message = "Pass was clicked.")
#PassButton = tk.Button(window, text = "Pass",font = "Times 20",
#    width = 10, height = 2, command = temporaryPassFunction)
#PassButton.grid(row = 4,column = 1)

# Show board.
BoardCanvasSize = 500
CellSize = 50
BoardMargin = (BoardCanvasSize-CellSize*8)/2

canvas = tk.Canvas(window, width = BoardCanvasSize, height = BoardCanvasSize)
canvas.grid(row = 1, column = 0, rowspan = 5)

canvas.create_line(BoardCanvasSize/2, BoardMargin,
    BoardCanvasSize/2, BoardCanvasSize-BoardMargin,
    width = BoardCanvasSize-BoardMargin*2, fill = "green")
for i in range(9):  
    canvas.create_line(BoardMargin+i*CellSize, BoardMargin,
        BoardMargin+i*CellSize, CellSize*8+ BoardMargin, fill = "black")
    canvas.create_line(BoardMargin, BoardMargin+i*CellSize, 
        CellSize*8+BoardMargin, BoardMargin+i*CellSize, fill = "black")

window.mainloop()
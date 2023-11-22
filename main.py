from tkinter import *
from tkinter import filedialog
from PIL import ImageGrab
from win32gui import GetWindowRect, FindWindow
from positions import positions

# creating the window
root = Tk()
root.title("Football formation creator")
root.geometry("800x600")
canvas = Canvas(root, width=800, height=600)


# drawing the pitch function
def draw_pitch():
    canvas.delete()
    canvas.create_rectangle(0, 0, 797, 566, fill="green")
    canvas.place(x=0, y=30)


# drawing the team name function
def update_team_name(*args):
    updated_name = Label(root, text=name.get(), justify="center", fg="white", bg="green", font=("Arial", 24))
    updated_name.place(x=400, y=80, width="794", anchor="center")


# drawing the formation function
def draw_formation():
    for index, position in enumerate(positions[formation_selected.get()]):
        canvas.create_oval(position[0] - 15, position[1] - 15, position[0] + 15, position[1] + 15,
                           fill=color_selected.get())
        canvas.create_text(position[0], position[1] + 30, text=players[index], fill="white", font=("Arial", 12))


# updating formation function
def update_formation(*args):
    draw_pitch()
    draw_formation()


# changing players names function
def change_names():
    dialog = Toplevel(root)
    dialog.title("Change Player Names")

    entry_fields = []
    for i in range(11):
        label = Label(dialog, text=f"Player {i + 1}")
        label.grid(row=i, column=0, padx=(10, 5), pady=5, sticky="e")

        entry_var = StringVar()
        entry = Entry(dialog, textvariable=entry_var, width=20)
        entry.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="w")

        entry_var.set(players[i])
        entry_fields.append(entry_var)

    def update_names():
        for i in range(11):
            players[i] = entry_fields[i].get()
        dialog.destroy()
        update_formation()

    ok_button = Button(dialog, text="OK", command=update_names)
    ok_button.grid(row=11, column=0, columnspan=2, pady=10)


# exporting formation function
def save_formation():
    win = FindWindow(None, "Football formation creator")
    window_rect = GetWindowRect(win)
    left, top, right, bottom = window_rect
    image = ImageGrab.grab(bbox=(left + 10, top + 66, right - 10, bottom - 12))

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
    if file_path:
        image.save(file_path)


# creating lists of formations, colors and players
formations = ["1-3-4-3", "1-3-5-2", "1-4-3-3", "1-4-4-2", "1-4-5-1", "1-5-3-2"]
colors = ["white", "black", "blue", "purple", "red", "yellow"]
players = []
for i in range(1, 12):
    players.append(f"Player {i}")

# name label and entry field
name_label = Label(root, text="Name")
name_label.grid(row=0, column=0, padx=(2, 0))
name = StringVar()
name_field = Entry(root, text=name, width=18)
name_field.grid(row=0, column=1)

# formation label and dropdown list
formation_label = Label(root, text="Formation")
formation_label.grid(row=0, column=2, padx=(44, 0))
formation_selected = StringVar()
formation_selected.set(formations[0])
formation_drop = OptionMenu(root, formation_selected, *formations)
formation_drop.grid(row=0, column=3)

# shirt color label and dropdown list
color_label = Label(root, text="Shirt color")
color_label.grid(row=0, column=4, padx=(44, 0))
color_selected = StringVar()
color_selected.set(colors[0])
color_drop = OptionMenu(root, color_selected, *colors)
color_drop.grid(row=0, column=5)
color_drop.config(width=6)

# change player names button
change_names_button = Button(root, text="Change player names", command=change_names)
change_names_button.grid(row=0, column=6, padx=(44, 0))

# export button
save_button = Button(root, text="Save as...", command=save_formation)
save_button.grid(row=0, column=7, padx=(44, 0))

draw_pitch()
draw_formation()
name.trace("w", update_team_name)
color_selected.trace("w", update_formation)
formation_selected.trace("w", update_formation)

root.resizable(False, False)
root.mainloop()

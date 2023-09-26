import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from functions import *
from analyzer import removePointsNotTouchingCross


# patternUI global variables
clickedCircles = []
circle_dict = {}


def visualize_grid_pattern(pattern, frame, clickable):
    fig = Figure(figsize=(2, 2), facecolor="blue")
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.set_facecolor("gray")
    ax.set_xticks([])
    ax.set_yticks([])

    circle_radius = 0.15
    row_count = 3
    col_count = 3
    circle_index = 0

    def on_circle_click(event):

        # Update focus point
        global entryInfocus
        entryInfocus = False
        # Get the row and column of the clicked circle
        col = int(event.xdata)
        row = row_count - 1 - int(event.ydata)
        circle_id = (row, col)

        # Get the equivalent number in the pattern
        circle_num = tuple_to_number(circle_id)
        # Check if the circle_id is in clickedCircles list
        if circle_num in clickedCircles:
            clickedCircles.remove(circle_num)
        else:
            clickedCircles.append(circle_num)

        # Check if the circle_id is in the circle_dict
        if circle_id in circle_dict:
            circle = circle_dict[circle_id]

            # Check the current circle color
            current_color = circle.get_facecolor()

            # Toggle circle color and fill
            if current_color == to_rgba('black'):
                circle.set_facecolor('white')
            else:
                circle.set_facecolor('black')
            fig.canvas.draw_idle()  # Update the plot
            return

    for row in range(row_count):

        for col in range(col_count):
            circle_index += 1
            if (row, col) in pattern:
                circle_x = col + 0.5
                circle_y = row_count - row - 0.5

                # Paint the First circle green and the last red
                if (row, col) == pattern[-1]:
                    circle = plt.Circle((circle_x, circle_y),
                                        circle_radius, color='red', fill=True)
                elif (row, col) == pattern[0]:
                    circle = plt.Circle((circle_x, circle_y),
                                        circle_radius, color='green', fill=True)
                else:
                    circle = plt.Circle((circle_x, circle_y),
                                        circle_radius, color='black', fill=True)

                ax.add_artist(circle)

            else:
                circle_x = col + 0.5
                circle_y = row_count - row - 0.5
                if clickable:
                    circle = plt.Circle((circle_x, circle_y),
                                        circle_radius, facecolor='black', fill=True)
                else:
                    circle = plt.Circle((circle_x, circle_y),
                                        circle_radius, facecolor='white', fill=False)

                ax.add_artist(circle)

            if clickable:
                # Add the circle to the circle_dict
                circle_dict[(row, col)] = circle

    ax.set_xlim(0, col_count)
    ax.set_ylim(0, row_count)

    for i in range(len(pattern) - 1):
        x_start = pattern[i][1] + 0.5
        y_start = row_count - pattern[i][0] - 0.5
        x_end = pattern[i + 1][1] + 0.5
        y_end = row_count - pattern[i + 1][0] - 0.5

        arrowprops = dict(arrowstyle='->', color='blue',
                          lw=1.5, mutation_scale=10)
        ax.annotate("", xy=(x_end, y_end), xytext=(
            x_start, y_start), arrowprops=arrowprops)

    # Specify boundary size between fig and ax
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    if clickable:
        # Bind the click event to the circle
        canvas.mpl_connect('button_press_event', on_circle_click)
    canvas.get_tk_widget().pack()
    return


# Will determine if the pattern will be generated from the patternUI or the entry
entryInfocus = False


def get_entryInFocus():
    """
        Returns the entryInFocus variable
    """
    global entryInfocus
    return entryInfocus


def update_entryInFocus(event):
    """
        Checks if the entry is in focus.
        This will determine if the generated pattern will be from the patternUI or the Entry box
    """
    global entryInfocus
    entryInfocus = True
    return


# Create a Tkinter window
root = tk.Tk()
root.title("Pattern Cracker")
root.config(bg="grey")
win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()
root.geometry("%dx%d" % (win_width, win_height))


# Create a frame within the root window to hold the everything
mainFrame = ttk.Frame(root)
mainFrame.pack(fill="both", expand=True)

# Labels and buttons in the frame
label = tk.Label(mainFrame, text="Enter Pattern Nums", font=("Arial", 10))
label.place(x=250, y=10)

patternEntry = tk.Entry(mainFrame, bg="grey", fg="white")
patternEntry.place(x=250, y=40)
patternEntry.bind("<FocusIn>", update_entryInFocus)

generatePatternsBtn = tk.Button(
    mainFrame, text="GENERATE", bg="green", fg="white")
generatePatternsBtn.place(x=280, y=70)


uiLabel = tk.Label(mainFrame, text="Select used points")
uiLabel.place(x=20, y=10)

# Frame for inputing the pattern graphically
patternUI = tk.Frame(mainFrame, bg="grey", height=100, width=200)
patternUI.place(x=10, y=30)
visualize_grid_pattern([], patternUI, True)  # Create a clickable pattern

# Fine tuning GUI elements
ftLabel = tk.Label(mainFrame, text="Fine Tuning Options")
ftLabel.place(x=470, y=10)

# Create variables to store the checkbox states
checkbox1_var = tk.BooleanVar()
checkbox2_var = tk.BooleanVar()


# Checkboxes
checkbox1 = ttk.Checkbutton(root, text="Must touch cross", variable=checkbox1_var)
checkbox1.place(x=470, y=40)
checkbox2 = ttk.Checkbutton(
    root, text="Remove invalid patterns", variable=checkbox2_var)
checkbox2.place(x=470, y=60)


exists = False  # If a user had generated patterns before


def getExists():
    # Check if a user had generated patterns before
    global exists
    return exists


def generate_button_click():
    """
        Handles events and logic when the GENERATE button is clicked
    """
    global exists, patternsCanvas, frame, scrollbar, entryInfocus
    if getExists():
        patternsCanvas.destroy()
        frame.destroy()
        scrollbar.destroy()

    # Get selected points on the patternUI or get from the patternEntry
    if get_entryInFocus():
        patternString = patternEntry.get()
        pattern = [int(num) for num in patternString]
    else:
        pattern = clickedCircles

    # Generate pattern based on fine tuning options
    if checkbox1_var.get() and checkbox2_var.get():
        patterns = convert_to_tuple(removePointsNotTouchingCross(
            remove_invalid_combinations(generate_combinations(pattern))))
    elif checkbox1_var.get():
        patterns = convert_to_tuple(
            removePointsNotTouchingCross(generate_combinations(pattern)))

    elif checkbox2_var.get():
        patterns = convert_to_tuple(
            remove_invalid_combinations(generate_combinations(pattern)))
    else:
        patterns = convert_to_tuple(generate_combinations(pattern))

    patternsCanvas = tk.Canvas(
        mainFrame, height=win_height-320, width=1350, bg="grey")
    patternsCanvas.place(x=0, y=250)
    # Create a frame inside the patternsCanvas for the grid patterns
    frame = tk.Frame(patternsCanvas, bg="grey")
    patternsCanvas.create_window((0, 0), window=frame, anchor="nw")

    # Create frames dynamically based on the number of grid patterns
    num_patterns = len(patterns)
    num_columns = 6  # Number of columns in the patternsCanvas

    for i in range(num_patterns):
        subframe = tk.Frame(frame)
        subframe.grid(row=i // num_columns, column=i %
                      num_columns, padx=10, pady=10)

        pattern = patterns[i]
        visualize_grid_pattern(pattern, subframe, False)

    # Add a scrollbar to the canvasFrame
    scrollbar = ttk.Scrollbar(mainFrame, orient="vertical",
                              command=patternsCanvas.yview)
    scrollbar.pack(side="right", fill="y")

    patternsCanvas.configure(yscrollcommand=scrollbar.set)
    patternsCanvas.bind("<Configure>", lambda e: patternsCanvas.configure(
        scrollregion=patternsCanvas.bbox("all")))


    # Update the canvas scroll region after all frames are added
    patternsCanvas.update_idletasks()
    patternsCanvas.configure(scrollregion=patternsCanvas.bbox("all"))

    # Configure the canvas to scroll with the scrollbar
    patternsCanvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=patternsCanvas.yview)

    exists = True
    return


generatePatternsBtn.config(command=generate_button_click)
# Start the Tkinter event loop

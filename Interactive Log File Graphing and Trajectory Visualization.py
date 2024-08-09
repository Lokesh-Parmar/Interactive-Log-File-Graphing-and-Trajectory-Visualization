import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Grapher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grapher")
        self.geometry("800x600")
        
        self.file_path = None
        self.df = None
        self.plot_colors = {}

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")
        
        self.create_widgets()
    
    def create_widgets(self):
        self.create_file_tab()
        self.create_plot_tab()
        self.create_trajectory_tab()
    
    def create_file_tab(self):
        self.file_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.file_tab, text="File")

        file_frame = tk.Frame(self.file_tab)
        file_frame.pack(pady=20)

        self.file_type_label = tk.Label(file_frame, text="Select File Type:")
        self.file_type_label.grid(row=0, column=0, padx=5)

        self.file_type_var = tk.StringVar(self)
        self.file_type_var.set(".csv")
        
        self.file_type_option = tk.OptionMenu(file_frame, self.file_type_var, ".csv", ".txt", ".xlsx")
        self.file_type_option.grid(row=0, column=1, padx=5)
        
        self.load_file_button = tk.Button(file_frame, text="Load File", command=self.load_file)
        self.load_file_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_plot_tab(self):
        self.plot_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.plot_tab, text="Plot Graph")

        plot_frame = tk.Frame(self.plot_tab)
        plot_frame.pack(pady=20)

        self.x_var = tk.StringVar(self.plot_tab)
        self.y_var = tk.StringVar(self.plot_tab)
        self.line_color = "blue"

        tk.Label(plot_frame, text="Choose X axis:").grid(row=0, column=0, padx=5)
        self.x_option_menu = tk.OptionMenu(plot_frame, self.x_var, "")
        self.x_option_menu.grid(row=0, column=1, padx=5)

        tk.Label(plot_frame, text="Choose Y axis:").grid(row=1, column=0, padx=5)
        self.y_option_menu = tk.OptionMenu(plot_frame, self.y_var, "")
        self.y_option_menu.grid(row=1, column=1, padx=5)

        tk.Button(plot_frame, text="Choose Line Color", command=self.choose_line_color).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(plot_frame, text="Plot", command=self.plot_selected_graph).grid(row=3, column=0, columnspan=2, pady=10)

        self.add_param_frame = tk.Frame(self.plot_tab)
        self.add_param_frame.pack(pady=20)

        tk.Label(self.add_param_frame, text="Choose Y axis to add:").grid(row=0, column=0, padx=5)
        self.new_y_var = tk.StringVar(self.add_param_frame)
        self.new_y_option_menu = tk.OptionMenu(self.add_param_frame, self.new_y_var, "")
        self.new_y_option_menu.grid(row=0, column=1, padx=5)

        tk.Button(self.add_param_frame, text="Choose Line Color", command=self.choose_new_line_color).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.add_param_frame, text="Add Parameter", command=self.plot_new_parameter).grid(row=2, column=0, columnspan=2, pady=10)

        self.plot_canvas = None
        self.fig, self.ax = plt.subplots(figsize=(8, 6))

    def create_trajectory_tab(self):
        self.trajectory_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trajectory_tab, text="Show Trajectory")

        trajectory_frame = tk.Frame(self.trajectory_tab)
        trajectory_frame.pack(pady=20)

        self.x_traj_var = tk.StringVar(self.trajectory_tab)
        self.y_traj_var = tk.StringVar(self.trajectory_tab)

        tk.Label(trajectory_frame, text="Choose X coordinate:").grid(row=0, column=0, padx=5)
        self.x_traj_option_menu = tk.OptionMenu(trajectory_frame, self.x_traj_var, "")
        self.x_traj_option_menu.grid(row=0, column=1, padx=5)

        tk.Label(trajectory_frame, text="Choose Y coordinate:").grid(row=1, column=0, padx=5)
        self.y_traj_option_menu = tk.OptionMenu(trajectory_frame, self.y_traj_var, "")
        self.y_traj_option_menu.grid(row=1, column=1, padx=5)

        tk.Button(trajectory_frame, text="Show", command=self.plot_trajectory).grid(row=2, column=0, columnspan=2, pady=10)

    def load_file(self):
        file_types = [("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        self.file_path = filedialog.askopenfilename(title="Open File", filetypes=file_types)
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return False
        
        file_extension = self.file_path.split(".")[-1]
        if file_extension == "csv":
            self.df = pd.read_csv(self.file_path)
        elif file_extension == "txt":
            self.df = pd.read_csv(self.file_path, delimiter="\t")
        elif file_extension == "xlsx":
            self.df = pd.read_excel(self.file_path)
        else:
            messagebox.showerror("Error", "Unsupported file format!")
            return False

        columns = list(self.df.columns)
        self.x_var.set(columns[0])
        self.y_var.set(columns[1])
        self.new_y_var.set(columns[1])
        self.x_traj_var.set(columns[0])
        self.y_traj_var.set(columns[1])
        
        self.x_option_menu['menu'].delete(0, 'end')
        self.y_option_menu['menu'].delete(0, 'end')
        self.new_y_option_menu['menu'].delete(0, 'end')
        self.x_traj_option_menu['menu'].delete(0, 'end')
        self.y_traj_option_menu['menu'].delete(0, 'end')

        for col in columns:
            self.x_option_menu['menu'].add_command(label=col, command=tk._setit(self.x_var, col))
            self.y_option_menu['menu'].add_command(label=col, command=tk._setit(self.y_var, col))
            self.new_y_option_menu['menu'].add_command(label=col, command=tk._setit(self.new_y_var, col))
            self.x_traj_option_menu['menu'].add_command(label=col, command=tk._setit(self.x_traj_var, col))
            self.y_traj_option_menu['menu'].add_command(label=col, command=tk._setit(self.y_traj_var, col))
        
        messagebox.showinfo("Success", "File loaded successfully")
        return True
    
    def choose_line_color(self):
        color = colorchooser.askcolor()[1]
        self.line_color = color

    def plot_selected_graph(self):
        x_col = self.x_var.get()
        y_col = self.y_var.get()

        self.ax.clear()
        self.ax.plot(self.df[x_col], self.df[y_col], marker='o', color=self.line_color, label=f'{y_col}')
        self.plot_colors = {y_col: self.line_color}
        self.ax.set_xlabel(x_col)
        self.ax.set_ylabel("Values")
        self.ax.set_title(f'Graph: {x_col} vs Parameters')
        self.ax.legend()
        self.ax.grid(True)

        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().pack_forget()

        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.plot_tab)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.plot_canvas, self.plot_tab)
        self.toolbar.update()
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def choose_new_line_color(self):
        color = colorchooser.askcolor()[1]
        self.new_line_color = color

    def plot_new_parameter(self):
        x_col = self.x_var.get()
        new_y_col = self.new_y_var.get()

        if new_y_col in self.plot_colors:
            messagebox.showerror("Error", f"{new_y_col} is already plotted!")
            return

        self.ax.plot(self.df[x_col], self.df[new_y_col], marker='o', color=self.new_line_color, label=f'{new_y_col}')
        self.plot_colors[new_y_col] = self.new_line_color
        self.ax.legend()

        self.plot_canvas.draw()

    def plot_trajectory(self):
        x_col = self.x_traj_var.get()
        y_col = self.y_traj_var.get()

        self.ax.clear()
        self.ax.plot(self.df[x_col], self.df[y_col], marker='o', linestyle='-', color='r', label='Trajectory')
        self.ax.set_xlabel(x_col)
        self.ax.set_ylabel(y_col)
        self.ax.set_title(f'Trajectory: {x_col} and {y_col}')
        self.ax.legend()
        self.ax.grid(True)

        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().pack_forget()

        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.trajectory_tab)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.plot_canvas, self.trajectory_tab)
        self.toolbar.update()
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    app = Grapher()
    app.mainloop()

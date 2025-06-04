import os
import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox

FILE_PATH = r"C:\Users\saqom\OneDrive\Deskto\Folders\vscode folder\reputation\reputation.json"

class ReputationTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("D&D Reputation Tracker")
        self.root.geometry("600x600")
        self.style = ttk.Style()
        self.place_visibility = {}
        self.places = self.load_data()
        
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=BOTH, expand=True)
        
        header_label = ttk.Label(self.main_frame, text="D&D Reputation Tracker", bootstyle="primary", font=("Helvetica", 16, "bold"))
        header_label.pack(pady=10)
        
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=X, pady=5)
        
        add_place_btn = ttk.Button(top_frame, text="Add Place", bootstyle="success", command=self.add_place)
        add_place_btn.pack(side=LEFT, padx=5)
        
        self.canvas = ttk.Canvas(self.main_frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.display_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.display_frame, anchor="nw")
        self.display_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.refresh_display()
    
    def load_data(self):
        if os.path.exists(FILE_PATH):
            try:
                with open(FILE_PATH, "r") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")
        return {}
    
    def save_data(self):
        try:
            directory = os.path.dirname(FILE_PATH)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(FILE_PATH, "w") as f:
                json.dump(self.places, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    
    def refresh_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        if not self.places:
            ttk.Label(self.display_frame, text="No places added yet.").pack(pady=10)
            return
        
        for place in self.places:
            place_frame = ttk.Frame(self.display_frame, bootstyle="secondary", padding=10)
            place_frame.pack(fill=X, padx=5, pady=5)
            
            header_frame = ttk.Frame(place_frame)
            header_frame.pack(fill=X)
            
            # Reputation controls for the place
            ttk.Button(header_frame, text="-5", bootstyle="info", command=lambda p=place: self.modify_place_reputation(p, -5)).grid(row=0, column=0, padx=2)
            ttk.Button(header_frame, text="-", bootstyle="info", command=lambda p=place: self.modify_place_reputation(p, -1)).grid(row=0, column=1, padx=2)
            
            name_label = ttk.Label(header_frame, text=place, font=("Helvetica", 12, "bold"))
            name_label.grid(row=0, column=2, sticky="w", padx=5)
            
            ttk.Button(header_frame, text="+", bootstyle="info", command=lambda p=place: self.modify_place_reputation(p, 1)).grid(row=0, column=3, padx=2)
            ttk.Button(header_frame, text="+5", bootstyle="info", command=lambda p=place: self.modify_place_reputation(p, 5)).grid(row=0, column=4, padx=2)
            
            rep_entry = ttk.Entry(header_frame, width=5, justify="center", font=("Helvetica", 14))
            rep_entry.insert(0, str(self.places[place]["reputation"]))
            rep_entry.grid(row=0, column=5, padx=2)
            rep_entry.bind("<Return>", lambda e, p=place, entry=rep_entry: self.set_place_reputation(p, entry.get()))
            
            # Add People button for the place
            ttk.Button(header_frame, text="Add People", bootstyle="info", command=lambda p=place: self.add_people(p)).grid(row=0, column=6, padx=5)
            # Hide/Show button for people under the place
            btn_text = "Hide" if self.place_visibility.get(place, True) else "Show"
            ttk.Button(header_frame, text=btn_text, bootstyle="secondary", command=lambda p=place: self.toggle_visibility(p)).grid(row=0, column=7, padx=5)
            # Delete Place button
            ttk.Button(header_frame, text="X", bootstyle="danger", command=lambda p=place: self.delete_place(p)).grid(row=0, column=8, padx=2)
            
            # People display frame
            people_frame = ttk.Frame(place_frame)
            people_frame.pack(fill=X, padx=10, pady=5)
            
            if self.place_visibility.get(place, True):
                for person, rep in self.places[place].get("people", {}).items():
                    person_frame = ttk.Frame(people_frame)
                    person_frame.pack(fill=X, pady=2)
                    # Layout: [Name]  -5, -, [number], +, +5
                    ttk.Label(person_frame, text=person, font=("Helvetica", 10)).grid(row=0, column=0, padx=5, sticky=W)
                    ttk.Button(person_frame, text="-5", bootstyle="info", command=lambda p=place, person=person: self.modify_person_reputation(p, person, -5)).grid(row=0, column=1, padx=2)
                    ttk.Button(person_frame, text="-", bootstyle="info", command=lambda p=place, person=person: self.modify_person_reputation(p, person, -1)).grid(row=0, column=2, padx=2)
                    
                    entry = ttk.Entry(person_frame, width=5, justify="center", font=("Helvetica", 10))
                    entry.insert(0, str(rep))
                    entry.grid(row=0, column=3, padx=2)
                    entry.bind("<Return>", lambda e, p=place, person=person, entry=entry: self.set_person_reputation(p, person, entry.get()))
                    
                    ttk.Button(person_frame, text="+", bootstyle="info", command=lambda p=place, person=person: self.modify_person_reputation(p, person, 1)).grid(row=0, column=4, padx=2)
                    ttk.Button(person_frame, text="+5", bootstyle="info", command=lambda p=place, person=person: self.modify_person_reputation(p, person, 5)).grid(row=0, column=5, padx=2)
    
    def add_place(self):
        place_name = simpledialog.askstring("Add Place", "Enter place name:")
        if place_name and place_name not in self.places:
            self.places[place_name] = {"reputation": 50, "people": {}}
            self.save_data()
            self.refresh_display()
        elif place_name:
            messagebox.showerror("Error", "Place already exists!")
    
    def add_people(self, place_name):
        person_name = simpledialog.askstring("Add Person", "Enter person's name:")
        if person_name:
            if person_name in self.places[place_name]["people"]:
                messagebox.showerror("Error", "Person already exists!")
            else:
                self.places[place_name]["people"][person_name] = 50
                self.save_data()
                self.refresh_display()
    
    def delete_place(self, place_name):
        if messagebox.askyesno("Confirm", f"Delete place '{place_name}'?"):
            del self.places[place_name]
            self.save_data()
            self.refresh_display()
    
    def modify_place_reputation(self, place_name, delta):
        self.places[place_name]["reputation"] = max(0, min(100, self.places[place_name]["reputation"] + delta))
        self.save_data()
        self.refresh_display()
    
    def set_place_reputation(self, place_name, value_str):
        try:
            value = int(value_str)
            if 0 <= value <= 100:
                self.places[place_name]["reputation"] = value
                self.save_data()
                self.refresh_display()
            else:
                messagebox.showerror("Error", "Reputation must be 0-100.")
        except ValueError:
            messagebox.showerror("Error", "Invalid number.")
    
    def modify_person_reputation(self, place_name, person_name, delta):
        current = self.places[place_name]["people"][person_name]
        new_value = max(0, min(100, current + delta))
        self.places[place_name]["people"][person_name] = new_value
        self.save_data()
        self.refresh_display()
    
    def set_person_reputation(self, place_name, person_name, value_str):
        try:
            value = int(value_str)
            if 0 <= value <= 100:
                self.places[place_name]["people"][person_name] = value
                self.save_data()
                self.refresh_display()
            else:
                messagebox.showerror("Error", "Reputation must be 0-100.")
        except ValueError:
            messagebox.showerror("Error", "Invalid number.")
    
    def toggle_visibility(self, place_name):
        self.place_visibility[place_name] = not self.place_visibility.get(place_name, True)
        self.refresh_display()

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ReputationTrackerGUI(root)
    root.mainloop()

import os
import json
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# Define the file path to save reputation data
FILE_PATH = r"C:\Users\saqom\OneDrive\Deskto\Folders\vscode folder\reputation\reputation.json"

class ReputationTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("D&D Reputation Tracker")
        self.root.geometry("600x600")
        
        # Dictionary to store toggle visibility for places; False means people are visible.
        self.place_visibility = {}
        
        # Set up ttk style for a modern look
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), foreground="#333")
        self.style.configure("TButton", font=("Helvetica", 10))
        # Configure a small, red delete button style
        self.style.configure("Delete.TButton", foreground="red", font=("Helvetica", 7, "bold"), padding=0)
        
        # Main container frame
        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_label = ttk.Label(main_frame, text="D&D Reputation Tracker", style="Header.TLabel")
        header_label.pack(pady=10)
        
        # Top frame for adding new places
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)
        add_place_btn = ttk.Button(top_frame, text="Add Place", command=self.add_place)
        add_place_btn.pack(side=tk.LEFT)
        
        # Canvas for scrollable display of places/people
        self.canvas = tk.Canvas(main_frame, background="#f0f0f0")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.display_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.display_frame, anchor="nw")
        self.display_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Load saved data or initialize new data
        self.places = self.load_data()
        self.refresh_display()
        
    def load_data(self):
        """Load reputation data from file, or return an empty dict if not available."""
        if os.path.exists(FILE_PATH):
            try:
                with open(FILE_PATH, "r") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")
        return {}
    
    def save_data(self):
        """Save reputation data to file."""
        try:
            directory = os.path.dirname(FILE_PATH)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(FILE_PATH, "w") as f:
                json.dump(self.places, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    
    def toggle_visibility(self, place):
        """Toggle the visibility of people for a given place."""
        current = self.place_visibility.get(place, False)
        self.place_visibility[place] = not current
        self.refresh_display()
    
    def refresh_display(self):
        """Clear and rebuild the display of places and people."""
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        if not self.places:
            ttk.Label(self.display_frame, text="No places added yet.").pack(pady=10)
            return
        
        for place in self.places:
            place_frame = ttk.Frame(self.display_frame, relief="ridge", borderwidth=2, padding=10)
            place_frame.pack(fill=tk.X, padx=5, pady=5)
            
            header_frame = ttk.Frame(place_frame)
            header_frame.pack(fill=tk.X)
            
            # Place name label
            name_label = ttk.Label(header_frame, text=place, style="Header.TLabel")
            name_label.grid(row=0, column=0, sticky="w")
            
            # Reputation controls for the place
            minus5_btn = ttk.Button(header_frame, text="-5", width=4,
                                     command=lambda p=place: self.modify_place_reputation(p, -5))
            minus5_btn.grid(row=0, column=1, padx=2)
            
            minus1_btn = ttk.Button(header_frame, text="-1", width=4,
                                     command=lambda p=place: self.modify_place_reputation(p, -1))
            minus1_btn.grid(row=0, column=2, padx=2)
            
            rep_entry = ttk.Entry(header_frame, width=5, justify="center", font=("Helvetica", 14))
            rep_entry.insert(0, str(self.places[place]["reputation"]))
            rep_entry.grid(row=0, column=3, padx=2)
            rep_entry.bind("<Return>", lambda e, p=place, entry=rep_entry: self.set_place_reputation(p, entry.get()))
            
            plus1_btn = ttk.Button(header_frame, text="+1", width=4,
                                    command=lambda p=place: self.modify_place_reputation(p, 1))
            plus1_btn.grid(row=0, column=4, padx=2)
            
            plus5_btn = ttk.Button(header_frame, text="+5", width=4,
                                   command=lambda p=place: self.modify_place_reputation(p, 5))
            plus5_btn.grid(row=0, column=5, padx=2)
            
            add_person_btn = ttk.Button(header_frame, text="Add Person",
                                        command=lambda p=place: self.add_person(p))
            add_person_btn.grid(row=0, column=6, padx=10)
            
            # Toggle visibility button for hiding/showing people in the place
            toggle_text = "Hide Names" if not self.place_visibility.get(place, False) else "Show Names"
            toggle_btn = ttk.Button(header_frame, text=toggle_text,
                                    command=lambda p=place: self.toggle_visibility(p))
            toggle_btn.grid(row=0, column=7, padx=2)
            
            # Delete Place button, placed at the top-right corner of the place_frame
            delete_place_btn = ttk.Button(place_frame, text="X", style="Delete.TButton", width=1,
                                          command=lambda p=place: self.delete_place(p))
            delete_place_btn.place(relx=1, rely=0, anchor="ne", x=-1, y=1)
            
            # Only display people if not toggled to hide
            if not self.place_visibility.get(place, False):
                people_frame = ttk.Frame(place_frame, padding="5 5 5 5")
                people_frame.pack(fill=tk.X, padx=20, pady=5)
                
                if not self.places[place]["people"]:
                    ttk.Label(people_frame, text="No people added yet.").pack(anchor="w")
                else:
                    for person, rep in self.places[place]["people"].items():
                        person_frame = ttk.Frame(people_frame)
                        person_frame.pack(fill=tk.X, pady=2)
                        
                        # Delete Person button using pack so it is visible
                        delete_person_btn = ttk.Button(person_frame, text="X", style="Delete.TButton", width=1,
                                                       command=lambda p=place, pe=person: self.delete_person(p, pe))
                        delete_person_btn.pack(side=tk.RIGHT, anchor="ne", padx=2)
                        
                        person_details_frame = ttk.Frame(person_frame)
                        person_details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                        
                        person_label = ttk.Label(person_details_frame, text=person)
                        person_label.grid(row=0, column=0, sticky="w")
                        
                        minus5_person = ttk.Button(person_details_frame, text="-5", width=4,
                                                   command=lambda p=place, pe=person: self.modify_person_reputation(p, pe, -5))
                        minus5_person.grid(row=0, column=1, padx=2)
                        
                        minus1_person = ttk.Button(person_details_frame, text="-1", width=4,
                                                   command=lambda p=place, pe=person: self.modify_person_reputation(p, pe, -1))
                        minus1_person.grid(row=0, column=2, padx=2)
                        
                        rep_entry_person = ttk.Entry(person_details_frame, width=5, justify="center", font=("Helvetica", 14))
                        rep_entry_person.insert(0, str(rep))
                        rep_entry_person.grid(row=0, column=3, padx=2)
                        rep_entry_person.bind("<Return>", lambda e, p=place, pe=person, entry=rep_entry_person: self.set_person_reputation(p, pe, entry.get()))
                        
                        plus1_person = ttk.Button(person_details_frame, text="+1", width=4,
                                                  command=lambda p=place, pe=person: self.modify_person_reputation(p, pe, 1))
                        plus1_person.grid(row=0, column=4, padx=2)
                        
                        plus5_person = ttk.Button(person_details_frame, text="+5", width=4,
                                                  command=lambda p=place, pe=person: self.modify_person_reputation(p, pe, 5))
                        plus5_person.grid(row=0, column=5, padx=2)
    
    def add_place(self):
        """Prompt user to add a new place."""
        place_name = simpledialog.askstring("Add Place", "Enter place name:")
        if place_name:
            if place_name in self.places:
                messagebox.showerror("Error", "Place already exists!")
            else:
                self.places[place_name] = {"reputation": 50, "people": {}}
                self.save_data()
                self.refresh_display()
    
    def add_person(self, place_name):
        """Prompt user to add a new person to a place."""
        person_name = simpledialog.askstring("Add Person", f"Enter person name for {place_name}:")
        if person_name:
            if person_name in self.places[place_name]["people"]:
                messagebox.showerror("Error", "Person already exists!")
            else:
                self.places[place_name]["people"][person_name] = 50
                self.save_data()
                self.refresh_display()
    
    def delete_place(self, place_name):
        """Delete a place from the tracker."""
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete place '{place_name}'?"):
            del self.places[place_name]
            self.save_data()
            self.refresh_display()
    
    def delete_person(self, place_name, person_name):
        """Delete a person from a place."""
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete '{person_name}' from '{place_name}'?"):
            del self.places[place_name]["people"][person_name]
            self.save_data()
            self.refresh_display()
    
    def modify_place_reputation(self, place_name, delta):
        """Modify a place's reputation by delta (±1 or ±5) within 0-100."""
        current = self.places[place_name]["reputation"]
        new_value = max(0, min(100, current + delta))
        self.places[place_name]["reputation"] = new_value
        self.save_data()
        self.refresh_display()
    
    def modify_person_reputation(self, place_name, person_name, delta):
        """Modify a person's reputation by delta (±1 or ±5) within 0-100."""
        current = self.places[place_name]["people"][person_name]
        new_value = max(0, min(100, current + delta))
        self.places[place_name]["people"][person_name] = new_value
        self.save_data()
        self.refresh_display()
    
    def set_place_reputation(self, place_name, value_str):
        """Set a place's reputation from a typed value."""
        try:
            value = int(value_str)
            if 0 <= value <= 100:
                self.places[place_name]["reputation"] = value
                self.save_data()
                self.refresh_display()
            else:
                messagebox.showerror("Error", "Reputation must be between 0 and 100.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")
    
    def set_person_reputation(self, place_name, person_name, value_str):
        """Set a person's reputation from a typed value."""
        try:
            value = int(value_str)
            if 0 <= value <= 100:
                self.places[place_name]["people"][person_name] = value
                self.save_data()
                self.refresh_display()
            else:
                messagebox.showerror("Error", "Reputation must be between 0 and 100.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReputationTrackerGUI(root)
    root.mainloop()

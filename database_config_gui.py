"""
GUI untuk konfigurasi database dinamis
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from pathlib import Path
import pymysql
import threading
import json
from datetime import datetime


class DatabaseConfigGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Brilink Backend - Database Configuration")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
        # Load saved config if exists
        self.config_file = Path("db_config.json")
        self.load_saved_config()
        
        # Setup UI
        self.setup_ui()
        
        # Center window
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def load_saved_config(self):
        """Load saved configuration from file"""
        self.saved_config = {}
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.saved_config = json.load(f)
            except:
                pass
                
    def save_config(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
            
    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg="#003366", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🏦 Brilink Backend API",
            font=("Arial", 20, "bold"),
            bg="#003366",
            fg="white"
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Database Configuration",
            font=("Arial", 10),
            bg="#003366",
            fg="#cccccc"
        )
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Database Configuration Section
        config_label = tk.Label(
            main_frame,
            text="Database Configuration",
            font=("Arial", 12, "bold")
        )
        config_label.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky='w')
        
        # Database Host
        tk.Label(main_frame, text="Host:", font=("Arial", 10)).grid(
            row=1, column=0, sticky='w', pady=5
        )
        self.host_var = tk.StringVar(value=self.saved_config.get('DB_HOST', 'localhost'))
        self.host_entry = ttk.Entry(main_frame, textvariable=self.host_var, width=40)
        self.host_entry.grid(row=1, column=1, pady=5, sticky='ew')
        
        # Database Port
        tk.Label(main_frame, text="Port:", font=("Arial", 10)).grid(
            row=2, column=0, sticky='w', pady=5
        )
        self.port_var = tk.StringVar(value=self.saved_config.get('DB_PORT', '3306'))
        self.port_entry = ttk.Entry(main_frame, textvariable=self.port_var, width=40)
        self.port_entry.grid(row=2, column=1, pady=5, sticky='ew')
        
        # Database Name
        tk.Label(main_frame, text="Database Name:", font=("Arial", 10)).grid(
            row=3, column=0, sticky='w', pady=5
        )
        self.dbname_var = tk.StringVar(value=self.saved_config.get('DB_NAME', 'db_api_brilink'))
        self.dbname_entry = ttk.Entry(main_frame, textvariable=self.dbname_var, width=40)
        self.dbname_entry.grid(row=3, column=1, pady=5, sticky='ew')
        
        # Database User
        tk.Label(main_frame, text="Username:", font=("Arial", 10)).grid(
            row=4, column=0, sticky='w', pady=5
        )
        self.user_var = tk.StringVar(value=self.saved_config.get('DB_USER', 'root'))
        self.user_entry = ttk.Entry(main_frame, textvariable=self.user_var, width=40)
        self.user_entry.grid(row=4, column=1, pady=5, sticky='ew')
        
        # Database Password
        tk.Label(main_frame, text="Password:", font=("Arial", 10)).grid(
            row=5, column=0, sticky='w', pady=5
        )
        self.password_var = tk.StringVar(value=self.saved_config.get('DB_PASSWORD', ''))
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, width=40, show="*")
        self.password_entry.grid(row=5, column=1, pady=5, sticky='ew')
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_cb = tk.Checkbutton(
            main_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password
        )
        show_password_cb.grid(row=6, column=1, sticky='w', pady=5)
        
        # Secret Key
        tk.Label(main_frame, text="Secret Key:", font=("Arial", 10)).grid(
            row=7, column=0, sticky='w', pady=5
        )
        self.secret_var = tk.StringVar(value=self.saved_config.get('SECRET_KEY', 'your-secret-key-here'))
        self.secret_entry = ttk.Entry(main_frame, textvariable=self.secret_var, width=40)
        self.secret_entry.grid(row=7, column=1, pady=5, sticky='ew')
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        # Test Connection Button
        self.test_btn = tk.Button(
            buttons_frame,
            text="🔌 Test Connection",
            command=self.test_connection,
            bg="#FFA500",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        # Save & Start Button
        self.start_btn = tk.Button(
            buttons_frame,
            text="✅ Save & Start Server",
            command=self.save_and_start,
            bg="#28a745",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # Exit Button
        exit_btn = tk.Button(
            buttons_frame,
            text="❌ Exit",
            command=self.exit_app,
            bg="#dc3545",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        exit_btn.pack(side=tk.LEFT, padx=5)
        
        # Log/Status area
        log_label = tk.Label(
            main_frame,
            text="Status Log:",
            font=("Arial", 10, "bold")
        )
        log_label.grid(row=9, column=0, columnspan=2, pady=(10, 5), sticky='w')
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            width=70,
            font=("Courier", 9),
            bg="#f8f9fa",
            state=tk.DISABLED
        )
        self.log_text.grid(row=10, column=0, columnspan=2, pady=5, sticky='ew')
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        self.log_message("Ready. Please configure database connection and test it.")
        
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
            
    def log_message(self, message, level="INFO"):
        """Add message to log area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_map = {
            "INFO": "#0066cc",
            "SUCCESS": "#28a745",
            "ERROR": "#dc3545",
            "WARNING": "#FFA500"
        }
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] [{level}] ", f"tag_{level}")
        self.log_text.tag_config(f"tag_{level}", foreground=color_map.get(level, "black"))
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
        
    def test_connection(self):
        """Test database connection"""
        self.log_message("Testing database connection...")
        self.test_btn.config(state=tk.DISABLED, text="Testing...")
        
        # Run test in thread to avoid freezing UI
        thread = threading.Thread(target=self._test_connection_thread)
        thread.daemon = True
        thread.start()
        
    def _test_connection_thread(self):
        """Thread worker for testing connection"""
        try:
            host = self.host_var.get().strip()
            port = int(self.port_var.get().strip())
            user = self.user_var.get().strip()
            password = self.password_var.get()
            dbname = self.dbname_var.get().strip()
            
            if not all([host, port, user, dbname]):
                self.log_message("Please fill all required fields", "ERROR")
                self.test_btn.config(state=tk.NORMAL, text="🔌 Test Connection")
                return
            
            self.log_message(f"Connecting to {host}:{port}...")
            
            # Try to connect
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                connect_timeout=5
            )
            
            self.log_message("✓ Connected to MySQL server", "SUCCESS")
            
            # Check if database exists
            cursor = connection.cursor()
            cursor.execute(f"SHOW DATABASES LIKE '{dbname}'")
            db_exists = cursor.fetchone()
            
            if db_exists:
                self.log_message(f"✓ Database '{dbname}' found", "SUCCESS")
            else:
                self.log_message(f"⚠ Database '{dbname}' not found. It will be created.", "WARNING")
            
            cursor.close()
            connection.close()
            
            self.log_message("✓ Connection test successful!", "SUCCESS")
            self.start_btn.config(state=tk.NORMAL)
            
        except pymysql.err.OperationalError as e:
            error_msg = str(e)
            if "Access denied" in error_msg:
                self.log_message("✗ Access denied. Check username/password", "ERROR")
            elif "Can't connect" in error_msg or "Unknown MySQL server" in error_msg:
                self.log_message(f"✗ Cannot connect to {host}:{port}", "ERROR")
            else:
                self.log_message(f"✗ Connection error: {error_msg}", "ERROR")
                
        except ValueError:
            self.log_message("✗ Invalid port number", "ERROR")
            
        except Exception as e:
            self.log_message(f"✗ Unexpected error: {str(e)}", "ERROR")
            
        finally:
            self.test_btn.config(state=tk.NORMAL, text="🔌 Test Connection")
            
    def save_and_start(self):
        """Save configuration and start server"""
        try:
            config = {
                'DB_HOST': self.host_var.get().strip(),
                'DB_PORT': self.port_var.get().strip(),
                'DB_USER': self.user_var.get().strip(),
                'DB_PASSWORD': self.password_var.get(),
                'DB_NAME': self.dbname_var.get().strip(),
                'SECRET_KEY': self.secret_var.get().strip()
            }
            
            # Create .env file
            env_content = f"""# Database Configuration
DB_HOST={config['DB_HOST']}
DB_PORT={config['DB_PORT']}
DB_NAME={config['DB_NAME']}
DB_USER={config['DB_USER']}
DB_PASSWORD={config['DB_PASSWORD']}

# Application Configuration
SECRET_KEY={config['SECRET_KEY']}
FLASK_ENV=production
"""
            
            with open('.env', 'w') as f:
                f.write(env_content)
                
            # Save config to JSON (without password for next time)
            save_config = config.copy()
            save_config['DB_PASSWORD'] = ''  # Don't save password
            self.save_config(save_config)
            
            self.log_message("✓ Configuration saved to .env file", "SUCCESS")
            self.log_message("Starting server...", "INFO")
            
            # Set flag to start server
            self.should_start_server = True
            self.root.quit()
            
        except Exception as e:
            self.log_message(f"✗ Error saving configuration: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
            
    def exit_app(self):
        """Exit application"""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.should_start_server = False
            self.root.quit()
            
    def run(self):
        """Run the GUI"""
        self.should_start_server = False
        self.root.mainloop()
        return self.should_start_server


def main():
    """Main entry point"""
    gui = DatabaseConfigGUI()
    return gui.run()


if __name__ == "__main__":
    should_start = main()
    if should_start:
        print("Configuration completed. Starting server...")
    else:
        print("Configuration cancelled.")

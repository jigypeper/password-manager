from tkinter import *
from tkinter import messagebox
import random
import json
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list.extend([random.choice(letters) for _ in range(nr_letters)])
    password_list.extend([random.choice(symbols) for _ in range(nr_symbols)])
    password_list.extend([random.choice(numbers) for _ in range(nr_numbers)])

    random.shuffle(password_list)

    password = "".join(password_list)

    pass_entry.delete(0, END)
    pass_entry.insert(0, password)
    # pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():

    web = web_entry.get()
    user = user_entry.get()
    password = pass_entry.get()
    new_data = {
        web: {
            "user": user,
            "password": password,
        }
    }

    if len(web) == 0 or len(password) == 0 or len( user) == 0:
        messagebox.showinfo(title="Oops", message="Don't leave any fields empty!")
        is_ok = False
    else:
        try:
            with open("data.json", 'r') as data:
                # reading old data
                old_data = json.load(data)
        except FileNotFoundError:
            with open("data.json", 'w') as data:
                json.dump(new_data, data, indent=4)
        else:
            # updating old data
            old_data.update(new_data)

            with open("data.json", "w") as data:
                # saving updated data
                json.dump(old_data, data, indent=4)
        finally:
            web_entry.delete(0, END)
            pass_entry.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------ #


def search_pass():

    web = web_entry.get()
    pass_data = {}
    try:
        with open("data.json", 'r') as data:
            pass_data = json.load(data)
            password_searched = pass_data[web]["password"]
            user_searched = pass_data[web]["user"]
            messagebox.showinfo(title=web, message=f"Username: {user_searched}\nPassword: {password_searched}")
    except FileNotFoundError as file_error:
        messagebox.showinfo(title="Error", message=f"{file_error}")
    except KeyError as key_error:
        messagebox.showinfo(title="Error", message=f"password for {key_error} does not exist")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

label_website = Label(text="Website:")
label_website.grid(column=0, row=1)

web_entry = Entry(width=30)
web_entry.grid(column=1, row=1, columnspan=1)
web_entry.focus()

label_user_email = Label(text="Email/Username:")
label_user_email.grid(column=0, row=2)

user_entry = Entry(width=21)
user_entry.grid(column=1, row=2, columnspan=1)
user_entry.insert(END, "email@mac.com")

label_password = Label(text="Password:")
label_password.grid(column=0, row=3)

pass_entry = Entry(width=21)
pass_entry.grid(column=1, row=3)

gen_pass_button = Button(text="Generate Password", command=generate_password)
gen_pass_button.grid(column=2, row=3)

add_details_button = Button(text="Add", width=36, command=save_data)
add_details_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=search_pass, width=13)
search_button.grid(column=2, row=1)

window.mainloop()

import json
import random
from tkinter import *
from tkinter import messagebox
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
               "v",
               "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q",
               "R",
               "S", "T", "U", "V", "W", "X", "Y", "Z"]

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+']

    n_letters = random.randint(8, 10)
    n_numbers = random.randint(2, 4)
    n_symbols = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(0, n_letters - 1)]
    password_numbers = [random.choice(numbers) for _ in range(0, n_numbers - 1)]
    password_symbols = [random.choice(symbols) for _ in range(0, n_symbols - 1)]

    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)

    generated_password = "".join(password_list)

    password.insert(0, generated_password)
    pyperclip.copy(generated_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    web_value = website.get()
    email_value = email.get()
    password_value = password.get()
    new_data = {web_value:{
        "email": email_value,
        "password": password_value
    }
    }

    if len(web_value) == 0 or len(password_value) == 0 or len(email_value) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any of the fields empty")
    else:
        is_ok = messagebox.askokcancel(title=web_value, message=f"These are the details entered, \n"
                                                                f"Email: {email_value},\n"
                                                                f"Password: {password_value},\n"
                                                                f"Is it okay to Save?")
        if is_ok:
            try:
                with open("data.json", "r") as data:
                    data_file = json.load(data)
                    data_file.update(new_data)
            except FileNotFoundError:
                with open("data.json", "w") as data:
                    json.dump(new_data, data, indent=4)
            else:
                with open("data.json", "w") as data:
                    json.dump(data_file, data, indent=4)
            finally:
                website.delete(0, END)
                email.delete(0, END)
                password.delete(0, END)

# -----------------------------Search website--------------------------#


def find_website():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="Sorry, Data does not exist")
    else:
        if website.get() in data:
            search_email = (data[website.get()]["email"])
            search_password = (data[website.get()]["password"])
            messagebox.showinfo(title=website.get(), message=f"Email: {search_email} \n Password: {search_password}")
        else:
            messagebox.showinfo(title="Oops", message=f"{website.get()} is not found in the data. please add a new one")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
icon = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=icon)
canvas.grid(column=1, row=0)

# website

website_name = Label(text="Website: ")
website_name.grid(column=0, row=1)

website = Entry(width=21)
website.grid(column=1, row=1)
website.focus()

search_button = Button(text="Search", width=15, command=find_website)
search_button.grid(column=2, row=1)


# email

email_name = Label(text="Email/Username: ")
email_name.grid(column=0, row=2)

email = Entry(width=40)
email.grid(column=1, row=2, columnspan=2)

# password

pass_txt = Label(text="Password: ")
pass_txt.grid(column=0, row=3)

password = Entry(width=21)
password.grid(column=1, row=3)

generate_button = Button(text="Generate", width=15, command=generate_password)
generate_button.grid(column=2, row=3)

# add

add_button = Button(text="Add", width=35, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()

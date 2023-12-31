from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


def generate_password():
    """generating a new password when the user clicked on the generate button"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for char in range(nr_symbols)]
    password_list += [random.choice(numbers) for char in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)


def save_to_file():
    """saving the data in a txt file when the user click the "Add" button """

    new_data = {website_input.get():
        {
            "email": email_input.get(),
            "password": password_input.get()
        }}
    if len(website_input.get()) == 0 or len(password_input.get()) == 0 or len(email_input.get()) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you entered all the fields")
    else:
        is_ok = messagebox.askokcancel(title=website_input.get(),
                                       message=f"These are the details entered:\n Email: {email_input.get()}\n Password: {password_input.get()}\n is is ok to save? ")
        if is_ok:

            try:
                with open("passwords_saver.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("passwords_saver.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)

                with open("passwords_saver.json", "w") as file:
                    json.dump(data, file, indent=4)

            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


def find_password():
    website = website_input.get()
    try:
        with open("passwords_saver.json", "r") as passwords_file:
            data = json.load(passwords_file)
            try:
                password = data[website]["password"]
                email = data[website]["email"]
                messagebox.showinfo(title=website, message=f"Email: {email} \n Password: {password}")
            except KeyError:
                messagebox.showerror(title="Invalid website name",
                                     message="Sorry..\n We did not find details for this website")
    except FileNotFoundError:
        messagebox.showerror(title="No data base", message="Your passwords saver is empty...")


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# canvas setting
canvas = Canvas(width=200, height=200)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

# website label
website_label = Label(text="Website")
website_label.grid(row=1, column=0)

# website input
website_input = Entry(width=21)
website_input.focus()
website_input.grid(row=1, column=1)

# search button
search_button = Button(text="Search", fg="red")
search_button.config(command=find_password)
search_button.grid(row=1, column=2, columnspan=2)

# email label
email_label = Label(text="Email/Username")
email_label.grid(row=2, column=0)

# email input
email_input = Entry(width=21)
email_input.insert(0, "eliyahron13@gmail.com")
email_input.grid(row=2, column=1)

# password label
password_label = Label(text="Password")
password_label.grid(row=3, column=0)

# password input
password_input = Entry(width=21)
password_input.grid(row=3, column=1)

# generate button
generate_button = Button(text="Generate password", fg="red", command=generate_password)
generate_button.grid(row=3, column=2)

# add button
add_button = Button(text="Add", width=33, fg="red")
add_button.config(command=save_to_file)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()

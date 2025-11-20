import streamlit as st
from pathlib import Path
import json
import random
import string

# --------------------------
# Bank Class
# --------------------------

class Bank:
    database = 'database.json'
    data = []

    # Load database
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            with open(database, "w") as fs:
                fs.write("[]")
    except Exception as err:
        st.error(f"Error loading database: {err}")

    @classmethod
    def update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @staticmethod
    def account_no():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        acc = alpha + digits
        random.shuffle(acc)
        return "".join(acc)

    # Basic operations
    def create_account(self, name, email, phone, pin):
        d = {
            "name": name,
            "email": email,
            "phone": phone,
            "pin": pin,
            "Account no.": Bank.account_no(),
            "Balance": 0
        }
        Bank.data.append(d)
        Bank.update()
        return d["Account no."]

    def authenticate(self, acc, pin):
        user = [i for i in Bank.data if i["Account no."] == acc and i["pin"] == pin]
        return user[0] if user else None

bank = Bank()


# --------------------------
# Streamlit UI
# --------------------------

st.title("🏦 Simple Bank Management System (Streamlit UI)")

menu = st.sidebar.selectbox(
    "Select Action",
    ["Create Account", "Deposit Money", "Withdraw Money",
     "View Account Details", "Update Details", "Delete Account"]
)


# --------------------------
# Create Account
# --------------------------
if menu == "Create Account":
    st.header("Create New Account")

    name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    phone = st.text_input("Enter Phone Number")
    pin = st.text_input("Set 4-digit PIN", type="password")

    if st.button("Create"):
        if len(phone) != 10 or not phone.isdigit():
            st.warning("Phone number must be 10 digits!")
        elif len(pin) != 4 or not pin.isdigit():
            st.warning("PIN must be 4 digits!")
        else:
            acc_no = bank.create_account(name, email, phone, int(pin))
            st.success(f"Account Created Successfully! Your Account No: {acc_no}")


# --------------------------
# Deposit Money
# --------------------------
if menu == "Deposit Money":
    st.header("Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    user = None
    if acc and pin and pin.isdigit():
        user = bank.authenticate(acc, int(pin))

    if user:
        amount = st.number_input("Enter Deposit Amount", min_value=1)
        if st.button("Deposit"):
            if amount > 10000:
                st.error("Amount cannot exceed 10,000")
            else:
                user["Balance"] += amount
                bank.update()
                st.success("Amount Deposited Successfully!")
    elif acc or pin:
        st.warning("Invalid account or PIN!")


# --------------------------
# Withdraw Money
# --------------------------
if menu == "Withdraw Money":
    st.header("Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    user = None
    if acc and pin and pin.isdigit():
        user = bank.authenticate(acc, int(pin))

    if user:
        amount = st.number_input("Enter Withdrawal Amount", min_value=1)
        if st.button("Withdraw"):
            if amount > user["Balance"]:
                st.error("Insufficient Balance!")
            elif amount > 10000:
                st.error("Amount cannot exceed 10,000")
            else:
                user["Balance"] -= amount
                bank.update()
                st.success("Amount Withdrawn Successfully!")
    elif acc or pin:
        st.warning("Invalid account or PIN!")


# --------------------------
# View Account Details
# --------------------------
if menu == "View Account Details":
    st.header("Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if acc and pin.isdigit():
        user = bank.authenticate(acc, int(pin))
        if user:
            st.json(user)
        else:
            st.error("Invalid Credentials")


# --------------------------
# Update Details
# --------------------------
if menu == "Update Details":
    st.header("Update Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    user = None
    if acc and pin and pin.isdigit():
        user = bank.authenticate(acc, int(pin))

    if user:
        st.info("Leave field empty if you don't want to update")
        name = st.text_input("New Name", user["name"])
        email = st.text_input("New Email", user["email"])
        phone = st.text_input("New Phone", user["phone"])
        new_pin = st.text_input("New PIN", type="password")

        if st.button("Update"):
            if phone and (not phone.isdigit() or len(phone) != 10):
                st.error("Phone must be 10 digits")
            else:
                user["name"] = name
                user["email"] = email
                user["phone"] = phone
                if new_pin:
                    user["pin"] = int(new_pin)

                bank.update()
                st.success("Details updated successfully!")
    elif acc or pin:
        st.warning("Invalid account or PIN!")


# --------------------------
# Delete Account
# --------------------------
if menu == "Delete Account":
    st.header("Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    user = None
    if acc and pin.isdigit():
        user = bank.authenticate(acc, int(pin))

    if user:
        if st.button("Delete Account"):
            Bank.data.remove(user)
            bank.update()
            st.success("Account Deleted Successfully!")
    elif acc or pin:
        st.warning("Invalid account or PIN!")

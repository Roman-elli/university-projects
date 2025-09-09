# 🚗 ManuWash – Reservation System

I made this project during my first year at university. it was developed in **C** and implements a **car wash and maintenance reservation system**. It allows you to **create, list, cancel, execute, save, and load reservations** in a simple and practical way.  

---

## 🚀 Features
- 📅 **Date and time validation** (leap years, valid days, etc.).  
- 🛠️ Two types of services:
  - Car Wash (**30 minutes**)  
  - Maintenance (**1 hour**)  
- 📝 Reservations and **pre-reservations** (waiting list).  
- ⏳ Automatic update of the waiting list.  
- 💾 **Save and load** reservations from files (`pre_reservation_list.txt` and `reservation_list.txt`).  
- ❌ Cancel reservations and pre-reservations.  
- ▶️ Execute the most recent task.  
- 🔍 Display options:
  - All reservations sorted in **ascending order**.  
  - Reservations of a specific client sorted in **descending order**.  

---

## 🕹️ Main Menu
When running the program, you will see the following options:

1. Create a reservation (wash or maintenance)  
2. Cancel a reservation or pre-reservation  
3. List all reservations (ascending order)  
4. List reservations of a client (descending order)  
5. Execute tasks or update current date  
6. Update the waiting list  
7. Load saved reservations  
8. Save reservations  
9. Exit program  

---

## ▶️ How to Run
1. Build the program using the provided Makefile:
    ```bash
    make
    ```

2. Run the program:
    ```bash
    make run
    ```

3. (optional) Clean all build files:
    ```bash
    make clean
    ```

4. Save files will be stored in the data/ folder:
    pre_reservation_list.txt → Reservations
    reservation_list.txt → Pre-reservations

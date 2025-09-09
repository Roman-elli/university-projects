# 📡 5G Auth Platform – Multi-Process Data Management System

This project was developed during a university course on **process synchronization**. It simulates a 5G data usage management system, where multiple mobile users request data services, and the platform handles authorization, monitoring, and logging using **semaphores, mutexes, message queues, pipes, and shared memory**.

---

## 🚀 Features

- 🖥 **Multi-Process Architecture:**  
  System Manager, Authorization Request Manager, Monitor Engine, Mobile Users, and BackOffice User.

- 🔄 **Synchronization Mechanisms:**  
  Uses semaphores, mutexes, and condition variables to synchronize access to shared resources.

- 📡 **Inter-Process Communication (IPC):**  
  Communicates through message queues, unnamed pipes, and named pipes for coordinating requests.

- 📝 **Mobile User Simulation:**  
  Mobile users send requests for VIDEO, MUSIC, or SOCIAL services with configurable data amounts.

- 🛠 **BackOffice Controls:**  
  - data statistics retrieval: `1#data_stats`
  - system reset via BackOffice user: `1#reset`
  

- 📊 **Real-Time Monitoring:**  
  Tracks data usage for each user and triggers alerts at 80%, 90%, and 100% thresholds.

- 💾 **Persistent Logging:**  
  All significant system events are logged into `data/log/log.txt`.

- ⚙️ **Dynamic Authorization Management:**  
  Extra Authorization Engines are dynamically created when queues are full, then removed when demand decreases.

---

## 🛠️ BackOffice Commands

- While running, the BackOffice User accepts the following commands:

- **Command**	 **Description**
    - **stats**  → Displays current statistics for all mobile users, including service usage, total data consumed, and alerts triggered.
    - **reset**  → Resets the system, clearing all data usage counters and log files. All mobile user sessions are restarted.
    - **help**   → Shows a list of available commands and their descriptions.
    - **exit**   → Exits the BackOffice User interface without affecting running mobile users or the 5G platform.

⚠️ Note: Commands must be typed in the BackOffice console after launching make run_back.

---

## 🛠️ How it Works

1. System Manager
- Initializes shared memory, semaphores, message queues, and starts all core processes.

2. Authorization Engines
- Handle requests from mobile users. Each request is processed in a synchronized way using semaphores and mutexes.

3. Monitor Engine
- Observes the usage of each mobile user and sends alerts when usage thresholds are reached.

4. Mobile Users
- Send requests for different services at configurable intervals. Requests are logged and processed in order.

5. BackOffice User
- Can request overall system statistics, reset the system, or exit. Commands are typed interactively.

6. Logging and Reporting
- All events, such as request processing, queue management, and alerts, are written to the log file.

⚡ Technologies Used

- C Language → Multi-threaded and multi-process programming 
- POSIX Semaphores & Mutexes → Synchronization primitives
- Message Queues & Pipes → IPC mechanisms
- Shared Memory → Shared data between processes
- Makefile → Build automation

---

## 🕹️ How to Run

1. **Build the project:**
    ```bash
    make all
    ```

2. **Run the 5G Authorization Platform:**
    ```bash
    make run_5g
    ```
3. **Run a Mobile User simulation:**
    ```bash
    make run_mobile
    ```

4. **Run the BackOffice User:**
    ```bash
    make run_back
    ```
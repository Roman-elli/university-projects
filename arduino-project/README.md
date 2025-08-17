# 🎮 Bit Math Game  

I made this game in my first year of the university and the goal of the game is to **practice binary logic operations** (AND, OR, XOR) in an interactive way using **Arduino, LEDs, and a button**.  

---

## 📌 Game Description  
- Two random numbers are generated and displayed in **binary format** using LEDs.  
- A binary operation (AND, OR, XOR) is randomly selected.  
- The **RGB LED color** indicates which operation to perform:  
  - 🔴 **Red** → AND  
  - 🔵 **Blue** → OR  
  - 🟢 **Green** → XOR  
- The player must press the button the number of times equal to the **operation’s result**.  
- The player has **7 seconds** to answer.  
- If the answer is wrong or time runs out, the game ends in **defeat**.  

---

## ⚡ Implemented Features  
✅ **Guess Button**:  
- Starts the game after the `"Press button to start!"` message.  
- Each click adds +1 to the player’s answer.  
- Long press (>1s) triggers a **game reset**.  

✅ **Random Numbers**:  
- Two random numbers are generated (1–15).  
- Displayed in **binary** using dedicated LEDs.  

✅ **Binary Operations**:  
- AND, OR, or XOR are chosen randomly.  
- Operation indicated by the **RGB LED**.  

✅ **Game Modes**:  
- **Victory** 🏆: LEDs blink and perform a sweep effect before restart.  
- **Defeat** ❌: Number LEDs turn off and only the RGB blinks before restart.  
- **Reset** 🔄: New numbers and a new operation are generated, with LEDs blinking and sweeping.  

✅ **Time Feedback**:  
- A message is displayed when **50%** and **75%** of the time has passed.  

---

## 🛠️ Circuit Setup  
- **Number 2 (LEDs):** Pins **10–13**  
- **Number 1 (LEDs):** Pins **6–9**  
- **Button:** Pin **2 (INPUT_PULLUP)**  
- **RGB LED:**  
  - 🔴 Red → Pin **5**  
  - 🔵 Blue → Pin **4**  
  - 🟢 Green → Pin **3**  

---

## 🎥 Demonstration  
An example gameplay video:  
👉 [YouTube Demo](https://youtu.be/llbvhd7cUFQ)  

---

## 📂 Project Deliverables  
- `bit_math.ino` → Complete Arduino code.  
- `circuit.jpeg` → Circuit diagram (Tinkercad).  
- `report.pdf` → Brief project report.  

---

## 📚 Key Learnings  
This project was a great opportunity to:  
- Work with **binary logic and number systems**.  
- Explore **button debounce handling**.  
- Control LEDs and an RGB LED with **Arduino**.  
- Implement **timers and real-time feedback**.  
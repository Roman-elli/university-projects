# 🚀 LunarLander Controller – Rule-Based Agent for Gymnasium LunarLander-v3  

This project was developed as an experiment in **reinforcement learning environments** in my artificial intelligence class. Instead of training a neural network, it implements a **rule-based controller** for the **LunarLander-v3** environment.  

The agent applies a set of **deterministic heuristics** to control the spacecraft, both in scenarios **with wind** and **without wind**, attempting to achieve stable landings.  

---

## ✨ Features  

- 🔹 **Environment Setup:**  
  Uses `gymnasium`’s `LunarLander-v3` in continuous mode with optional wind and turbulence.  

- 🔹 **Landing Success Check:**  
  Verifies stability based on velocity, orientation, and landing pad position.  

- 🔹 **Perception Functions:**  
  Provides abstractions to extract position, velocity, orientation, and landing gear contact from the raw environment observations.  

- 🔹 **Action Helpers:**  
  Functions to apply **main engine**, **left thruster**, or **right thruster** with **full** or **partial power**.  

- 🔹 **Rule-Based Policies:**  
  - `agent_no_wind` → Heuristic policy tuned for scenarios without wind.  
  - `agent_wind` → Heuristic policy tuned for wind and turbulence conditions.  

- 🔹 **Simulation Runner:**  
  Evaluates the agent over multiple episodes, measuring **success rate** and **average steps until landing**.  

---

## 📂 Project Report  

  - A detailed description of the **Spacecraft Production System** used by the agents is available in `project-report.md`.
  - **Production System Rules** The report contains all 17 rules mapping **perceptions** to **actions** for stable landings.  

---

## 🛠️ Project Workflow  

1. **Initialize Environment** → Configure gravity, wind, turbulence, and rendering options.  
2. **Simulate Episodes** → Run episodes using either `agent_no_wind` or `agent_wind`.  
3. **Agent Policy** → Select thrusters/actions based on current state variables.  
4. **Landing Evaluation** → Check if the lander achieves a stable landing.  
5. **Report Metrics** → Print success rate and average landing steps.  

---

## ⚡ Technologies Used  

- **Python 3** → Core implementation  
- **Gymnasium** → LunarLander-v3 environment  
- **NumPy** → Numerical operations  
- **Pygame** → Optional rendering (when `render_mode="human"`)  

---

## 🕹️ How to Run  

1. **Install dependencies:**  
   ```bash
   pip install gymnasium[box2d] numpy pygame
   ```

2. Run the simulation:
    ```bash
    python src/main.py
    ```
3. Modify configuration (inside config.py):

  - ENABLE_WIND = False → Run no-wind scenario
  - ENABLE_WIND = True → Run with wind + turbulence
  - EPISODES = 1000 → Change number of evaluation episodes

# 🧬 LunarLander Controller – Evolutionary Neural Network Agent  

This project was developed as part of my **Artificial Intelligence university coursework**.  
Instead of a rule-based controller, it uses an **evolutionary algorithm** to evolve neural networks that control the lander in the **LunarLander-v3** environment.  

The algorithm applies **genetic operators** (selection, crossover, mutation, survival) to search for policies that maximize stable landings under different conditions.  

---

## ✨ Features  

- 🔹 **Environment Setup:**  
  Uses `gymnasium`’s `LunarLander-v3` in continuous mode with configurable gravity, wind, and turbulence.  

- 🔹 **Custom Fitness Function:**  
  Combines multiple **reward signals** (approaching zone, centering, vertical alignment, stable landing) and **penalties** (extreme angle, drifting, velocity).  

- 🔹 **Evolutionary Algorithm:**  
  - **Initial Population** → Random genotypes (neural network weights).  
  - **Parent Selection** → Tournament-based.  
  - **Crossover & Mutation** → To generate diverse offspring.  
  - **Survival Selection** → Keeps elite and best-performing individuals.  

- 🔹 **Parallel Evaluation:**  
  Uses Python’s `multiprocessing` to evaluate individuals faster.  

- 🔹 **Logging & Replay:**  
  Saves best individuals of each generation and allows validation over multiple test episodes.  

---

## 🛠️ Project Workflow  

1. **Initialize Population** → Create random individuals (neural network weights).  
2. **Evaluate Fitness** → Run simulation in LunarLander-v3 environment.  
3. **Apply Evolutionary Operators** → Selection, crossover, mutation.  
4. **Survival Selection** → Keep best individuals across generations.  
5. **Track Bests** → Save top fitness and genotype to logs.  

---

## ⚡ Technologies Used  

- **Python 3** → Core implementation  
- **Gymnasium** → LunarLander-v3 environment  
- **NumPy** → Numerical operations  
- **Multiprocessing** → Parallel evaluation of individuals  

---

## 📂 Logs & Validation

- After training, the best individuals of each run are stored in `logX.txt`.

---

## 🕹️ How to Run  

1. **Install dependencies:**  
   ```bash
   pip install gymnasium[box2d] numpy
   ```

2. Configure training/evaluation in config.py:

    - POPULATION_SIZE → Number of individuals per generation
    - NUMBER_OF_GENERATIONS → Evolution length
    - PROB_CROSSOVER / PROB_MUTATION → Genetic operators
    - ENABLE_WIND = True/False → Wind and turbulence settings

3. Run the evolutionary training:
    ```bash
    python src/main.py
    ```
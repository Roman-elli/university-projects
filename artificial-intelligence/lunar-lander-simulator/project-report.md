# Spacecraft Production System

## Actions

- **GDP** – rotate the spacecraft to the right with partial left engine  
- **GDT** – rotate the spacecraft to the right with full left engine  
- **GEP** – rotate the spacecraft to the left with partial right engine  
- **GET** – rotate the spacecraft to the left with full right engine  
- **MT** – activate main engine only at full power  
- **MP** – activate main engine only at partial power  

---

## Perceptions

- **H** – Horizontal position relative to the center  
- **V** – Vertical position relative to the ground  
- **VH** – Horizontal velocity  
- **VV** – Vertical velocity  
- **O** – Spacecraft orientation  
- **VA** – Angular velocity  
- **PE** – touching the ground with the left leg  
- **PD** – touching the ground with the right leg  

---

## Thresholds

- **Θ** – Angle threshold = 0.005  
- **LAE** – External angle threshold = 0.053  
- **LV** – Vertical velocity threshold = -0.07  
- **LVH** – Horizontal velocity threshold = 0.005  
- **LHE** – External horizontal velocity threshold = 0.15  
- **LH** – Horizontal threshold = 0.023  

---

## Production System

1. **PE, PD → NIL**  

2. **If** VH > LHE, O < 1.8 × LAE, VV < LV → **GET, MP**  
   **Else if** VH > LHE, O < 1.8 × LAE → **GET**  

3. **If** VH > LHE, VV < LV → **GDT, MP**  
   **Else if** VH > LHE → **GDT**  

4. **If** VH < -LHE, O > -1.8 × LAE, VV < LV → **GDT, MP**  
   **Else if** VH < -LHE, O > -1.8 × LAE → **GDT**  

5. **If** VH < -LHE, VV < LV → **GET, MP**  
   **Else if** VH < -LHE → **GET**  

6. **If** H < -LH, O > -LAE, VV < LV → **GDT, MP**  
   **Else if** H < -LH, O > -LAE → **GDT**  

7. **If** H < -LH, VV < LV → **GET, MP**  
   **Else if** H < -LH → **GET**  

8. **If** H > LH, O < LAE, VV < LV → **GET, MP**  
   **Else if** H > LH, O < LAE → **GET**  

9. **If** H > LH, VV < LV → **GDT, MP**  
   **Else if** H > LH → **GDT**  

10. **If** VH > LVH, O < Θ, VV < LV → **GET, MP**  
    **Else if** VH > LVH, O < Θ → **GET**  

11. **If** VH > LVH, VV < LV → **GDT, MP**  
    **Else if** VH > LVH → **GDT**  

12. **If** VH < -LVH, O > -Θ, VV < LV → **GDT, MP**  
    **Else if** VH < -LVH, O > -Θ → **GDT**  

13. **If** VH < -LVH, VV < LV → **GET, MP**  
    **Else if** VH < -LVH → **GET**  

14. **If** O > 4 × Θ, VV < LV → **GDT, MP**  
    **Else if** O > 4 × Θ → **GDT**  

15. **If** O < -4 × Θ, VV < LV → **GET, MP**  
    **Else if** O < -4 × Θ → **GET**  

16. **If** O < -Θ, VV < LV → **GDP, MP**  
    **Else if** O < -Θ → **GDP**  

17. **If** O > Θ, VV < LV → **GEP, MP**  
    **Else if** O > Θ → **GEP**  

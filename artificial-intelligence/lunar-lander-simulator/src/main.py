import gymnasium as gym
import numpy as np
import pygame

ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = 'human'
RENDER_MODE = None # seleccione esta opção para não visualizar o ambiente (testes mais rápidos)
EPISODES = 1000

env = gym.make("LunarLander-v3", render_mode =RENDER_MODE, 
    continuous=True, gravity=GRAVITY, 
    enable_wind=ENABLE_WIND, wind_power=WIND_POWER, 
    turbulence_power=TURBULENCE_POWER)

def check_successful_landing(observation):
    x = observation[0]
    vy = observation[3]
    theta = observation[4]
    contact_left = observation[6]
    contact_right = observation[7]

    legs_touching = contact_left == 1 and contact_right == 1

    on_landing_pad = abs(x) <= 0.2

    stable_velocity = vy > -0.2
    stable_orientation = abs(theta) < np.deg2rad(20)
    stable = stable_velocity and stable_orientation
 
    if legs_touching and on_landing_pad and stable:
        print("✅ Aterragem bem sucedida!")
        return True

    print("⚠️ Aterragem falhada!")        
    return False
        
def simulate(steps=1000,seed=None, policy = None):    
    observ, _ = env.reset(seed=seed)
    for step in range(steps):
        action = policy(observ)

        observ, _, term, trunc, _ = env.step(action)

        if term or trunc:
            break

    success = check_successful_landing(observ)
    return step, success

# Perceptions
# Posiçao horizontal em relação ao centro
def posicao_horizontal(observation):
    return observation[0]

# Posiçao vertical em relação ao centro
def posicao_vertical(observation):
    return observation[1]

# Velocidade horizontal
def velocidade_horizontal(observation):
    return observation[2]

# Velocidade vertical
def velocidade_vertical(observation):
    return observation[3]

# Orientação da nave
def orientacao(observation):
    return observation[4]

# Velocidade Angular
def velocidade_angular(observation):
    return observation[5]

# Pé esquerdo
def toque_esquerdo(observation):
    if (observation[6] == 1): return True
    return False

# Pé direito
def toque_direito(observation):
    if (observation[7] == 1): return True
    return False

# Actions
# Gira a nave para a direita com o motor esquerdo
def gira_direita_total(action):
    action[1] = 0.8
    return action
def gira_direita_parcial(action):
    action[1] = 0.51
    return action

# Gira a nave para a esquerda com o motor direito
def gira_esquerda_total(action):
    action[1] = -0.8
    return action
def gira_esquerda_parcial(action):
    action[1] = -0.51
    return action

# Ativa motor principal
def principal_total(action):
    action[0] = 0.9
    return action
def principal_parcial(action):
    action[0] = 0.51
    return action

# Limiares definidos para o cenario SEM vento

LIMIAR_ANGULO = 0.005
LIMIAR_ANGULO_EXTERNO = 0.053
LIMIAR_VELOCIDADE_VERTICAL = -0.07
LIMIAR_VELOCIDADE_HORIZONTAL = 0.005
LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO = 0.15
LIMIAR_HORIZONTAL = 0.023

def agent_no_wind(observation):
    action = [0, 0]

    toque_esq = toque_esquerdo(observation)
    toque_dir = toque_direito(observation)
    vel_hor = velocidade_horizontal(observation)
    vel_ver = velocidade_vertical(observation)
    orient = orientacao(observation)
    pos_hor = posicao_horizontal(observation)

    # 1. CASO FINAL
    # PE, PD -> NIL
    if toque_esq and toque_dir:
        return action

    # 2. ACIMA DA VELOCIDADE HORIZONTAL EXTERNA PARA A DIREITA E GRAU CORRETO
    # VH > LHE, O < 1.8 * LAE, VV < LV -> GET, MP
    # VH > LHE, O < 1.8 * LAE -> GET
    elif vel_hor > LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO and orient < 1.8 * LIMIAR_ANGULO_EXTERNO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_esquerda_total(action)
        action = principal_parcial(action)
    elif vel_hor > LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO and orient < 1.8 * LIMIAR_ANGULO_EXTERNO:
        action = gira_esquerda_total(action)

    # 3. ACIMA DA VELOCIDADE HORIZONTAL EXTERNA PARA A DIREITA E GRAU INCORRETO
    # VH > LHE, VV < LV -> GDT, MP
    # VH > LHE -> GDT
    elif vel_hor > LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_direita_total(action)
        action = principal_parcial(action)
    elif vel_hor > LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO:
        action = gira_direita_total(action)

    # 4. ACIMA DA VELOCIDADE HORIZONTAL EXTERNA PARA A ESQUERDA E GRAU CORRETO
    # VH < -LHE, O > -1.8 * LAE, VV < LV -> GDT, MP
    # VH < -LHE, O > -1.8 * LAE -> GDT
    elif vel_hor < -LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO and orient > -1.8 * LIMIAR_ANGULO_EXTERNO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_direita_total(action)
        action = principal_parcial(action)
    elif vel_hor < -LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO and orient > -1.8 * LIMIAR_ANGULO_EXTERNO:
        action = gira_direita_total(action)

    # 5. ACIMA DA VELOCIDADE HORIZONTAL EXTERNA PARA A ESQUERDA E GRAU INCORRETO
    # VH < -LHE, VV < LV -> GET, MP
    # VH < -LHE -> GET
    elif vel_hor < -LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_esquerda_total(action)
        action = principal_parcial(action)
    elif vel_hor < -LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO:
        action = gira_esquerda_total(action)

    # 6. FORA DOS LIMITES A ESQUERDA E O GRAU CORRETO
    # H < -LH, O > -LAE, VV < LV -> GDT, MP
    # H < -LH, O > -LAE -> GDT
    elif pos_hor < -LIMIAR_HORIZONTAL and orient > -LIMIAR_ANGULO_EXTERNO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_direita_total(action)
        action = principal_parcial(action)
    elif pos_hor < -LIMIAR_HORIZONTAL and orient > -LIMIAR_ANGULO_EXTERNO:
        action = gira_direita_total(action)

    # 7. FORA DOS LIMITES A ESQUERDA E O GRAU INCORRETO
    # H < -LH, VV < LV -> GET, MP
    # H < -LH -> GET
    elif pos_hor < -LIMIAR_HORIZONTAL and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_esquerda_total(action)
        action = principal_parcial(action)
    elif pos_hor < -LIMIAR_HORIZONTAL:
        action = gira_esquerda_total(action)

    # 8. FORA DOS LIMITES A DIREITA E O GRAU CORRETO
    # H > LH, O < LAE, VV < LV -> GET, MP
    # H > LH, O < LAE -> GET
    elif pos_hor > LIMIAR_HORIZONTAL and orient < LIMIAR_ANGULO_EXTERNO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_esquerda_total(action)
        action = principal_parcial(action)
    elif pos_hor > LIMIAR_HORIZONTAL and orient < LIMIAR_ANGULO_EXTERNO:
        action = gira_esquerda_total(action)

    # 9. FORA DOS LIMITES A DIREITA E O GRAU INCORRETO
    # H > LH, VV < LV -> GDT, MP
    # H > LH -> GDT 
    elif pos_hor > LIMIAR_HORIZONTAL and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_direita_total(action)
        action = principal_parcial(action)
    elif pos_hor > LIMIAR_HORIZONTAL:
        action = gira_direita_total(action)

    # 10. ACIMA DO LIMITE DE VELOCIDADE HORIZONTAL A DIREITA PERMITIDO INTERNAMENTE COM GRAU CORRETO
    # VH > LVH, O < Θ, VV < LV -> GET, MP
    # H > LVH, O < Θ -> GET
    elif vel_hor > LIMIAR_VELOCIDADE_HORIZONTAL and orient < LIMIAR_ANGULO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_esquerda_total(action)
        action = principal_parcial(action)
    elif vel_hor > LIMIAR_VELOCIDADE_HORIZONTAL and orient < LIMIAR_ANGULO:
        action = gira_esquerda_total(action)

    # 11. ACIMA DO LIMITE DE VELOCIDADE HORIZONTAL A DIREITA PERMITIDO INTERNAMENTE COM GRAU INCORRETO
    # VH > LVH, VV < LV -> GDT, MP
    # VH > LVH -> GDT
    elif vel_hor > LIMIAR_VELOCIDADE_HORIZONTAL and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_direita_total(action)
        action = principal_parcial(action)
    elif vel_hor > LIMIAR_VELOCIDADE_HORIZONTAL:
        action = gira_direita_total(action)

    # 12. ACIMA DO LIMITE DE VELOCIDADE HORIZONTAL A ESQUERDA PERMITIDO INTERNAMENTE COM GRAU CORRETO
    # VH < -LVH, O > -Θ, VV < LV -> GDT, MP
    # VH < -LVH, O > -Θ -> GDT
    elif vel_hor < -LIMIAR_VELOCIDADE_HORIZONTAL and orient > -LIMIAR_ANGULO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_direita_total(action)
        action = principal_parcial(action)
    elif vel_hor < -LIMIAR_VELOCIDADE_HORIZONTAL and orient > -LIMIAR_ANGULO:
        action = gira_direita_total(action)

    # 13. ACIMA DO LIMITE DE VELOCIDADE HORIZONTAL A ESQUERDA PERMITIDO INTERNAMENTE COM GRAU INCORRETO
    # VH < -LVH, VV < LV -> GET, MP
    # VH < -LVH -> GET
    elif vel_hor < -LIMIAR_VELOCIDADE_HORIZONTAL and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_esquerda_total(action)
        action = principal_parcial(action)
    elif vel_hor < -LIMIAR_VELOCIDADE_HORIZONTAL:
        action = gira_esquerda_total(action)

    # 14. CORREÇAO FORTE DE GRAU A DIREITA NA EM DESCIDA NO PONTO CORRETO
    # O > 4 * Θ, VV < LV -> GDT, MP 
    # O > 4 * Θ -> GDT
    elif orient > 4 * LIMIAR_ANGULO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_direita_total(action)
        action = principal_parcial(action)
    elif orient > 4 * LIMIAR_ANGULO:
        action = gira_direita_total(action)

    # 15. CORREÇAO FORTE DE GRAU A ESQUERDA NA EM DESCIDA NO PONTO CORRETO
    # O < -4 * Θ, VV < LV -> GET, MP
    # O < -4 * Θ -> GET
    elif orient < -4 * LIMIAR_ANGULO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_esquerda_total(action)
        action = principal_parcial(action)
    elif orient < -4 * LIMIAR_ANGULO:
        action = gira_esquerda_total(action)

    # 16. CORREÇAO FRACA DE GRAU A DIREITA NA EM DESCIDA NO PONTO CORRETO
    # O < -Θ, VV < LV -> GDP, MP
    # O < -Θ -> GDP
    elif orient < -LIMIAR_ANGULO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_direita_parcial(action)
        action = principal_parcial(action)
    elif orient < -LIMIAR_ANGULO:
        action = gira_direita_parcial(action)
    
    # 17. CORREÇAO FRACA DE GRAU A ESQUERDA NA EM DESCIDA NO PONTO CORRETO
    # O > Θ, VV < LV -> GEP, MP
    # O > Θ -> GEP
    elif orient > LIMIAR_ANGULO and vel_ver < LIMIAR_VELOCIDADE_VERTICAL:
        action = gira_esquerda_parcial(action)
        action = principal_parcial(action)
    elif orient > LIMIAR_ANGULO:
        action = gira_esquerda_parcial(action)
    
    if action == [0, 0]:
        action = env.action_space.sample()
    
    return action

# Limiares definidos para o cenario COM vento

LIMIAR_ANGULO_VENTO = 0.015
LIMIAR_ANGULO_EXTERNO_VENTO = 0.062
LIMIAR_VELOCIDADE_VERTICAL_VENTO = -0.015
LIMIAR_VELOCIDADE_VERTICAL_EXTERNA = -0.06
LIMIAR_VELOCIDADE_HORIZONTAL_VENTO = 0.005
LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO_VENTO = 0.15
LIMIAR_HORIZONTAL_VENTO = 0.072

def agent_wind(observation):
    action = [0, 0]

    # Ambos os toques
    if toque_esquerdo(observation) == True and toque_direito(observation) == True: return action

    # ULTRAPASSA A VELOCIDADE MAXIMA PERMITIDA A DIREITA
    elif(velocidade_horizontal(observation) > 2*LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO_VENTO):
        # ORIENTA PARA ESQUERDA
        if orientacao(observation) < 3.1 * LIMIAR_ANGULO_EXTERNO_VENTO:
            action = gira_esquerda_total(action)
        elif orientacao(observation) > 3.3 * LIMIAR_ANGULO_EXTERNO_VENTO: action = gira_direita_total(action)
        # VELOCIDADE VERTICAL TOTAL
        if velocidade_vertical(observation) < 6 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action = principal_total(action)
        # VELOCIDADE VERTICAL PARCIAL
        elif velocidade_vertical(observation) < 5 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action = principal_parcial(action)

    # ULTRAPASSA A VELOCIDADE MAXIMA PERMITIDA A ESQUERDA  
    elif(velocidade_horizontal(observation) < -2*LIMIAR_VELOCIDADE_HORIZONTAL_EXTERNO_VENTO): 
        # ORIENTA PARA DIREITA
        if orientacao(observation) > -3.1 * LIMIAR_ANGULO_EXTERNO_VENTO:
            action = gira_direita_total(action)
        elif orientacao(observation) < -3.3 * LIMIAR_ANGULO_EXTERNO_VENTO: action = gira_esquerda_total(action)
        # VELOCIDADE VERTICAL TOTAL
        if velocidade_vertical(observation) < 6 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action = principal_total(action)
        # VELOCIDADE VERTICAL PARCIAL
        elif velocidade_vertical(observation) < 5 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action = principal_parcial(action)        

    # FORA DOS LIMITES A ESQUERDA
    elif(posicao_horizontal(observation) < -LIMIAR_HORIZONTAL_VENTO):
        # ORIENTA A DIREITA
        if orientacao(observation) > -2.7 * LIMIAR_ANGULO_EXTERNO_VENTO: action = gira_direita_total(action)
        elif orientacao(observation) < -2.8 * LIMIAR_ANGULO_EXTERNO_VENTO: action = gira_esquerda_total(action)

        # VELOCIDADE VERTICAL TOTAL
        if velocidade_vertical(observation) < 4 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action = principal_total(action)
        # VELOCIDADE VERTICAL PARCIAL
        elif velocidade_vertical(observation) < 3*LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action = principal_parcial(action)
    
    # FORA DOS LIMITES A DIREITA
    elif(posicao_horizontal(observation) > LIMIAR_HORIZONTAL_VENTO):
        # ORIENTA ESQUERDA
        if orientacao(observation) < 2.7 * LIMIAR_ANGULO_EXTERNO_VENTO: action = gira_esquerda_total(action)
        elif orientacao(observation) > 2.8 * LIMIAR_ANGULO_EXTERNO_VENTO: action = gira_direita_total(action)

        # VELOCIDADE VERTICAL TOTAL
        if velocidade_vertical(observation) < 4 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action[0] = principal_total(action)[0]
        # VELOCIDADE VERTICAL PARCIAL
        elif velocidade_vertical(observation) < 3 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action[0] = principal_parcial(action)[0]

    # ACIMA DO LIMITE DE VELOCIDADE HORIZONTAL A DIREITA PERMITIDO INTERNAMENTE
    elif(velocidade_horizontal(observation) > LIMIAR_VELOCIDADE_HORIZONTAL_VENTO):
        # ORIENTA A ESQUERDA
        if orientacao(observation) < LIMIAR_ANGULO_VENTO: action = gira_esquerda_total(action)
        elif orientacao(observation) > 1.2 * LIMIAR_ANGULO_VENTO: action = gira_direita_total(action)

        # VELOCIDADE VERTICAL TOTAL
        if velocidade_vertical(observation) < 4 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action = principal_total(action)
        # VELOCIDADE VERTICAL PARCIAL
        elif velocidade_vertical(observation) < 3 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action = principal_parcial(action)
        
    # ACIMA DO LIMITE DE VELOCIDADE HORIZONTAL A ESQUERDA PERMITIDO INTERNAMENTE
    elif(velocidade_horizontal(observation) < -LIMIAR_VELOCIDADE_HORIZONTAL_VENTO): 
        # ORIENTA A DIREITA
        if orientacao(observation) > -LIMIAR_ANGULO_VENTO: action = gira_direita_total(action)
        elif orientacao(observation) < -1.2 * LIMIAR_ANGULO_VENTO: action = gira_esquerda_total(action)

        # VELOCIDADE VERTICAL TOTAL
        if velocidade_vertical(observation) < 4 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action = principal_total(action)
        # VELOCIDADE VERTICAL PARCIAL
        elif velocidade_vertical(observation) < 3 * LIMIAR_VELOCIDADE_VERTICAL_EXTERNA:
            action = principal_parcial(action)

    # ORIENTA COM FORÇA A DIREITA INTERNAMENTE
    elif orientacao(observation) > 2.5 * LIMIAR_ANGULO_VENTO:
        action = gira_direita_total(action)
        # VELOCIDADE VERTICAL TOTAL
        if velocidade_vertical(observation) < 5 * LIMIAR_VELOCIDADE_VERTICAL_VENTO:
            action = principal_total(action)
        # VELOCIDADE VERTICAL PARCIAL
        elif velocidade_vertical(observation) < 4*LIMIAR_VELOCIDADE_VERTICAL_VENTO:
            action = principal_parcial(action)

    # ORIENTA COM FORÇA A ESQUERDA INTERNAMENTE
    elif orientacao(observation) < -2.5 * LIMIAR_ANGULO_VENTO:
        action = gira_esquerda_total(action)
        # VELOCIDADE VERTICAL TOTAL
        if velocidade_vertical(observation) < 5 * LIMIAR_VELOCIDADE_VERTICAL_VENTO:
            action = principal_total(action)
            
        # VELOCIDADE VERTICAL PARCIAL
        elif velocidade_vertical(observation) < 4 * LIMIAR_VELOCIDADE_VERTICAL_VENTO:
            action = principal_parcial(action)
    
    # ORIENTA PARCIAL ESQUERDA INTERNAMENTE
    elif orientacao(observation) > LIMIAR_ANGULO_VENTO:
        action = gira_esquerda_parcial(action)

        # VELOCIDADE VERTICAL TOTAL
        if velocidade_vertical(observation) < 4 * LIMIAR_VELOCIDADE_VERTICAL_VENTO:
            action = principal_total(action)
        # VELOCIDADE VERTICAL PARCIAL
        elif velocidade_vertical(observation) < 3*LIMIAR_VELOCIDADE_VERTICAL_VENTO:
            action = principal_parcial(action)
    
    # ORIENTA PARCIAL DIREITA INTERNAMENTE
    elif orientacao(observation) < -LIMIAR_ANGULO_VENTO:
        action = gira_direita_parcial(action)

        # VELOCIDADE VERTICAL TOTAL
        if velocidade_vertical(observation) < 4 * LIMIAR_VELOCIDADE_VERTICAL_VENTO:
            action[0] = principal_total(action)[0]
        # VELOCIDADE VERTICAL PARCIAL
        elif velocidade_vertical(observation) < 3*LIMIAR_VELOCIDADE_VERTICAL_VENTO:
            action[0] = principal_parcial(action)[0]

    # Garante que há uma ação definida
    if action == [0, 0]:
        action = env.action_space.sample()

    return action

success = 0.0
steps = 0.0

for i in range(EPISODES):
    if(not ENABLE_WIND): st, su = simulate(steps=1000000, policy=agent_no_wind)
    else: st, su = simulate(steps=1000000, policy=agent_wind)

    if su:
        steps += st
    success += su
    
    if su>0:
        print('Média de passos das aterragens bem sucedidas:', steps/success*100)
    print(': Taxa de sucesso:', success/(i+1)*100)

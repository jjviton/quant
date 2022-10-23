
"""
******************************************************************************
REINFORCED LEARNING FOR TRADING 
******************************************************************************
******************************************************************************


Fuente: #https://es.acervolima.com/juego-de-serpientes-impulsado-por-ia-usando-deep-q-learning/


En esta verison del programa organizamos en clases y lo tenemso preparado para hacer backTesting.
            


IMPROVEMENTS:    



Started on oct/2022
Version_1: 

Objetivo: 

    
BACKTEST:
    http://localhost:8888/notebooks/Documents/J3/100.-%20cursos/Quant_udemy/programas/Projects/6_regresionLineal/backTestREGRESIONLINEAL.ipynb


@author: J3Viton

"""




import torch
import random
import numpy as np
from collections import deque 

from game import TradingAI, Direction, Point  # EL JUEGO, Lo cambiaré por datos de la bolsa

from model import Linear_QNet, QTrainer   # RED NEURONAL
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    
    """CLASE AGENTE

       
    """  

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()  # array de doble entrada
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        """
        Fucnion que devuelve el estado actual del tablero de juego
        Returns:un array con la información

        """
        
        game.Observations('2021-9-19' )
        
        # 1.- Llama a Juego para conseguir es estado de todo el tablero de juego
        #head = game.snake[0]
        
        # State son los 11 estados que definen la posicon actual del juego. Se obtienen de las propiedades de la clase game
        state = [
            # Danger straight
            1,
            # Danger right
            1,
            # Danger left
            0,
            # Move direction
            0,
            1,
            0,
            0,
            # Food location 
            1,  # food left
            0,  # food right
            1,  # food up
            0  # food down
            ]

        return np.array(state, dtype=int)
    
    def get_action(self, state):
        """
        Funcion que calcula el siguiente movimiento segun el tradeoff explorar//explotar
        Returns:un array con la información

        """
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games   #ratio para manejar la explotacion
        
        final_move = [0,0,0]
        
        #Exploration
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1   #action es un array [0,0,1]  recto, giro derecha. giro izquierda
        
        #Explotation
        else:
            state0 = torch.tensor(state, dtype=torch.float)     # Creo un tensor tipo Torch
            prediction = self.model(state0)                     # Pido prediccion a la red
            move = torch.argmax(prediction).item()              # Me devuelve la probabilidad para cada accion. Argmax me dice el indice de la mayor
            final_move[move] = 1                                # Pongo a 1, el indice de la mayor probalilidad

        return final_move   # el array de siguiente accion [1,0,0]    



    def remember(self, state, action, reward, next_state, done):
        """
        Funcion que almacena todos los datos de cada movimiento.
        Returns: nada

        """        
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached
        
        

    def train_long_memory(self):

        """
        Funcion que toma un batch ramdon de los movimeinto en memoria y se los lanza a la red para entrenarla
        Returns: nada

        """         
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        """
        Funcion que toma un moviento de la partida y entrena la red
        Returns: nada

        """           
        self.trainer.train_step(state, action, reward, next_state, done)




def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = TradingAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
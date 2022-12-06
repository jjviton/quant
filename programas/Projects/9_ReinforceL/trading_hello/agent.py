
"""
******************************************************************************
REINFORCED LEARNING FOR TRADING 
******************************************************************************
******************************************************************************


Fuente: #https://es.acervolima.com/juego-de-serpientes-impulsado-por-ia-usando-deep-q-learning/


Vamos a realizar el 'Hola Mundo del trading con Reinforced Learning'. Basicamente el cruce de medias, la teoría dice que compres
con una media del precio muy larga (la tendencia), para luego entrar cuando una Media corta cruza al alza a una media un poco mas larga.
            


IMPROVEMENTS:    
    [13 nov 22] No parece que la red aprenda bien. Probaré un cambio de tactica, cada partida es recorrer otra vez
    el dataSerie... corro el riesgo de overfitting, pero sabre si la redNeuronal aprende (aunque sea regular :-)




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
import matplotlib.pyplot as plt

from game import TradingAI, Direction, Point  # EL JUEGO, Lo cambiaré por datos de la bolsa

from model import Linear_QNet, QTrainer   # RED NEURONAL
from helper import plot, plot2

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001    #♦j original 0.001


class Agent:
    
    """CLASE AGENTE

       
    """  

    def __init__(self):
        self.n_games = 1
        self.epsilon = 0 # randomness exploitation vs exploration
        self.gamma = 0.7 # discount rate   Original = 0.9  Como afectan futuras recompensas al Q. O=nada
        self.exploitation =1
        self.exploration=1
        
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()  # array de doble entrada
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        
        self.stage =0  # Indice con el que recorro el trading track
        ##self.inside =False   # Estoy comprado True. Si no False
        self.finalMove =0
        self.umbral =0


    def get_state(self, game, _stage):
        """
        Funcion que devuelve el estado actual del tablero de juego
        Returns:un array con la información

        """  
        state= game.Observations( game, _stage)
        
        return np.array(state, dtype=float)
  

    def get_action(self, state):
        """
        Funcion que calcula el siguiente movimiento segun el tradeoff explorar//explotar
        Trading: creo el array de decision [comprar, mantener, vender]
        Returns:un array con la información

        """
        # random moves: tradeoff exploration / exploitation
        #self.epsilon = 80 - self.n_games   #ratio para manejar la explotacion  ORIGINAL
        learningWindow = 500
        self.epsilon = learningWindow - self.stage
        
        final_move = [0,0,0]
        
        #Exploration  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if random.randint(0, 2*learningWindow) < self.epsilon:
            move = random.randint(0, 2)    #decision aleatoria C/M/V
            final_move[move] = 1   #action es un array [0,0,1]  Compro, Mantengo, Vendo   B/H/S
            self.exploration +=1
            
        #Exploitation  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        else:
            state0 = torch.tensor(state, dtype=torch.float)     # Creo un tensor tipo Torch
            prediction = self.model(state0)                     # Pido prediccion a la red
            move = torch.argmax(prediction).item()              # Me devuelve la probabilidad para cada accion. Argmax me dice el indice de la mayor
            final_move[move] = 1                                # Pongo a 1, el indice de la mayor probalilidad
            self.exploitation +=1                     

        #final_move = [0,0,1]
        return final_move   # el array de siguiente accion [1,0,0]    // Buy/Hold/Sell
    
    def get_actionExploi(self, state):
        """
        Funcion que calcula el siguiente movimiento segun el tradeoff explorar//explotar
        Esta función esta hecha para explotar el sistema aprendido antes
        Returns:un array con la información

        """
        final_move = [0,0,0]
        state0 = torch.tensor(state, dtype=torch.float)     # Creo un tensor tipo Torch
        prediction = self.model(state0)                     # Pido prediccion a la red
        move = torch.argmax(prediction).item()              # Me devuelve la probabilidad para cada accion. Argmax me dice el indice de la mayor
        final_move[move] = 1                                # Pongo a 1, el indice de la mayor probalilidad
        self.exploitation +=1                     

        return final_move   # el array de siguiente accion [1,0,0]    // Buy/Hold/Sell



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
    plot_aux01 = []
    plot_aux02 = []
    plot_aux03 = []
    plot_aux04 = []
    plot_aux05 = []
    plot_aux06 = []
    total_score = 0
    record = 0
    
    #Llamamos a los constructores
    agent = Agent()
    game = TradingAI()

    agent.stage =0
    
    aux32=0
    plot_aux04.append(1 )
    plot_aux05.append(1 )
    plot_aux06.append(1 )
    
    

    
    ##*************************************************************************
    ## PRIMERA FASE DE ENTRENO DE LA RED PARA CALCULAR EL VALOR DE LOS TENSORES
    ## Aqui utilizo el tradeoff 
    
    while True:   ##agent.stage < len(game.df):    #hasta que stage llegue al final y ¿repetimos?
         
        # get old state
        state_old = agent.get_state( game,agent.stage)  

        # get move
        ##finalKK= agent.get_actionExploi(state_old)  ###
        
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(game, agent.stage, final_move)
        agent.stage+=1
        #print('reward', reward)
        state_new = agent.get_state(game, agent.stage)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        
        if (reward ==10):
            ##agent.train_long_memory()  # esto se hace al acabar una partida completa,lo aplico a ver que pasa.
            plot_aux04.append(agent.stage-1)
        if (reward ==1):
            ##agent.train_long_memory()  # esto se hace al acabar una partida completa,lo aplico a ver que pasa.
            plot_aux06.append(agent.stage-1)            
        if (reward ==-5):
            ##agent.train_long_memory()  # esto se hace al acabar una partida completa,lo aplico a ver que pasa.
            plot_aux05.append(agent.stage-1)                        
            
        
        if done:
            # train long memory, plot result
        
            #j#agent.n_games += 1
            agent.train_long_memory()

            if score > record:  
                record = score
                agent.model.save()   # Solo debemos hacer save de la red si ha ido bien???
                ##Creo que al grabar se pierden los datos de los tensores
                print('\n ********************************************** R E C O R D ')
                ##if record >30:
                ##    break

            #print('Game', agent.n_games, 'Score', score, 'Record:', record)

            print(' Acabado ')
            print('Total ',len(game.df), '; ///////// SCORE =>', score,'\n', 'Exploitation %d' %(100*agent.exploitation/len(game.df)), '%','\n')    
            print('Profit = %d' %game.profit, 'Loss= %d' %game.loss, '________ Profit porcentage %.2f' %(100*game.profit/(game.loss+game.profit)),'%')
            ##plot(plot_aux01 , plot_aux02 , plot_aux03)
            
            
            game.reset()
            agent.stage=0
            agent.exploitation =0
            agent.exploration =0
            
            agent.umbral=25
            
            if(record <=agent.umbral   ):
                plot_aux04.clear()  # vacio la list
                plot_aux05.clear()
                plot_aux06.clear()
            
            #j# return
            #j#break
      
        ## Grafico
        #total_score += score
        #mean_score = total_score / agent.n_games
        
        plot_aux01.append(game.profit )
        plot_aux02.append(game.buyOrder)
        plot_aux03.append(agent.exploration)
        ##plot(plot_aux01 , plot_aux02 , plot_aux03)
        
        if (record> agent.umbral ):
            ##game.df[['Close','EMA_50','EMA_200','EMA_30']].plot()
           
            # specifying the plot size
            plt.figure(figsize = (10, 5))
            # only one line may be specified; full height
            ##plt.axvline(x=plot_aux04, color = 'b', label = 'ght') 
            for xc in plot_aux04:
                plt.axvline(x=xc,color ='lime')
            for xc in plot_aux05:
                plt.axvline(x=xc, color='r')      
            for xc in plot_aux06:
                plt.axvline(x=xc, color='deepskyblue')     
            plt.plot(game.df[['Close','EMA_50','EMA_200','EMA_30']])
            plt.title(" ENTRENAMIENTO ")
            # rendering plot
            plt.show()
            aux32=game.buyOrder
            ##plot_aux04.clear()  # vacio la list
            ##plot_aux05.clear()
            ##plot_aux06.clear()
            break
           

        
    ##*************************************************************************
    ## SEGUNDA FASE EXPLOTO EL SISTEMA
    ## Casi igual pero ahora todo explotar y ver que tasa de acierto nos da.
    
    agent.stage=0   #Reiniciamos la serie
    agent.exploitation =0
    agent.exploration =0
    game.score = 0
    game.profit = 1
    agent.finalMove =0
    game.loss = 1
    game.inside = False 
    game.buyOrder =0
    
    plot_aux011 = []
    plot_aux022 = []
    plot_aux033 = []
    plot_aux044 = []
    plot_aux04.clear()  # vacio la list
    plot_aux05.clear()
    plot_aux06.clear()    
    done = False
    
    while agent.stage < len(game.df):    #hasta que stage llegue al final y ¿repetimos?
         
        # get old state
        state_old = agent.get_state( game,agent.stage)

        # get move
        final_move = agent.get_actionExploi(state_old)
        
        # perform move and get new state
        reward, done, score = game.play_step(game, agent.stage, final_move)
        agent.stage+=1
        #print('reward', reward)
        #state_new = agent.get_state(game, agent.stage)

        # train short memory
        ##agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        ##agent.remember(state_old, final_move, reward, state_new, done)
        
        if (agent.stage == len(game.df) -1):
            done = True

        plot_aux011.append(game.profit )
        plot_aux022.append(game.buyOrder)
        plot_aux033.append(agent.finalMove)
        
        if (reward ==10):
            ##agent.train_long_memory()  # esto se hace al acabar una partida completa,lo aplico a ver que pasa.
            plot_aux04.append(agent.stage-1)
        if (reward ==1):
            ##agent.train_long_memory()  # esto se hace al acabar una partida completa,lo aplico a ver que pasa.
            plot_aux06.append(agent.stage-1)            
        if (reward ==-5):
            ##agent.train_long_memory()  # esto se hace al acabar una partida completa,lo aplico a ver que pasa.
            plot_aux05.append(agent.stage-1)    
        
        if done:
            # train long memory, plot result
            #game.reset()
            #agent.n_games += 1
            ##agent.train_long_memory()

            #if score > record:
            #   record = score
            #   agent.model.save()   # Solo debemos hacer save de la red si ha ido bien???

            #print('Game', agent.n_games, 'Score', score, 'Record:', record)

            #plot_scores.append(score)
            #total_score += score
            #mean_score = total_score / agent.n_games
            #plot_mean_scores.append(mean_score)
            #plot(plot_scores, plot_mean_scores)
            
            print('\n ----- EXPLOITATION ----')
            print('Total ',len(game.df), '; Score', score,'\n', 'Exploration %d' %(100*agent.exploration/len(game.df)), '%','\n')    
            print('Profit = %d' %game.profit, 'Loss= %d' %game.loss, '__________ Porcentage %.2f' %(100*game.profit/(game.loss+game.profit)),'%')
            
            # specifying the plot size
            plt.figure(figsize = (10, 5))
            # only one line may be specified; full height
            ##plt.axvline(x=plot_aux04, color = 'b', label = 'ght') 
            for xc in plot_aux04:
                plt.axvline(x=xc,color ='lime')
            for xc in plot_aux05:
                plt.axvline(x=xc, color='r')      
            for xc in plot_aux06:
                plt.axvline(x=xc, color='deepskyblue')     
            plt.plot(game.df[['Close','EMA_50','EMA_200','EMA_30']])
            plt.title("TEST DE LA RED NEURONAL ")
            # rendering plot
            plt.show()
            
            #j#plot2(plot_aux011 , plot_aux022 , plot_aux033)
            return        


if __name__ == '__main__':
    train()
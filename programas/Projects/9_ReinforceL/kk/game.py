##import pygame
import time
import datetime as dt
import yfinance as yf
import sys
sys.path.insert(0,"C:\\Users\\INNOVACION\\Documents\\J3\\100.- cursos\\Quant_udemy\\programas\\Projects\\libreria")
import quant_j3_lib as quant_j
from pykalman import KalmanFilter



import random
from enum import Enum
from collections import namedtuple
import numpy as np
import pandas as pd
##pygame.init()
##font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum): ##
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Actions(Enum):
    BUY = 1
    SELL = 2
    HOLD = 3
    


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 80

class TradingAI:

    def __init__(self, instrumento = 'SAN'):
        ##self.w = w
        ##self.h = h
        # init display
        ##self.display = pygame.display.set_mode((self.w, self.h))
        ##pygame.display.set_caption('Snake')
        
        self.currentDate = dt.datetime.today()
        
        self.clock = time.time()
        self.reset()
        # Leemos los valores del instrumento desde el -Yahoo finnaces para tener el set de datos
        
        
        #### FECHAS
        #start =dt.datetime(2000,1,1)
        self.start =dt.datetime.today() - dt.timedelta(days=2000)    #un año tiene 250 sesiones.
        #end = dt.datetime(2019,10,1)
        self.end= dt.datetime.today()  - dt.timedelta(days=1)        #Quito hoy para no ver el valor al ejecutar antes del cierre
        #end = '2021-9-19' 
        
        #### Los datos del instrumento
        self.instrumento = instrumento
        self.df = yf.download(self.instrumento, self.start, self.end)  # diario OCHLV
        self.df.dropna(inplace=True) 
        
        self.df =self.featured_Data(self.df)    # calculamos extra features 
        
    def featured_Data (self, dff):
        """
        Descripcion: this method calculates the extra features of the eviroment observation. 
        Aqui es donde radica parte del arte de este poryecto, como diseñar la estrategia y los rewards.
        En definitiva enriquecemos el dataSet.
        
        Parameters
        ----------
            df: 
        Returns
        -------
            TYPE
                DESCRIPTION.
        """
   
        # Calculo el media exponencial del Volumen de los ultimos dias
        df_aux =dff.loc[:,['Volume','Open']] #si paso una sola hace una serie y rompe todo
        df_aux.rename(columns={'Volume': 'Close'}, inplace=True)       
        df_aux= quant_j.ExponentialMovingAverage(df_aux)
        df_aux.rename(columns={'EMA_30': 'VolEMA_30'}, inplace=True)
        del df_aux['EMA_200']
        dff['VolEMA_30']= df_aux['VolEMA_30']  
        dff.dropna(inplace=True)
        dff['DeltaVol_EMA']=dff['Volume']-dff['VolEMA_30']
        
        # El amigo Kalman
        
        # 1.- CALCULAMOS EL FILTRO DE KALMAN
        # Construct a Kalman filter
        kf = KalmanFilter(transition_matrices = [1],
                      observation_matrices = [1],
                      initial_state_mean = 0,
                      initial_state_covariance = 1,
                      observation_covariance=1,
                      transition_covariance=.01)
        state_meansS, _ =kf.smooth(dff.Close)
        state_meansS = pd.Series(state_meansS.flatten(), index=dff.index)
        dff['Kalman'] = state_meansS
        
        # Regresion lineal ultimas 50 sesiones
        close_ =dff.columns.get_loc("Close")
        slice01= dff.iloc[-50:,close_]
        coef_, intercept_= quant_j.linearRegresion_J3(slice01)
        
        # SUPERVISED: Un poco de supervisado  https://www.aprendemachinelearning.com/pronostico-de-series-temporales-con-redes-neuronales-en-python/
        dias = 1   # 1= cierre de mañana
        dff['Futuro'] = dff['Close'].shift((-1)*dias)
        
        # Coloco un indice natural y incremental
        dff['position']=dff['Close']   #columna fake
        position_ =dff.columns.get_loc("position")
        for i in range(len(dff)):
            dff.iloc[i,position_] = int( i)
        # Cambio el indice del Dataframe
        dff.set_index('position', drop=False,inplace=True)
     
            

        
        
        print(dff.head())

        
        
        return dff



    def Observations (self, game, _stage):
        """
        Descripcion: This function returns all today´s data. Market basic data and featured data
                
        Parameters
        ----------
            df: 
        Returns
        -------
            numpay array containing al information
        """
        
        # State son los 11 estados que definen la posicon actual del juego. Se obtienen de las propiedades de la clase game
        state = np.zeros(11)
 
        state[0] = game.df.loc[_stage,'Open']   
        state[1] = game.df.loc[_stage,'Close']   
        state[2] = game.df.loc[_stage,'High']   
        state[3] = game.df.loc[_stage,'Low']   
        state[4] = game.df.loc[_stage,'Volume'] 
        state[5] = game.df.loc[_stage,'DeltaVol_EMA']
        state[6] = game.df.loc[_stage,'Kalman']   
        state[7] = game.df.loc[_stage,'Futuro']    
        
        return np.array(state, dtype=float)
    
    


    def reset(self):
        # init game state
        ##self.direction = Direction.RIGHT

        ##self.head = Point(self.w/2, self.h/2)
        ##self.snake = [self.head,
        ##Point(self.head.x-BLOCK_SIZE, self.head.y),
        ##Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        ##self._place_food()
        self.frame_iteration = 0

    """
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
    """

    def play_step(self, game, _stage, action):
        """
        Descripcion: Avanza un paso en la secuencia temporal de precios. No es como un juego que tiene un 'mapa'... en nuestro caso
        de acciones tenemos una serie temporal, digamos lineal (unidimensional)
        Parameters
        ----------
            Recibe un array de tres elementos con uno seteado Buy//Hold//Sell  [0,1,0]    
        Returns
        -------
            reward
        """        
        
        # Calculo el Reward (empiezo con la simplest version). Esta es la parte más compleja y que requiere de mi...
        reward =0
        
        # Si el dia siguente abre mas alto reward++
        # Si el dia sigueitne abre más bajo reward--
        
        if   (game.df.loc[_stage,'Futuro'] > (1.01*game.df.loc[_stage,'Close'])):
            reward +=10  
            self.score +=1
        elif (game.df.loc[_stage,'Futuro'] < game.df.loc[_stage,'Close']):
            reward -=10
        else:
            reward +=0

        
        return reward, False, self.score


    def is_collision(self, pt=None):
        """
        ##if pt is None:
        ##    pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        """
        return False

    """
    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
    """
    """
    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
     """   
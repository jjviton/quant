echo ON
del salida.txt
cd C:\Users\INNOVACION\Documents\J3\100.- cursos\Quant_udemy\programas
call conda activate trading

python estrategia_03_v2.py >salida.txt

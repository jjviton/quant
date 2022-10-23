echo ON
del salida.txt
cd C:\Users\INNOVACION\Documents\J3\100.- cursos\Quant_udemy\programas
call conda activate trading

rem python estrategia_03_v2.py >salida.txt

rem cd C:\Users\INNOVACION\Documents\J3\100.- cursos\Quant_udemy\programas\Projects\regresionLineal_MediaMovil
rem python regresionAMedia.py >salida.txt

cd C:\Users\INNOVACION\Documents\J3\100.- cursos\Quant_udemy\programas\Projects\6_regresionLineal
python regresionAMedia.py >salida.txt

cd C:\Users\INNOVACION\Documents\J3\100.- cursos\Quant_udemy\programas\Projects\6_regresionLineal\6_regresionLineal_v2
python regresionAMedia.py   

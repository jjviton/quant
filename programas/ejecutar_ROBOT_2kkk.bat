echo ON
del salida.txt
cd C:\Users\INNOVACION\Documents\J3\100.- cursos\Quant_udemy\programas\Projects\kalmanIndicator\kalmanRealtime
call conda activate trading

python KalmanREALTIME_telegram-version2.py >salida.txt

rem cd C:\Users\INNOVACION\Documents\J3\100.- cursos\Quant_udemy\programas\Projects\regresionLineal_MediaMovil
rem python regresionAMedia.py >salida.txt

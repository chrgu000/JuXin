function Comm=commission(pEx,p_1,etf50_1) % pEx:义务仓行权价；p_1:期权昨日收盘价；etf50_1:50etf昨日收盘价
    imaginary=max(pEx-etf50_1,0);
    Comm=(p_1+max(0.12*etf50_1-imaginary,0.07*etf50_1))*15000;
end
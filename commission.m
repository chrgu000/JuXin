function Comm=commission(pEx,p_1,etf50_1) % pEx:�������Ȩ�ۣ�p_1:��Ȩ�������̼ۣ�etf50_1:50etf�������̼�
    imaginary=max(pEx-etf50_1,0);
    Comm=(p_1+max(0.12*etf50_1-imaginary,0.07*etf50_1))*15000;
end
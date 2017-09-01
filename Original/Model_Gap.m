function op1=Model_Gap(I)

global open high low close vol;
op1=0;

if (low(I-1)-open(I))/close(I-1)>=0.01 && vol(I-1)<vol(I-2)*0.8 %&& close(I-2)<close(I-3)
    op1=open(I);
end
end
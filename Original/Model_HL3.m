function [op1,op2]=Model_HL3(I)
global date open high low close vol;
op1=0;
op2=0;
   
if close(I-1)>mean(close(I-9:I-1)) && low(I)<mean(low(I-3:I-1));
    op1=mean(low(I-3:I-1));
end

if high(I)>mean(high(I-3:I-1));
    op2=close(I);
end

end


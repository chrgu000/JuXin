function op1=Model_Reverse(I)
global date open high low close vol;
op1=0;
ratio=1.8;
   
if close(I-1)<min(close(I-5:I-2)) % && weekday(date(I))-1~=5
    diff=high(I-5:I-2)-open(I-5:I-2);
    if high(I)>open(I)+ratio*mean(diff)
        op1=open(I)+ratio*mean(diff);
    end
end
end
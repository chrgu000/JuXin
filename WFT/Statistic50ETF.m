function Statistic50ETF
w=windmatlab;
[close,~,~,date]=w.wsd('510050.SH','close','ED-251TD',today-1,'PriceAdj=F');
L=length(date);
results=zeros(L,1);
for j=2:L
    wd=weekday(date(j))-1;
    M=month(date(j));
    monthups=[2,3,4,7,9,10,11,12];
    monthdowns=[1,5,6,8]; 
    if sum(monthups==M)
        monthParaUp=1;
        monthParaDown=0;
    elseif sum(monthdowns==M)
        monthParaUp=0;
        monthParaDown=1;
    else
        monthParaUp=0;
        monthParaDown=0;
    end
    ratio=close(j)/close(j-1)-1;
    switch wd
        case 1
            results(j)=monthParaUp*ratio;
        case 2
            results(j)=-monthParaDown*ratio;
        case 3
            results(j)=monthParaUp*ratio;
        case 4
            results(j)=-monthParaDown*ratio;
        case 5
            results(j)=monthParaUp*ratio;
    end
end
results=cumprod(results+1)-1;
figure;
plot([results,close./close(1)-1]);
end
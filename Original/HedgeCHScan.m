function HedgeCHScan
n=input('trade today for tomorrow or not?  y/n [y]:','s');
w=windmatlab;
if n=='n'
    data=w.wsd('ic00.cfe,ih00.cfe','pct_chg','ED-1TD',today);
    temLast=(data(1,1)-data(1,2))/100;
    wd=weekday(today)-1;
    display(['today is ',num2str(wd),'; trade for today as below; temLast value is: ',num2str(temLast)]);
else
    data=w.wsq('ic00.cfe,ih00.cfe','rt_pct_chg');
    temLast=data(1)-data(2);
    wd=weekday(today);
    display(['today is ',num2str(wd-1),'; trade for tomorrow as below; temLast value is: ',num2str(temLast)]);
end
switch wd
    case 1 % hold status on monday;
        if temLast>=-0.0180 && temLast<=0.0279 %  -1.8% <= diff <= 2.79%
            display({'Buy: IH -- 2 hands;';'Sell: IC -- 1 hand;'}); %results(i)=-tem;
        elseif temLast<0.037 % diff <= 3.7%
            display({'Buy: IC -- 1 hand;';'Sell: IH -- 2 hands;'}); %results(i)=tem;
        end
    case 2
        if temLast>=-0.05 && temLast<=0.075 % -5%  <= diff <= 7.5%
            display({'Buy: IC -- 1 hand;';'Sell: IH -- 2 hands;'}); %results(i)=tem;
        else
            display({'Buy: IH -- 2 hands;';'Sell: IC -- 1 hand;'}); %results(i)=-tem;
        end
    case 3
        if temLast>=-0.006 %  0.6% <= diff
            display({'Buy: IH -- 2 hands;';'Sell: IC -- 1 hand;'}); %results(i)=-tem;
        else
            display({'Buy: IC -- 1 hand;';'Sell: IH -- 2 hands;'}); %results(i)=tem;
        end
    case 4
        if temLast>=-0.065 %  6.5% <= diff
            display({'Buy: IC -- 1 hand;';'Sell: IH -- 2 hands;'}); %results(i)=tem;
        else
            display({'Buy: IH -- 2 hands;';'Sell: IC -- 1 hand;'}); %results(i)=-tem;
        end
    case 5
        if temLast>=0.031 % 3.1% <= diff
            display({'Buy: IH -- 2 hands;';'Sell: IC -- 1 hand;'}); %results(i)=-tem;
        else
            display({'Buy: IC -- 1 hand;';'Sell: IH -- 2 hands;'}); %results(i)=tem;
        end
    case 6
        if temLast>=-0.0180 && temLast<=0.0279 %  -1.8% <= diff <= 2.79%
            display({'Buy: IH -- 2 hands;';'Sell: IC -- 1 hand;'}); %results(i)=-tem;
        elseif temLast<0.037 % diff <= 3.7%
            display({'Buy: IC -- 1 hand;';'Sell: IH -- 2 hands;'}); %results(i)=tem;
        end
end
end




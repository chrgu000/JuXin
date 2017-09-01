function [op1,op4,op41,ord,udlen]=Model_DownUpDown % back forward is less than half of current up forward
global high low vol;
op1=0;
op4=0;
op41=0;
ord(10,3)=0;
udlen(15,3)=0;
L=length(high);
if low(L)<=low(lowest(L-5,L))
    kline=0;
    for j=3:20
        if L-ceil(3*j/2)<=0
            break;
        else
            flag=0;
        end
        if high(L-j)>=high(highest(L-ceil(3*j/2),L))
            for jj=L-3*j-3:L-j-1
                if jj-ceil(3*j/2)<=0
                    flag=1;
                    break;
                end
                if low(jj)<=low(lowest(jj-ceil(j/2),L-j)) && high(highest(jj-j-1,jj-j+1))>=high(highest(jj-ceil(3*j/2),L))...
                        && low(L)<=low(lowest(jj-j,L)) 
                    H1=highest(jj-j-1,jj-j+1);
                    L1=lowest(jj-1,jj+1);
                    H2=highest(L-j-1,L-j+1);
                    Bar0=4*(L-H1); % Bar0 is back forward's start point;
                    if L<Bar0
                        Bar0=L-1;
                    end
                    if (high(H1)-low(L1))/(L1-H1)>=(high(H2)-low(L))/(L-H2) && AboveHalf(Bar0)
                        kline=kline+1;
                        X(1,kline)=jj-j; Y(1,kline)=high(jj-j);
                        X(2,kline)=jj;   Y(2,kline)=low(jj);
                        X(3,kline)=L-j;  Y(3,kline)=high(L-j);
                        X(4,kline)=L;    Y(4,kline)=low(L);
                        
                        ord1=mean(vol(jj-j:jj));
                        ord2=mean(vol(L-j:L));
                        ord3=mean(vol(jj:L-j));
                        ordH1=high(jj-j)*1.03;
                        ordH2=high(L-j)*1.03;
                        ordH=max(ordH1,ordH2);
                        ordL1=low(jj)*0.95;
                        ordL2=low(L)*0.95;
                        ordL=min(ordL1,ordL2);
                        if ord==0
                            ord(1:2,:)=[(2*jj-j)/2-2,ordH,roundn(ord1/ord2,-2);(2*L-j)/2-2,ordH,roundn(ord3/ord2,-2)];
                            udlen(1:3,:)=[jj-2,ordL,high(highest(jj-j-1,jj-j+1))-low(jj);(jj+L)/2,ordL,high(L-j)-low(jj);L+1,ordL,high(L-j)-low(L)];
                        else
                            rowO=sum(sum(ord')~=0);
                            ord(rowO+1:rowO+2,:)=[(2*jj-j)/2-2,ordH,roundn(ord1/ord2,-2);(2*L-j)/2-2,ordH,roundn(ord3/ord2,-2)];
                            udlen(rowO+1:rowO+3,:)=[jj-2,ordL,high(highest(jj-j-1,jj-j+1))-low(jj);(jj+L)/2,ordL,high(L-j)-low(jj);L+1,ordL,high(L-j)-low(L)];
                        end
                        if abs(ord1-ord3)/ord1>0.45 || abs(ord2-ord3)/ord2>0.45
                            kline=kline+1;
                        end
                        
                    end
                end
            end
        end
        if flag==1
            break;
        end
    end
    if kline>0
        op1=kline;
        op4=X;
        op41=Y;
    end
end
end
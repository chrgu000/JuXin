function op1=Model_Spring(I)
global open high low close vol;
op1=0;

limitP=high(I-1)-low(I-1);
if ( abs(close(I-1)-open(I-1))<limitP/3 && close(I-1)+open(I-1)<high(I-1)+low(I-1) && high(I)>high(I-1) ||...
        close(I-1)<low(I-1)+limitP/4 && high(I)>high(I-1) && low(I-1)>min(low(I-3:I-2))&&high(I-1)>high(I-2) )...
        && vol(I-1)>mean(vol(I-12:I-1)) 
    op1=max(open(I),high(I-1));
end

end

% 
% function op1=Model_Spring
% global open high low close vol;
% op1=0;
% I=length(high);
% limitP=high(I-1)-low(I-1);
% if ( abs(close(I-1)-open(I-1))<limitP/3 && close(I-1)+open(I-1)<high(I-1)+low(I-1) && high(I)>high(I-1) )|| ...
%    ( close(I-1)<low(I-1)+limitP/4 && high(I)>high(I-1) && low(I-1)>min(low(I-3:I-2))&&high(I-1)>high(I-2) )...
%         && vol(I-1)>mean(vol(I-12:I-1)) 
%     op1=max(open(I),high(I-1));
% end
% 
% end
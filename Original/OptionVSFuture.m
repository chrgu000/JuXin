function OptionVSFuture(reqid,isfinished,errorid,datas,codes,fields,times,selfdata) %w.wsq('10000869.SH,ih1705.cfe','rt_last',@OptionVSFuture)
try
    load OptionVSFuture;
    if(length(codes)==0|| length(fields)==0||length(times)==0)
    else
        if(length(times)==1)
            datas = reshape(datas,length(fields),length(codes))';
        elseif (length(codes)==1)
            datas = reshape(datas,length(fields),length(times))';
        elseif(length(fields)==1)
            datas = reshape(datas,length(codes),length(times));
        end
    end
    indO=find(strcmp(codes,{'10000869.SH'}),1);
    indF=find(strcmp(codes,{'IH1705.CFE'}),1);
    if ~isempty(indO)
        priceO=datas(indO);
        lastO=datas(indO);
    else
        priceO=lastO;
    end
    if ~isempty(indF)
        priceF=datas(indF);
        lastF=datas(indF);
    else
        priceF=lastF;
    end
    diff=priceF*300-(2.25+priceO)*300000-3100;
    if lastO==0||lastF==0
        save OptionVSFuture lastO lastF minute y;
        return;    
    end
    minuteT=datevec(times);
    minuteT=minuteT(5);
    if minute==minuteT
        y(end)=diff;
    elseif minute~=-1
        minute=minuteT;
        y=[y,diff];
        if ~mod(minute,5)
            fprintf('\nCancel this by codes: ''w.cancelRequest(%d)''',reqid);
        end
    else
        minute=minuteT;
        figure;
        plot(y);
        ymin=min(y);
        ymax=max(y);
        axis([0,length(y)+1,ymin-100,ymax+100]);
        grid on;
    end
    if ~(length(y)==1&&y==0)      
        ymin=min(y);
        ymax=max(y);
        axis([0,length(y)+1,ymin-abs(ymin)/10,ymax+abs(ymax)/10]);
        h=findobj(gca,'Type','Line');
        if isempty(h)
            plot(y);
            axis([0,length(y)+1,ymin-abs(ymin)/10,ymax+abs(ymax)/10]);
        else
            set(h,'XData',1:length(y),'YData',y);
        end
        grid on;
    end
    % set(h,'XData',1:length(y),'YData',y)
    save OptionVSFuture lastO lastF minute y;   
catch
    lastO=0;
    lastF=0;
    minute=-1;
    y=0;
    save OptionVSFuture lastO lastF minute y; 
end
end



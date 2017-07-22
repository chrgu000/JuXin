 function [newDate,newOpen,newHigh,newLow,newClose,newVolume] = ReSampleUsed(period,DATE,OPEN,HIGH,LOW,CLOSE,VOLUME)
%Raw data is day data and 'date' is number type of date;
%In puts:
%period: 'day'-- get day lines data;'week'-- get week lines data;'month'-- get month lines data;
% 'quarter'-- get quarter lines data; 'year'--year lines data;
%Out puts:
%newDate,newOpen,newHigh,newLow,newClose,newVolume,newAmt,newTurn

if strcmpi(period,'week') == 1
    tDate = DATE-weekday(DATE); 
elseif strcmpi(period,'month') == 1
    tDate = DATE-day(DATE);
elseif strcmpi(period,'quarter') == 1
    tDate = year(DATE)*10 +ceil(month(DATE)/3);
elseif strcmpi(period,'year') == 1
    tDate = year(DATE);
else
    newDate = DATE;
    newOpen = OPEN;
    newHigh = HIGH;
    newLow = LOW;
    newClose = CLOSE;
    newVolume = VOLUME;
    return;
end

nlen = length(DATE);

k = 1;
newDate(k) = DATE(1);newOpen(k) = OPEN(1);newHigh(k) = HIGH(1);newLow(k) = LOW(1);
newClose(k) = CLOSE(1);newVolume(k) = VOLUME(1);

for i=2:nlen
    if tDate(i) ~= tDate(i-1)
        k = k+1;
        newDate(k) = DATE(i);
        newOpen(k) = OPEN(i);
        newHigh(k) = HIGH(i);
        newLow(k) = LOW(i);
        newClose(k) = CLOSE(i);
        newVolume(k) = VOLUME(i);
    else
        if HIGH(i) > newHigh(k)
            newHigh(k) = HIGH(i);
        end
         
        if LOW(i) < newLow(k)
            newLow(k) = LOW(i);
        end
        
        newDate(k) = DATE(i);
        newClose(k) = CLOSE(i);
        newVolume(k) = newVolume(k) + VOLUME(i);
    end
end

 newDate = newDate';
 newOpen = newOpen';
 newHigh = newHigh';
 newLow = newLow';
 newClose = newClose';
 newVolume = newVolume';
end
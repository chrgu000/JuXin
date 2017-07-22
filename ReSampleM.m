function StockData = ReSampleM(period,DATE,OPEN,HIGH,LOW,CLOSE,VOLUME,AMT,TURN)

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
    newAmt = AMT;
    newTurn = TURN;
    return;
end

nlen = length(DATE);

k = 1;
newDate(k) = DATE(1);newOpen(k) = OPEN(1);newHigh(k) = HIGH(1);newLow(k) = LOW(1);
newClose(k) = CLOSE(1);newVolume(k) = VOLUME(1);newAmt(k) = AMT(1);newTurn(k) = TURN(1);
StockData(1).date = newDate';
StockData(1).open = newOpen';
StockData(1).high = newHigh';
StockData(1).low = newLow';
StockData(1).close = newClose';
StockData(1).volume = newVolume';
StockData(1).amt = newAmt';
StockData(1).turn = newTurn';
for i=2:nlen
    if tDate(i) ~= tDate(i-1)
        k = k+1;
        newDate(k) = DATE(i);
        newOpen(k) = OPEN(i);
        newHigh(k) = HIGH(i);
        newLow(k) = LOW(i);
        newClose(k) = CLOSE(i);
        newVolume(k) = VOLUME(i);
        newAmt(k) = AMT(i);
        newTurn(k) = TURN(i);
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
        newAmt(k) = newAmt(k) + AMT(i);
        newTurn(k) = newTurn(k) + TURN(i);
    end
    
    StockData(i).date = newDate';
    StockData(i).open = newOpen';
    StockData(i).high = newHigh';
    StockData(i).low = newLow';
    StockData(i).close = newClose';
    StockData(i).volume = newVolume';
    StockData(i).amt = newAmt';
    StockData(i).turn = newTurn';
end

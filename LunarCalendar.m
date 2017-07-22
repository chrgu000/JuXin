function [month,day,solarterm]=LunarCalendar(Date)

y=str2num(datestr(Date,'yyyy'));
m=str2num(datestr(Date,'mm'));
d=str2num(datestr(Date,'dd'));
solarterm=25;
if nargin==0;
    cccc=clock;
    y=cccc(1);
    m=cccc(2);
    d=cccc(3);
end
Animals={'Mouse','Bull','Tiger','Rabbit','Dragon','Snake','Horse','Sheep','Monkey','Chook','Dog','Pig'};
solarTerm={'XiaoHan','DaHan','LiChun','YuShui','JingZhe','ChunFen','QingMing','GuYu','LiXia','XiaoMan','MangZhong','XiaZhi','XiaoShu','DaShu','LiQiu','ChuShu','BaiLu','QiuFen','HanLu','ShuangJiang','LiDong','XiaoXue','DaXue','DongZhi'};
switch m
    case 1
        Y=mod(y,100);
        if y>=2000
            C=5.4055;
        else
            C=6.11;
        end
        result=floor(Y*0.2422+C)-floor((Y-1)/4);
        if y==1982
            result=result+1;
        end
        if y==2019
            result=result-1;
        end
        if result==d
            solarterm=1;
        end
        if solarterm==25
            if y>=2000
                C=20.12;
            else
                C=20.84;
            end
            result=floor(Y*0.2422+C)-floor((Y-1)/4);
            if y==2082
                result=result+1;
            end
            if result==d
                solarterm=2;
            end
        end
    case 2
        Y=mod(y,100);
        if y>=2000
            C=3.87;
        else
            C=4.6295;
        end 
        result=floor(Y*0.2422+C)-floor((Y-1)/4);
        if result==d
            solarterm=3;
        end
        if solarterm==25
            if y>=2000
                C=18.73;
                result=floor(Y*0.2422+C)-floor((Y-1)/4);
                if y==2026
                    result=result-1;
                end
                if result==d
                    solarterm=4;
                end
            end
        end
    case 3
        Y=mod(y,100);
        if y>=2000
            C=5.63;
            result=floor(Y*0.2422+C)-floor(Y/4);
            if result==d
                solarterm=5;
            end
        end         
        if solarterm==25
            if y>=2000
                C=20.646;
                result=floor(Y*0.2422+C)-floor(Y/4);
                if y==2084
                    result=result+1;
                end
                if result==d
                    solarterm=6;
                end
            end
        end
    case 4
        Y=mod(y,100);
        if y>=2000
            C=4.81;
        else
            C=5.59;
        end
        result=floor(Y*0.2422+C)-floor(Y/4);
        if result==d
            solarterm=7;
        end
        if solarterm==25
            if y>=2000
                C=20.1;
            else
                C=20.888;
            end
            result=floor(Y*0.2422+C)-floor(Y/4);
            if result==d
                solarterm=8;
            end
        end
    case 5
        Y=mod(y,100);
        if y>=2000
            C=5.52;
        else
            C=6.318;
        end
        result=floor(Y*0.2422+C)-floor(Y/4);
        if y==1911
            result=result+1;
        end
        if result==d
            solarterm=9;
        end
        if solarterm==25
            if y>=2000
                C=21.04;
            else
                C=21.86;
            end
            result=floor(Y*0.2422+C)-floor(Y/4);
            if y==2008
                result=result+1;
            end
            if result==d
                solarterm=10;
            end
        end
    case 6
        Y=mod(y,100);
        if y>=2000
            C=5.678;
        else
            C=6.5;
        end
        result=floor(Y*0.2422+C)-floor(Y/4);
        if y==1902
            result=result+1;
        end
        if result==d
            solarterm=11;
        end
        if solarterm==25
            if y>=2000
                C=21.37;
            else
                C=22.2;
            end
            result=floor(Y*0.2422+C)-floor(Y/4);
            if result==d
                solarterm=12;
            end
        end
    case 7
        Y=mod(y,100);
        if y>=2000
            C=7.108;
        else
            C=7.928;
        end
        result=floor(Y*0.2422+C)-floor(Y/4);
        if y==1925 || y==2016
            result=result+1;
        end
        if result==d
            solarterm=13;
        end
        if solarterm==25
            if y>=2000
                C=22.83;
            else
                C=23.65;
            end
            result=floor(Y*0.2422+C)-floor(Y/4);
            if y==1922
                result=result+1;
            end
            if result==d
                solarterm=14;
            end
        end
    case 8
        Y=mod(y,100);
        if y>=2000
            C=7.5;
        else
            C=8.35;
        end
        result=floor(Y*0.2422+C)-floor(Y/4);
        if y==2002
            result=result+1;
        end
        if result==d
            solarterm=15;
        end
        if solarterm==25
            if y>=2000
                C=23.13;
            else
                C=23.95;
            end
            result=floor(Y*0.2422+C)-floor(Y/4);
            if result==d
                solarterm=16;
            end
        end
    case 9
        Y=mod(y,100);
        if y>=2000
            C=7.646;
        else
            C=8.44;
        end
        result=floor(Y*0.2422+C)-floor(Y/4);
        if y==1927
            result=result+1;
        end
        if result==d
            solarterm=17;
        end
        if solarterm==25
            if y>=2000
                C=23.042;
            else
                C=23.822;
            end
            result=floor(Y*0.2422+C)-floor(Y/4);
            if y==1942
                result=result+1;
            end
            if result==d
                solarterm=18;
            end
        end
    case 10
        Y=mod(y,100);
        if y>=2000
            C=8.318;
        else
            C=9.098;
        end
        result=floor(Y*0.2422+C)-floor(Y/4);
        if result==d
            solarterm=19;
        end
        if solarterm==25
            if y>=2000
                C=23.438;
            else
                C=24.218;
            end
            result=floor(Y*0.2422+C)-floor(Y/4);
            if y==2089
                result=result+1;
            end
            if result==d
                solarterm=20;
            end
        end
    case 11
        Y=mod(y,100);
        if y>=2000
            C=7.438;
        else
            C=8.218;
        end
        result=floor(Y*0.2422+C)-floor(Y/4);
        if y==2089
            result=result+1;
        end
        if result==d
            solarterm=21;
        end
        if solarterm==25
            if y>=2000
                C=22.36;
            else
                C=23.08;
            end
            result=floor(Y*0.2422+C)-floor(Y/4);
            if y==1978
                result=result+1;
            end
            if result==d
                solarterm=22;
            end
        end
    case 12
        Y=mod(y,100);
        if y>=2000
            C=7.18;
        else
            C=7.9;
        end
        result=floor(Y*0.2422+C)-floor(Y/4);
        if y==1954
            result=result+1;
        end
        if result==d
            solarterm=23;
        end
        if solarterm==25
            if y>=2000
                C=21.94;
            else
                C=22.6;
            end
            result=floor(Y*0.2422+C)-floor(Y/4);
            if y==1918 || y==2021
                result=result-1;
            end
            if result==d
                solarterm=24;
            end
        end
end

% CnDayStr={'1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'};
% CnMonthStr={'1','2','3','4','5','6','7','8','9','10','11','12'};
CnDayStr=[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30];
CnMonthStr=[1 2 3 4 5 6 7 8 9 10 11 12];

monthName={'JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'};
lunarInfo=[19416,19168,42352,21717,53856,55632,91476,22176,39632,21970,19168,42422,42192,53840,119381,46400,54944,44450,38320,84343,18800,42160,46261,27216,27968,109396,11104,38256,21234,18800,...
25958,54432,59984,28309,23248,11104,100067,37600,116951,51536,54432,120998,46416,22176,107956,9680,37584,53938,43344,46423,27808,46416,86869,19872,42448,83315,21200,43432,59728,27296,44710,43856,19296,43748,42352,21088,62051,55632,23383,22176,38608,19925,19152,42192,54484,53840,54616,46400,46496,103846,38320,18864,43380,42160,45690,27216,27968,44870,43872,38256,19189,18800,25776,29859,59984,27480,21952,43872,38613,37600,51552,55636,54432,55888,30034,22176,43959,9680,37584,51893,43344,46240,47780,44368,21977,19360,42416,86390,21168,43312,31060,27296,44368,23378,19296,42726,42208,53856,60005,54576,23200,30371,38608,19415,19152,42192,118966,53840,54560,56645,46496,22224,21938,18864,42359,42160,43600,111189,27936,44448];
lYearDays=[384,354,355,383,354,355,384,354,355,384,354,384,354,354,384,354,355,384,355,384,354,354,384,354,354,385,354,355,384,354,383,354,355,384,355,354,384,354,384,354,354,384,355,354,385,354,354,384,354,384,354,355,384,354,355,384,354,383,355,354,384,355,354,384,355,353,384,355,384,354,355,384,354,354,384,354,384,354,355,384,355,354,384,354,384,354,354,384,355,355,384,354,354,383,355,384,354,355,384,354,354,384,354,355,384,354,385,354,354,384,354,354,384,355,384,354,355,384,354,354,384,354,355,384,354,384,354,354,384,355,354,384,355,384,354,354,384,354,354,384,355,355,384,354,384,354,354,384,354,355];
leapDays=[29,0,0,29,0,0,30,0,0,29,0,29,0,0,30,0,0,29,0,30,0,0,29,0,0,30,0,0,29,0,29,0,0,29,0,0,30,0,30,0,0,30,0,0,30,0,0,29,0,29,0,0,30,0,0,30,0,29,0,0,29,0,0,29,0,0,29,0,29,0,0,29,0,0,29,0,29,0,0,30,0,0,29,0,29,0,0,29,0,0,29,0,0,29,0,29,0,0,29,0,0,29,0,0,29,0,29,0,0,29,0,0,29,0,29,0,0,30,0,0,29,0,0,29,0,29,0,0,29,0,0,29,0,29,0,0,30,0,0,29,0,0,29,0,29,0,0,30,0,0];
leapMonth=[8,0,0,5,0,0,4,0,0,2,0,6,0,0,5,0,0,2,0,7,0,0,5,0,0,4,0,0,2,0,6,0,0,5,0,0,3,0,7,0,0,6,0,0,4,0,0,2,0,7,0,0,5,0,0,3,0,8,0,0,6,0,0,4,0,0,3,0,7,0,0,5,0,0,4,0,8,0,0,6,0,0,4,0,10,0,0,6,0,0,5,0,0,3,0,8,0,0,5,0,0,4,0,0,2,0,7,0,0,5,0,0,4,0,9,0,0,6,0,0,4,0,0,2,0,6,0,0,5,0,0,3,0,7,0,0,6,0,0,5,0,0,2,0,7,0,0,5,0,0];

offset=datenum(y,m,d)-datenum(1900,1,31)+1; 
dayCyl=offset+40;
monCyl=14;

cumLYearDays=cumsum([0,lYearDays]);
LunarYear=find(offset>cumLYearDays);
LunarYear=LunarYear(end);
monCyl=monCyl+(LunarYear-1)*12;yearCyl=LunarYear+36;
offset=offset-cumLYearDays(LunarYear);
monthDays=[29,30];
monthDays=monthDays((bitand(lunarInfo(LunarYear),bitshift(65536,-(1:12)))~=0)+1);
leap=leapMonth(LunarYear);
if leap,
    monthDays=[monthDays(1:leap),leapDays(LunarYear),monthDays(leap+1:end)];
end
cumMonthDays=cumsum([0,monthDays]);
LunarMonth=find(offset>cumMonthDays);LunarMonth=LunarMonth(end);
offset=offset-cumMonthDays(LunarMonth);
ch_run_ch='';
if leap
    if LunarMonth==(leap+1),
        ch_run_ch='Run';
    end
    if (LunarMonth>leap),
        LunarMonth=LunarMonth-1;
    end
end
monCyl=monCyl+LunarMonth;


month=CnMonthStr(LunarMonth);
day=CnDayStr(offset);
% xx=['Lunar ',Animals{rem(yearCyl-1,12)+1},' Year ',ch_run_ch,CnMonthStr{LunarMonth},' Month ',CnDayStr{offset}];
% xx={xx;[cyclical(yearCyl),' Year ',cyclical(monCyl),' Month ',cyclical(dayCyl),'Day']};


end

    function ganzhi=cyclical(num)
        Gan={'Jia','Yi','Bing','Ding','Wu','Ji','Geng','Xin','Ren','Kui'};
        Zhi={'Zi','Chou','Yan','Mao','Chen','Si','Wu','Wei','Shen','You','Xu','Hai'};
        ganzhi=[Gan{rem(num-1,10)+1},Zhi{rem(num-1,12)+1}];
    end

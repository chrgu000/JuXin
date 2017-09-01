%注意:使用时，请将代码末尾处的Owner=w0814497修改成自己的账号，并将w.wupf函数使用的组合名称改成自己在PMS系统中创建的组合名称
%即代码末尾的 w.wupf('pmsbacktest',test_date,select_list,volume_list,price_list,'Owner=w0814497;Direction=Long;HedgeType=Spec;')

%启动API接口
w=windmatlab;
% 提取全部A股
wset_temp=w.wset('SectorConstituent','date=20150601;sectorId=a001010100000000') ;
stockList=wset_temp(:,2)
%获取调仓的日期序列
[w_tdays_data,w_tdays_codes,w_tdays_fields,w_tdays_times,w_tdays_errorid,w_tdays_reqid]=w.tdays('2015-02-01','2015-12-24','Period=M')

%回测策略，按调仓日期循环，对每一个周期进行选股
for i=1: length(w_tdays_data)
    disp(w_tdays_data(i))
    %获取当前调仓日期
    test_date=datestr(w_tdays_data(i),'yyyymmdd');
    [date_temp,~,~,~,w_tdays_errorid,~]=w.tdaysoffset(-1,w_tdays_data(i));
    pre_date=datestr(date_temp,'yyyymmdd');
    disp(pre_date)
    %策略部分，此处以一个简单策略为例
    %该策略选出前一天涨停，调仓当日开盘为涨停，并在调仓日有买入机会的股票，买入此类股票并持有到下一次调仓
    [w_wss_data1,~,~,~,w_wss_errorid1,~]=w.wss(stockList,'pct_chg','tradeDate',pre_date,'cycle=D');
    [w_wss_data2,~,~,~,w_wss_errorid2,~]=w.wss(stockList,'swing,vwap','tradeDate',test_date,'cycle=D');
    
    select_list={}; %存放选出的股票
    price_list={}; %存放对应的成交均价
    volume_list={}; %存放对应的持股数量
    for j=1: length(stockList)
        % 调仓日前一天涨跌幅大于9.9%则判断为涨停，调仓日的振幅大于1%则判断为有买入机会. 最多满足此条件的20只股票
        if(~isempty(w_wss_data1(j)) && ~isempty(w_wss_data2(j,1)))
            if(w_wss_data1(j)>9.9) && (w_wss_data2(j,1)>1.0)
                if(length(select_list)>=20)
                    %如果已经选出20只股票了，那么久不再继续选股
                    break;
                end
                select_list(length(select_list)+1)=stockList(j);
                price_list(length(price_list)+1)={w_wss_data2(j,2)};
                volume_list(length(volume_list)+1)={1000};
            end
        end
    end
    %通过wupf函数上传次调仓周期的持仓
    %注意日期格式必须转换成类似20151224这种格式
    if(~isempty(select_list))
        w.wupf('pmsbacktest',test_date,select_list,volume_list,price_list,'Owner=w0814497;Direction=Long;HedgeType=Spec;')
    end
end




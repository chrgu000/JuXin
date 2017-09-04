#Re=[]
#fig=5
#dateAll=[]
#for i2 in range(15,len(dates)):
#    if closes[i2-1]<lows[i2-1]+(highs[i2-1]-lows[i2-1])/4  and closes[i2]>lows[i2]+(highs[i2]-lows[i2])*3/4  and \
#    highs[i2-3]>lows[i2-3] and highs[i2-2]>lows[i2-2]and highs[i2-1]>lows[i2-1]and highs[i2]>lows[i2] and closes[i2]/closes[i2-1]<1.095: #vols[i2-2:i2].min()>vols[[i2-3,i2]].max() and 
#        if closes[i2+1]>closes[i2]:
#            Re.append(closes[i2+2]/closes[i2]-1)
#            if fig>0:
#                figx=[i2,i2+2]
#                figy=[closes[i2],closes[i2+2]]
#        else:
#            Re.append(closes[i2+1]/closes[i2]-1)
#            if fig>0:
#                figx=[i2,i2+1]
#                figy=[closes[i2],closes[i2+1]]
#        dateAll.append(dates[i2])
#        max5near=max(closes[i2-4:i2+1]);max5far=max(closes[i2-9:i2-4]);
#        min5near=min(closes[i2-4:i2+1]);min5far=min(closes[i2-9:i2-4]);
#        max_7near=max(highs[i2-6:i2+1]);max_7far=max(highs[i2-13:i2-6]);
#        min_7near=min(lows[i2-6:i2+1]);min_7far=min(lows[i2-13:i2-6]);
#        if max5near>max5far and min5near>min5far:
#            ud5=1
#        elif max5near<max5far and min5near<min5far:
#            ud5=-1
#        else:
#            ud5=0
#        if max_7near>max_7far and min_7near>min_7far:
#            ud_7=1
#        elif max_7near<max_7far and min_7near<min_7far:
#            ud_7=-1
#        else:
#            ud_7=0                                                       
#        tem=[ opens[i2]/highs[i2-1],\
#             lows[i2]/highs[i2-1],\
#             min5near/min5far,\
#             closes[i2-4:i2].mean()/closes[i2-9:i2].mean(),\
#             max5near/max5far,\
#             highs[i2-4:i2].mean()/highs[i2-9:i2].mean(),\
#             lows[i2]/opens[i2-1],\
#             highs[i2]/highs[i2-1],\
#             lows[i2]/lows[i2-1],\
#             lows[i2]/closes[i2-1],\
#             (vols[i2]+vols[i2-1])/(vols[i2-3]+vols[i2-2]),\
#             vols[i2-1]/vols[i2-2],\
#             vols[i2]/vols[i2-2],\
#             closes[i2-4:i2].std()/closes[i2-9:i2].std(),\
#             highs[i2]/closes[i2-1],\
#             ud_7,\
#             opens[i2]/closes[i2-1],\
#             vols[i2-1]/vols[i2-3],\
#             highs[i2]/lows[i2-1],\
#             vols[i2]/vols[i2-3],\
#             closes[i2]/np.mean(opens[i2-4:i2]),\
#             pd.DataFrame([lows[i2-3],opens[i2-3],closes[i2-3],highs[i2-3]])[0].corr(pd.DataFrame([lows[i2],closes[i2],opens[i2],highs[i2]])[0]),\
#             vols[i2]/vols[i2-1],\
#             highs[i2-4:i2].std()/highs[i2-9:i2].std(),\
#             vols[i2-2]/vols[i2-3],\
#             np.std([ closes[i2],opens[i2],highs[i2],lows[i2] ])/np.std([closes[i2-1],opens[i2-1],highs[i2-1],lows[i2-1]]),\
#             closes[i2]/closes[i2-1],\
#             opens[i2]/lows[i2-1],\
#             highs[i2]/opens[i2-1] ] 
#        if np.isnan(tem).sum():
#            continue
#        if fig>0:
#            fig=fig-1
plt.figure()
#
candleData=[]
for i3 in range(i2-10,i2+3):
    tem=(date2num(dates[i3]),opens[i3],highs[i3],lows[i3],closes[i3])
    candleData.append(tem)
ax=plt.subplot(1,2,1)
ax.xaxis_date()
plt.xticks(rotation=45)
plt.yticks()
plt.title(stocks[i][0])
plt.xlabel('Date')
plt.ylabel('Price')
mpf.candlestick_ohlc(ax,candleData,width=0.8,colorup='r',colordown='g')
ax=plt.subplot(1,2,2)
ax.plot(figx,figy,color='r',linewidth='2')
plt.grid() 

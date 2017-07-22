function op=HMMpy(matrix) % related to Python procedure:hmmMatlab;matrix:current close;close one trading-day ago;close 5 trading-days ago;current high;current low;
dlmwrite('D:\Trading\hmmMatlabIn.txt',matrix,'delimiter',',','precision','%.5f','newline','pc');
system('python D:\Trading\Python\machinelearning\hmmMatlab.py D:\Trading\hmmMatlabIn.txt D:\Trading\hmmMatlabOut.txt');
op=importdata('D:\Trading\hmmMatlabOut.txt');
end
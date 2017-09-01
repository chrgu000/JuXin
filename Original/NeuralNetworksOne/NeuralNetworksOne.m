%% Initialization
clear ; close all; clc

%% Setup the parameters you will use for this part of the exercise
input_layer_size  = 6;  % 20x20 Input Images of Digits
num_labels = 2;          % 10 labels, from 1 to 10   
                          % (note that we have mapped "0" to label 10)

%% =========== Part 1: Loading and Visualizing Data =============
%  We start the exercise by first loading and visualizing the dataset. 
%  You will be working with a dataset that contains handwritten digits.
%

% Load Training Data
fprintf('Loading Data ...\n')
dataXy=dlmread('dataML.txt');
X=dataXy(:,1:6);
% tem=size(X,1);
% Xmean=mean(X);
% Xstd=std(X);
% X=(X-repmat(Xmean,tem,1))./repmat(Xstd,tem,1);
y=dataXy(:,7)+1;

tem=size(X,1);
Xind=randperm(tem);
X0=X(Xind(1:ceil(tem*0.8)),:);
X1=X(Xind(ceil(tem*0.8):end),:);
y0=y(Xind(1:ceil(tem*0.8)));
y1=y(Xind(ceil(tem*0.8):end));

%% ============ Part 2: Vectorize Logistic Regression ============
%  In this part of the exercise, you will reuse your logistic regression
%  code from the last exercise. You task here is to make sure that your
%  regularized logistic regression implementation is vectorized. After
%  that, you will implement one-vs-all classification for the handwritten
%  digit dataset.
%

lambda = 0.1;
[all_theta] = oneVsAll(X0, y0, num_labels, lambda);
save all_theta all_theta

%% ================ Part 3: Predict for One-Vs-All ================
%  After ...
[~,pred]= predictOneVsAll(all_theta, X0);
fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y0)) * 100);

[~,pred]= predictOneVsAll(all_theta, X1);
fprintf('\nTesting Set Accuracy: %f\n', mean(double(pred == y1)) * 100);



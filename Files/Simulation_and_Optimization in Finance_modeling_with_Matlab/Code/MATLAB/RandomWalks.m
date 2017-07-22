%Copyright © 2010 John Wiley & Sons, Inc., Dessislava A. Pachamanova, and Frank J. Fabozzi.
%All rights reserved.

%Model files and code may be copied and used only by owners of the book Simulation and Optimization in Finance: Modeling with MATLAB, @RISK or VBA, by Dessislava A. Pachamanova and Frank J. Fabozzi, Hoboken, NJ: John Wiley & Sons, 2010 and only for their own personal use.  Copying and/or use for any other purpose or by any other person is prohibited. Requests for permission for other uses should be addressed to the Permissions Department, John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 07030, (201) 748-6011, fax (201) 748-6008, or online at http://www.wiley.com/go/permissions.

%While the authors and publisher have used all reasonable efforts in creating the work, the model files and the code, they make no representations or warranties with respect to the accuracy or completeness of the contents thereof, and specifically disclaim any implied warranties of merchantability or fitness for a particular purpose.  No warranty may be created or extended by sales representatives or written sales materials.  The advice and strategies contained herein may not be suitable for a particular party’s situation.  Users should consult with a professional where appropriate.  

%LIMITATION OF LIABILITY

%IN NO EVENT SHALL THE AUTHOR OR THE PUBLISHER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE WORK, THE MODEL FILES OR THE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

%read in data
%data for arithmetic and geometric random walks
ExxonPriceData = xlsread('Ch12-RandomWalks.xlsx','ARW','b4:b107');
[numObsRW,nn] = size(ExxonPriceData); 

%data for mean reversion and geometric mean reversion
USEuroRateData = xlsread('Ch12-RandomWalks.xlsx','MR','b4:b107');
[numObsMR,nn] = size(USEuroRateData);

%ARITHMETIC RANDOM WALK

%create a vector of price changes
priceChangesARW = zeros(numObsRW-1,1);

for iObs = 1:numObsRW-1
    priceChangesARW(iObs,:) =  ExxonPriceData(iObs+1)-ExxonPriceData(iObs);
end

%estimate parameters
muARW = mean(priceChangesARW);
sigmaARW = std(priceChangesARW);

%convert the estimated drift and volatility to annual values
%since the data for estimation were weekly, multiply by 52 (weeks in a year)
muARW = muARW*52;
sigmaARW = sigmaARW*sqrt(52);

%simulate a path for the arithmetic random walk
ARWPaths(ExxonPriceData(numObsRW,1),muARW,sigmaARW,20/52,20,1);

%GEOMETRIC RANDOM WALK

%create a vector of ln(S_(t+1)/S_t)
priceRatiosGRW = zeros(numObsRW-1,1);

for iObs = 1:numObsRW-1
    priceRatiosGRW(iObs,:) = log(ExxonPriceData(iObs+1)/ExxonPriceData(iObs));
end

%estimate parameters
sigmaGRW = std(priceRatiosGRW);
muGRW = mean(priceRatiosGRW)+0.5*sigmaGRW^2;

%convert the estimated drift and volatility to annual values
%since the data for estimation were weekly, multiply by 52 (weeks in a year)
muGRW = muGRW*52;
sigmaGRW = sigmaGRW*sqrt(52);

%simulate a path for the geometric random walk
GRWPaths(ExxonPriceData(numObsRW,1),muGRW,sigmaGRW,20/52,20,1);

%MEAN REVERSION

%create a vector of price changes
priceChangesMR = zeros(numObsMR-1,1);

for iObs = 1:numObsMR-1
    priceChangesMR(iObs,:) =  USEuroRateData(iObs+1)-USEuroRateData(iObs);
end

%estimate parameters

[bMR,nn,nn,nn,statsMR] = regress(priceChangesMR,[ones(numObsMR-1,1),USEuroRateData(1:(numObsMR-1),1)])

interceptMR = bMR(1);
slopeMR = bMR(2);
if (slopeMR > 0)
    error('Cannot use mean reversion: slope positive.');
end

%the fourth element of stats should be the variance of errors in the regression
sigmaMR = sqrt(statsMR(4));
kappaMR = -slopeMR; 
muMR = -interceptMR/slopeMR;

%convert the estimated drift and volatility to annual values
%since the data for estimation were weekly, multiply by 52 (weeks in a year)
muMR = muMR*52;
sigmaMR = sigmaMR*sqrt(52);

%simulate a path for the mean reverting walk
MRPaths(USEuroRateData(numObsMR,1),muMR,sigmaMR,kappaMR,20/52,20,1);

%GEOMETRIC MEAN REVERSION

%create a vector of percentage changes
percentageChangesGMR = zeros(numObsMR-1,1);

for iObs = 1:numObsMR-1
    percentageChangesGMR(iObs,:) =  (USEuroRateData(iObs+1)-USEuroRateData(iObs))/USEuroRateData(iObs);
end

%estimate parameters

[bGMR,nn,nn,nn,statsGMR] = regress(percentageChangesGMR,[ones(numObsMR-1,1),USEuroRateData(1:(numObsMR-1),1)])

interceptGMR = bGMR(1);
slopeGMR = bGMR(2);
if (slopeGMR > 0)
    error('Cannot use geometric mean reversion: slope positive.');
end

%the fourth element of stats should be the variance of errors in the regression
sigmaGMR = sqrt(statsGMR(4));
kappaGMR = -slopeGMR; 
muGMR = -interceptGMR/slopeGMR;

%convert the estimated drift and volatility to annual values
%since the data for estimation were weekly, multiply by 52 (weeks in a year)
muGMR = muGMR*52;
sigmaGMR = sigmaGMR*sqrt(52);

%simulate a path for the mean reverting walk
GMRPaths(USEuroRateData(numObsMR,1),muGMR,sigmaGMR,kappaGMR,20/52,20,1);

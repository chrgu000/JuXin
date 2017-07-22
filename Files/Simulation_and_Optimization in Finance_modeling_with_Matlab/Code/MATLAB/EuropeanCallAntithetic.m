function CEPrice =  EuropeanCallAntithetic(initPrice,K,r,T,sigma,q,numPaths)
%function for evaluating the price of a European option using
%antithetic variables
%Asset price assumed to follow a geometric random walk
%initPrice is the initial price, K is the strike price
%r is the annual interest rate, T is the time to maturity, sigma is the
%annual volatility
%q is the continuous dividend yield
%numPaths is the number of scenarios to generate for the evaluation 

%Copyright © 2010 John Wiley & Sons, Inc., Dessislava A. Pachamanova, and Frank J. Fabozzi.
%All rights reserved.

%Model files and code may be copied and used only by owners of the book Simulation and Optimization in Finance: Modeling with MATLAB, @RISK or VBA, by Dessislava A. Pachamanova and Frank J. Fabozzi, Hoboken, NJ: John Wiley & Sons, 2010 and only for their own personal use.  Copying and/or use for any other purpose or by any other person is prohibited. Requests for permission for other uses should be addressed to the Permissions Department, John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 07030, (201) 748-6011, fax (201) 748-6008, or online at http://www.wiley.com/go/permissions.

%While the authors and publisher have used all reasonable efforts in creating the work, the model files and the code, they make no representations or warranties with respect to the accuracy or completeness of the contents thereof, and specifically disclaim any implied warranties of merchantability or fitness for a particular purpose.  No warranty may be created or extended by sales representatives or written sales materials.  The advice and strategies contained herein may not be suitable for a particular party’s situation.  Users should consult with a professional where appropriate.  

%LIMITATION OF LIABILITY

%IN NO EVENT SHALL THE AUTHOR OR THE PUBLISHER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE WORK, THE MODEL FILES OR THE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

payoffsOrig = zeros(numPaths,1); %payoffs with originally generated random numbers
payoffsAnt = zeros(numPaths,1); %payoffs with antithetic variables
randNumOrig = zeros(numPaths,1); %normal random numbers generated for each scenario
randNumAnt = zeros(numPaths,1); %antithetic of normal random numbers generated for each scenario
payoffs = zeros(numPaths,1); %averaged out payoffs

%generate an array of normal random numbers with dimensions [numPaths,1]
randNumOrig = normrnd(0,1,numPaths,1);

%generate antithetic variables
randNumAnt = -randNumOrig;

for iPath = 1:numPaths
    finalPriceOrig = initPrice*exp((r-q-0.5*sigma^2)*T+sigma*sqrt(T)*randNumOrig(iPath));
    payoffsOrig(iPath) = exp(-r*T)*max(finalPriceOrig - K,0);
    finalPriceAnt = initPrice*exp((r-q-0.5*sigma^2)*T+sigma*sqrt(T)*randNumAnt(iPath));
    payoffsAnt(iPath) = exp(-r*T)*max(finalPriceAnt - K,0);
    payoffs(iPath) = (payoffsOrig(iPath) + payoffsAnt(iPath))/2;
end

CEPrice = mean(payoffs);





%Copyright ?2010 John Wiley & Sons, Inc., Dessislava A. Pachamanova, and Frank J. Fabozzi.
%All rights reserved.

%Model files and code may be copied and used only by owners of the book Simulation and Optimization in Finance: Modeling with MATLAB, @RISK or VBA, by Dessislava A. Pachamanova and Frank J. Fabozzi, Hoboken, NJ: John Wiley & Sons, 2010 and only for their own personal use.  Copying and/or use for any other purpose or by any other person is prohibited. Requests for permission for other uses should be addressed to the Permissions Department, John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 07030, (201) 748-6011, fax (201) 748-6008, or online at http://www.wiley.com/go/permissions.

%While the authors and publisher have used all reasonable efforts in creating the work, the model files and the code, they make no representations or warranties with respect to the accuracy or completeness of the contents thereof, and specifically disclaim any implied warranties of merchantability or fitness for a particular purpose.  No warranty may be created or extended by sales representatives or written sales materials.  The advice and strategies contained herein may not be suitable for a particular party’s situation.  Users should consult with a professional where appropriate.  

%LIMITATION OF LIABILITY

%IN NO EVENT SHALL THE AUTHOR OR THE PUBLISHER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE WORK, THE MODEL FILES OR THE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

numAssets = 2;
expectedReturns =  [9.1; 12.1;13.2]; 
stdDeviations = [16.5; 15.8;1];
corr = -0.22;
covMx = [stdDeviations(1)^2, corr*stdDeviations(1)*stdDeviations(2); 
        corr*stdDeviations(1)*stdDeviations(2), stdDeviations(2)^2];

targetReturn = 11;

%SINGLE OPTIMIZATION

%create the matrix X
H = 2*covMx;

%create a vector of length numAssets with zeros
f = zeros(numAssets,1); 

%create right hand and left hand side of inequality constraints 
A = -transpose(expectedReturns);
b = -targetReturn;

%create lower bounds array for asset weights (negative infinity)
lb = -inf*ones(numAssets,1);

%create upper bounds array for asset weights (infinity)
ub = inf*ones(numAssets,1);

%create right hand and left hand side of equality constraints
beq = [1];
Aeq = (ones(numAssets,1));

[weights,variance] = quadprog(H,f,A,b,Aeq,beq,lb,ub);

%print results to screen
stdDev = sqrt(variance)
weights

%EFFICIENT FRONTIER
%loop through different values of the target portfolio returns, compute the optimal 
%portfolio standard deviation, and plot the efficient frontier

iCounter = 1;

for iTRet = 9.5:0.5:12 
    b = -iTRet;
    [weights,variance] = quadprog(H,f,A,b,Aeq,beq,lb,ub);
    y(iCounter) = iTRet;
    x(iCounter) = sqrt(variance);
    iCounter = iCounter + 1;
end

%plot efficient frontier
plot(x,y);
xlabel('Portfolio standard deviation');
ylabel('Portfolio expected return');
title('Efficient Frontier');

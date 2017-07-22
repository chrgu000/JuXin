%sample portfolio CVaR optimization

%Copyright © 2010 John Wiley & Sons, Inc., Dessislava A. Pachamanova, and Frank J. Fabozzi.
%All rights reserved.

%Model files and code may be copied and used only by owners of the book Simulation and Optimization in Finance: Modeling with MATLAB, @RISK or VBA, by Dessislava A. Pachamanova and Frank J. Fabozzi, Hoboken, NJ: John Wiley & Sons, 2010 and only for their own personal use.  Copying and/or use for any other purpose or by any other person is prohibited. Requests for permission for other uses should be addressed to the Permissions Department, John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 07030, (201) 748-6011, fax (201) 748-6008, or online at http://www.wiley.com/go/permissions.

%While the authors and publisher have used all reasonable efforts in creating the work, the model files and the code, they make no representations or warranties with respect to the accuracy or completeness of the contents thereof, and specifically disclaim any implied warranties of merchantability or fitness for a particular purpose.  No warranty may be created or extended by sales representatives or written sales materials.  The advice and strategies contained herein may not be suitable for a particular party’s situation.  Users should consult with a professional where appropriate.  

%LIMITATION OF LIABILITY

%IN NO EVENT SHALL THE AUTHOR OR THE PUBLISHER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE WORK, THE MODEL FILES OR THE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

%input data
epsilon = 0.05;
returnsData = xlsread('Ch8-VaRCVaROpt.xlsx','CVaR','B10:D69');
[numObservations,numAssets] = size(returnsData);

K = floor(epsilon*numObservations); %to determine the number of observations in the tail

weights = zeros(numAssets,1);
xi = 0;
yVec = zeros(numObservations,1);

x = [weights; xi; yVec];

%set up the optimization problem
f = [zeros(numAssets,1); 1; (1/K)*ones(numObservations,1)];

A = [-returnsData -ones(numObservations,1) -1*eye(numObservations,numObservations)];
b = zeros(numObservations,1);

Aeq = [ones(1,numAssets) 0 zeros(1,numObservations)];
beq = [1];

lb = [-inf*ones(numAssets,1); -inf; zeros(numObservations,1)];
ub = inf*ones(1, numAssets + 1 + numObservations);

%solve the CVaR linear optimization problem with the function linprog
[x,fval] = linprog(f,A,b,Aeq,beq,lb,ub);

%print output
weights = x(1:numAssets)
CVaR = fval

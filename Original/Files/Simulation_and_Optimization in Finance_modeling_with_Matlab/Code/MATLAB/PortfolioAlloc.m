numAssets = 4;
expReturnsVec = [0.2069 0.0587 0.1052 0.0243]';
%create placeholders for an array of decision variables (amounts to invest
%in each fund) and the optimal portfolio expected return (to be filled out
%after the optimization)
amountsVec = zeros(numAssets,1);
optReturn = [];

%vector of coefficients of objective function f
%since MATLAB expects minimization (and we are maximizing), take the
%negative of the function we are trying to maximize
f = -expReturnsVec;

%A, matrix of coefficients in constraints with inequalities so that Ax<=b
A = [1 0 1 0;
    4 2 2 1;
    1 0 0 0;
    0 1 0 0;
    0 0 1 0;
    0 0 0 1];

%b
b = [6000000 20000000 4000000 4000000 4000000 4000000]';

%Aeq, matrix of coefficients in constraints with equalities so that
%Aeq*x=beq

Aeq = ones(1,numAssets);

%beq

beq = 10000000;

%lower bounds: nonnegativity requires that all decision variables are >= 0

lb = zeros(numAssets,1);

%upper bounds can be left infinite (although, technically, we cannot invest
%more than the $10m we have available)
ub = inf*ones(numAssets,1);

[amountsVec,optReturn] = linprog(f,A,b,Aeq,beq,lb,ub);

format('bank');

amountsVec
%revert to correct number for maximum return
optReturn = -optReturn

%Copyright © 2010 John Wiley & Sons, Inc., Dessislava A. Pachamanova, and Frank J. Fabozzi.
%All rights reserved.

%Model files and code may be copied and used only by owners of the book Simulation and Optimization in Finance: Modeling with MATLAB, @RISK or VBA, by Dessislava A. Pachamanova and Frank J. Fabozzi, Hoboken, NJ: John Wiley & Sons, 2010 and only for their own personal use.  Copying and/or use for any other purpose or by any other person is prohibited. Requests for permission for other uses should be addressed to the Permissions Department, John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 07030, (201) 748-6011, fax (201) 748-6008, or online at http://www.wiley.com/go/permissions.

%While the authors and publisher have used all reasonable efforts in creating the work, the model files and the code, they make no representations or warranties with respect to the accuracy or completeness of the contents thereof, and specifically disclaim any implied warranties of merchantability or fitness for a particular purpose.  No warranty may be created or extended by sales representatives or written sales materials.  The advice and strategies contained herein may not be suitable for a particular party’s situation.  Users should consult with a professional where appropriate.  

%LIMITATION OF LIABILITY

%IN NO EVENT SHALL THE AUTHOR OR THE PUBLISHER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE WORK, THE MODEL FILES OR THE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.




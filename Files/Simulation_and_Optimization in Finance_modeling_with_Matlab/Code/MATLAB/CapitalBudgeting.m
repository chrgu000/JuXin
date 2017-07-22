%x = bintprog(f,A,b,Aeq,beq)
%All numbers are in thousands of dollars
%MATLAB assumes that all variables are binary automatically when using
%bintprog

numProjects = 8;
expBenefitsVec = [950.00 780.00	440.00	215.00	630.00	490.00	560.00	600.00]';
%create placeholders for an array of decision variables (binary variables
%deciding whether to invest or not)
%and the optimal total benefits (to be filled out after the optimization)
fundBin = zeros(numAssets,1);
optBenefits = [];

%vector of coefficients of objective function f
%since MATLAB expects minimization (and we are maximizing), take the
%negative of the function we are trying to maximize
f = -expBenefitsVec;

%A, matrix of coefficients in constraints with inequalities so that Ax<=b
A = [400.00	350.00	200.00	100.00	300.00	250.00	300.00	350.00];
    
%b
b = [1000]';

%There are no equality constraints, so no need to declare these matrices Aeq*x=beq
Aeq = [];
beq = [];

[fundBin,optBenefits] = bintprog(f,A,b,Aeq,beq);
fundBin
%revert to correct number for maximum return
optBenefits = -optBenefits

%PART II: Incorporate constraint that if Pr. 1 is funded, then Pr. 8 must
%be funded too. 
%The only difference is in the specification of the matrices A and b in the inequality constraints.

A = [400.00	350.00	200.00	100.00	300.00	250.00	300.00	350.00;
    1 0 0 0 0 0 0 -1];
b = [1000 0]';

[fundBin,optBenefits] = bintprog(f,A,b,Aeq,beq);
fundBin
%revert to correct number for maximum return
optBenefits = -optBenefits

%PART III: Add constraint that Pr. 4 and 5 cannot be funded at the same
%time. Again, only A and b change

A = [400.00	350.00	200.00	100.00	300.00	250.00	300.00	350.00;
    1 0 0 0 0 0 0 -1;
    0 0 0 1 1 0 0 0];
b = [1000 0 1]';

[fundBin,optBenefits] = bintprog(f,A,b,Aeq,beq);
fundBin
%revert to correct number for maximum return
optBenefits = -optBenefits

%Copyright © 2010 John Wiley & Sons, Inc., Dessislava A. Pachamanova, and Frank J. Fabozzi.
%All rights reserved.

%Model files and code may be copied and used only by owners of the book Simulation and Optimization in Finance: Modeling with MATLAB, @RISK or VBA, by Dessislava A. Pachamanova and Frank J. Fabozzi, Hoboken, NJ: John Wiley & Sons, 2010 and only for their own personal use.  Copying and/or use for any other purpose or by any other person is prohibited. Requests for permission for other uses should be addressed to the Permissions Department, John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 07030, (201) 748-6011, fax (201) 748-6008, or online at http://www.wiley.com/go/permissions.

%While the authors and publisher have used all reasonable efforts in creating the work, the model files and the code, they make no representations or warranties with respect to the accuracy or completeness of the contents thereof, and specifically disclaim any implied warranties of merchantability or fitness for a particular purpose.  No warranty may be created or extended by sales representatives or written sales materials.  The advice and strategies contained herein may not be suitable for a particular party’s situation.  Users should consult with a professional where appropriate.  

%LIMITATION OF LIABILITY

%IN NO EVENT SHALL THE AUTHOR OR THE PUBLISHER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE WORK, THE MODEL FILES OR THE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

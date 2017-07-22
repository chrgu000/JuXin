function paths=GMRPaths(initPrice,mu,sigma,speed,T,numSteps,numPaths)
    %computes numPaths random paths for a geometric mean reversion process
    %mu is the annual drift, sigma the annual volatility
    %speed is the speed of adjustment (kappa)
    %T is the total length of time for the path (in years)
    %dT is the time increment (in years)
 
    %Copyright © 2010 John Wiley & Sons, Inc., Dessislava A. Pachamanova, and Frank J. Fabozzi.
%All rights reserved.

%Model files and code may be copied and used only by owners of the book Simulation and Optimization in Finance: Modeling with MATLAB, @RISK or VBA, by Dessislava A. Pachamanova and Frank J. Fabozzi, Hoboken, NJ: John Wiley & Sons, 2010 and only for their own personal use.  Copying and/or use for any other purpose or by any other person is prohibited. Requests for permission for other uses should be addressed to the Permissions Department, John Wiley & Sons, Inc., 111 River Street, Hoboken, NJ 07030, (201) 748-6011, fax (201) 748-6008, or online at http://www.wiley.com/go/permissions.

%While the authors and publisher have used all reasonable efforts in creating the work, the model files and the code, they make no representations or warranties with respect to the accuracy or completeness of the contents thereof, and specifically disclaim any implied warranties of merchantability or fitness for a particular purpose.  No warranty may be created or extended by sales representatives or written sales materials.  The advice and strategies contained herein may not be suitable for a particular party’s situation.  Users should consult with a professional where appropriate.  

%LIMITATION OF LIABILITY

%IN NO EVENT SHALL THE AUTHOR OR THE PUBLISHER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE WORK, THE MODEL FILES OR THE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    
    paths = zeros(numSteps+1,numPaths);
    dT = T/numSteps; 
    %the vector of paths will store realizations of the asset price. 
    %the first asset price is, of course, the initial price
    paths(1,:) = initPrice;
    figure;
    for iPath = 1:numPaths
        for iStep = 1:numSteps
            paths(iStep+1,iPath) = paths(iStep,iPath) + speed*(mu*dT - paths(iStep,iPath))*paths(iStep,iPath) +...
                sigma*paths(iStep,iPath)*sqrt(dT)*normrnd(0,1);
        end
        plot(0:numSteps,(paths(:,iPath))');
        hold on;
    end 
end
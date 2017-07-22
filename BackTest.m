function varargout = BackTest(varargin)
% BACKTEST MATLAB code for BackTest.fig
%      BACKTEST, by itself, creates a new BACKTEST or raises the existing
%      singleton*.
%
%      H = BACKTEST returns the handle to a new BACKTEST or the handle to
%      the existing singleton*.
%
%      BACKTEST('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in BACKTEST.M with the given input arguments.
%
%      BACKTEST('Property','Value',...) creates a new BACKTEST or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before BackTest_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to BackTest_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help BackTest

% Last Modified by GUIDE v2.5 29-Nov-2015 20:33:28

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @BackTest_OpeningFcn, ...
                   'gui_OutputFcn',  @BackTest_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before BackTest is made visible.
function BackTest_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to BackTest (see VARARGIN)

% Choose default command line output for BackTest
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes BackTest wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = BackTest_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global date open high low close vol sum1;
NameS=get(handles.edit1,'String');
if NameS(1)=='S' || NameS(1)=='s'
else
   if NameS(1)=='6'
       NameS=strcat('SH',NameS);
   else
       NameS=strcat('SZ',NameS);
   end
end
    name_f=strcat('E:\360Synchronization\360Synchronization\MatLab\DataFromZX\',NameS,'.txt');
    [date,open,high,low,close,vol,sum1]=textread(name_f,'%s %f %f %f %f %d %d','headerlines',2);  
    date(2:2:end)=[];date(end)=[]; % delete all needless 0s.
    open(2:2:end)=[];open(end)=[];
    high(2:2:end)=[];high(end)=[];
    low(2:2:end)=[];low(end)=[];
    close(2:2:end)=[];close(end)=[];
    vol(2:2:end)=[];vol(end)=[];
    h1=figure;

% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double


% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global open high low close;
figure(1);
subplot(3,1,[1 2]);
candle(high,low,close,open);

% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
figure(1);
subplot(3,1,3);
global close;
MACD(close);


% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

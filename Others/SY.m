function varargout = SY(varargin)
% SY MATLAB code for SY.fig
%      SY, by itself, creates a new SY or raises the existing
%      singleton*.
%
%      H = SY returns the handle to a new SY or the handle to
%      the existing singleton*.
%
%      SY('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in SY.M with the given input arguments.
%
%      SY('Property','Value',...) creates a new SY or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before SY_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to SY_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help SY

% Last Modified by GUIDE v2.5 06-Aug-2015 20:29:59

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @SY_OpeningFcn, ...
                   'gui_OutputFcn',  @SY_OutputFcn, ...
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

% --- Executes just before SY is made visible.
function SY_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to SY (see VARARGIN)

% Choose default command line output for SY
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes SY wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = SY_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global f;
[filename,pathname]=uigetfile('*.xls','select the excel file');
f=fullfile(pathname,filename);

% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global f;
x=xlsread(f);
y=x<=50;
x(y)=nan;
[filename,pathname]=uigetfile('*.xls','Please create an Excel file!');
if filename==0
    warndlg('Failed to create an Excel file, please again!');
else
    xlswrite(fullfile(pathname,filename),x);
end



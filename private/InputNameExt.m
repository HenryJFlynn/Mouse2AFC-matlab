function Params = InputNameExt(StackDepth)
% Ugly hack taken to get input variable name when it's part of a struct.
% Original code ripped form:
% https://stackoverflow.com/questions/35943676/workaround-equivalent-of-inputname-to-return-structure-name
% NOTICE: THIS WILL ONLY WORK IF THE CALLING FUNCTION IS ONLY ON ONE LINE
if ~exist('StackDepth','var')
     StackDepth = 2;
end
if StackDepth > 1
    [ST, I] = dbstack('-completenames', StackDepth-1);
else
    [ST, I] = dbstack('-completenames', StackDepth);
end
Params = {};
if numel(ST)> 0
    if numel(ST)> 1 && StackDepth > 1
        callingFunctionName = ST(1).name;
        ST = ST(2:end);
    else
        callingFunctionName = '';
    end
    fid=fopen(ST(1).file,'r');
    for ix=2:ST(1).line;fgetl(fid);end
    codeline=fgetl(fid);
    fclose(fid);
    fprintf('function was called with line %s\n',codeline);
    fprintf('calling function name %s\n',callingFunctionName);
    if numel(callingFunctionName) > 0
        funcStart = strfind(codeline, callingFunctionName);
        funcStart = funcStart(1);
        fprintf('Function start %d\n', funcStart  + numel(callingFunctionName));
        codeline = codeline(funcStart + numel(callingFunctionName):end);
    end
    startParenth = strfind(codeline, '('); startParenth = startParenth(1);
    codeline = codeline(startParenth+1:end);
    endParenth = strfind(codeline, ')');
    codeline = codeline(1:endParenth-1);
    fprintf('First parenthesis index %s\n', codeline);
    splittedParams = strsplit(codeline, ',');
    Params = strings(1,numel(splittedParams)); % Preallocate
    i = 1;
    for param=splittedParams
        Params(1) = strip(param);
        i = i + 1;
    end
end
end
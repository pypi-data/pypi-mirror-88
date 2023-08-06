define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    // Numpy 패키지용 import 라이브러리
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeGenerator/parent/NumpyCodeGenerator'
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi'
], function(requirejs, sb, 
            NumpyCodeGenerator,
            numpyStateApi) {
    "use strict";
    var sbCode = new sb.StringBuilder();
    var { fixNumpyParameterValue } = numpyStateApi;

    /**
     * @class NpArrayCodeGenerator
     * @constructor
    */
    var NpArrayCodeGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    NpArrayCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     */
    NpArrayCodeGenerator.prototype.makeCode = function() {
        const { paramOption
                , paramData
                , returnVariable
                , dtype
                , isReturnVariable
                , indentSpaceNum } = this.numpyStateGenerator.getStateAll();
        const { paramOneArray, paramTwoArray, paramThreeArray, paramScalar, paramVariable } = paramData;
        
        var paramStr = ``;
        switch (paramOption) {
            // 1차원 배열
            case "1":{
                sbCode.append(`[`);
                paramOneArray.forEach(element => {
                    sbCode.append(`${fixNumpyParameterValue(element)},`);
                });
                sbCode.append(`]`);
                paramStr += sbCode.toString();
                sbCode.clear();
                break;
            }
            // 2차원 배열
            case "2":{
                sbCode.append(`[`);
                paramTwoArray.forEach(element => {
                    sbCode.append(`[`);
                    element.forEach(innerElement => {
                        sbCode.append(`${fixNumpyParameterValue(innerElement)},`);
                    });
                    sbCode.append(`],`);
                });
                sbCode.append(`]`);
                paramStr += sbCode.toString();
                sbCode.clear();
                break;
            }
            // 3차원 배열
            case "3":{
                sbCode.append(`[`);
                paramThreeArray.forEach(n2array => {
                    sbCode.append(`[`);
                    n2array.forEach(n1array => {
                        sbCode.append(`[`);
                        n1array.forEach(element => {
                            sbCode.append(`${fixNumpyParameterValue(element)},`);
                        });
                        sbCode.append(`],`);
                    });
                    sbCode.append(`],`);
                });
                sbCode.append(`]`);
                paramStr += sbCode.toString();
                sbCode.clear();
                break;
            }
            // 스칼라
            case "4":{
                paramStr += paramScalar;
                break;
            }
            // 사용자 정의 파라미터 변수
            case "5":{
                paramStr += paramVariable;
                break;
            }
            default:{
                break;
            }
        }

        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            numpyFunctionName: "array",
            paramStr: `${paramStr}`, 
            dtypeStr: dtype,
            isPrintReturnVar: isReturnVariable
        }
        this.makeNumpyFunctionCode(codeObject);
    }

    
    return NpArrayCodeGenerator;
});
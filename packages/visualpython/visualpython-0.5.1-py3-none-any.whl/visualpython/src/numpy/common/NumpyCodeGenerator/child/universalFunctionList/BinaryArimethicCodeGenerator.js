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
     * @class BinaryArimethicCodeGenerator
     * @constructor
    */
    var BinaryArimethicCodeGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    BinaryArimethicCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     */
    BinaryArimethicCodeGenerator.prototype.makeCode = function() {
        const { paramOption1
            , paramOption2
            , paramData
            , returnVariable
            , dtype
            , isReturnVariable
            , indentSpaceNum
            , funcId } = this.numpyStateGenerator.getStateAll();

        const { paramVariable
                , paramScalar
                , paramOneArray
                , paramTwoArray
                , paramThreeArray

                , param2Variable
                , param2Scalar
                , param2OneArray
                , param2TwoArray
                , param2ThreeArray } = paramData;

        var paramStr1 = ``;
        var paramStr2 = ``;

        switch (paramOption1) {
            // 1차원 배열
            case "1":{
                sbCode.append(`[`);
                paramOneArray.forEach(element => {
                    sbCode.append(`${fixNumpyParameterValue(element)},`);
                });
                sbCode.append(`]`);
                paramStr1 += sbCode.toString();
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
                paramStr1 += sbCode.toString();
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
                paramStr1 += sbCode.toString();
                sbCode.clear();
                break;
            }
            case "4": {
                paramStr1 += paramScalar;
                break;
            }
            case "5": {
                paramStr1 += paramVariable;
                break;
            }
            default: {
                break;
            }
        }

        switch (paramOption2) {
            case "1": {
                sbCode.append(`[`);
                param2OneArray.forEach(element => {
                    sbCode.append(`${fixNumpyParameterValue(element)},`);
                });
                sbCode.append(`]`);
                paramStr2 += sbCode.toString();
                sbCode.clear();
                break;
            }
            case "2": {
                sbCode.append(`[`);
                param2TwoArray.forEach(element => {
                    sbCode.append(`[`);
                    element.forEach(innerElement => {
                        sbCode.append(`${fixNumpyParameterValue(innerElement)},`);
                    });
                    sbCode.append(`],`);
                });
                sbCode.append(`]`);
                paramStr2 += sbCode.toString();
                sbCode.clear();
                break;
            }
            // 3차원 배열
            case "3":{
                sbCode.append(`[`);
                param2ThreeArray.forEach(n2array => {
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
                paramStr2 += sbCode.toString();
                sbCode.clear();
                break;
            }
            case "4": {
                paramStr2 += param2Scalar;
                break;
            }
            case "5": {
                paramStr2 += param2Variable;
                break;
            }
            default: {
                break;
            }
        }

        var numpyFunctionName = ``;
        switch(funcId){
            case "JY313": {
                numpyFunctionName = `add`;
                break;
            }
            case "JY314": {
                numpyFunctionName = `divide`;
                break;
            }
            case "JY315": {
                numpyFunctionName = `floor_divide`;
                break;
            }
            case "JY316": {
                numpyFunctionName = `fmax`;
                break;
            }
            case "JY317": {
                numpyFunctionName = `fmin`;
                break;
            }
            case "JY318": {
                numpyFunctionName = `maximum`;
                break;
            }
            case "JY319": {
                numpyFunctionName = `minimum`;
                break;
            }
            case "JY320": {
                numpyFunctionName = `mod`;
                break;
            }
            case "JY321": {
                numpyFunctionName = `multiply`;
                break;
            }
            case "JY322": {
                numpyFunctionName = `power`;
                break;
            }
            case "JY323": {
                numpyFunctionName = `subtract`;
                break;
            }
        }

        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            numpyFunctionName: `${numpyFunctionName}`,
            paramStr: `${paramStr1} , ${paramStr2} `, 
            dtypeStr: dtype,
            isPrintReturnVar: isReturnVariable
        }

        this.makeNumpyFunctionCode(codeObject);
    }

    
    return BinaryArimethicCodeGenerator;
});

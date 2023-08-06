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
     * @class BinaryComparatorCodeGenerator
     * @constructor
    */
    var BinaryComparatorCodeGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    BinaryComparatorCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     */
    BinaryComparatorCodeGenerator.prototype.makeCode = function() {
        const { paramOption1
            , paramOption2
            , paramData
            , returnVariable
            // , dtype
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
            case "JY324": {
                numpyFunctionName = `equal`;
                break;
            }
            case "JY325": {
                numpyFunctionName = `greater`;
                break;
            }
            case "JY326": {
                numpyFunctionName = `greater_equal`;
                break;
            }
            case "JY327": {
                numpyFunctionName = `less`;
                break;
            }
            case "JY328": {
                numpyFunctionName = `less_equal`;
                break;
            }
            case "JY329": {
                numpyFunctionName = `not_equal`;
                break;
            }
            default: {
                break;
            }
        }

        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            numpyFunctionName: `${numpyFunctionName}`,
            paramStr: `${paramStr1} , ${paramStr2} `, 
            // dtypeStr: dtype,
            isPrintReturnVar: isReturnVariable
        }

        this.makeNumpyFunctionCodeNoDtype(codeObject);
    }

    
    return BinaryComparatorCodeGenerator;
});

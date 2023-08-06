define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeGenerator/parent/NumpyCodeGenerator'
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi'
], function(requirejs, sb, 
            NumpyCodeGenerator,
            numpyStateApi) {
    "use strict";
    var sbCode = new sb.StringBuilder();
    var { fixNumpyParameterValue } = numpyStateApi;
    /**
     * @class NpLinalgSolveGenerator
     * @constructor
    */
    var NpLinalgSolveGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    NpLinalgSolveGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     * @param {Obejct} state 
     */
    NpLinalgSolveGenerator.prototype.makeCode = function(state) {
        const { paramOption1
                , paramOption2
                , paramData
                , returnVariable
                , dtype
                , isReturnVariable
                , indentSpaceNum } = this.numpyStateGenerator.getStateAll();

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

            // 2차원 배열
            case "1":{
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
            case "2":{
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
  
            case "3": {
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
            case "2":{
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
   
            case "3": {
                paramStr2 += param2Variable;
                break;
            }
            default: {
                break;
            }
        }

        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            numpyFunctionName: "linalg.solve",
            paramStr: `${paramStr1} , ${paramStr2} `, 
            dtypeStr: dtype,
            isPrintReturnVar: isReturnVariable
        }

        this.makeNumpyFunctionCodeNoDtype(codeObject);
    }

    return NpLinalgSolveGenerator;
});

define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    // Numpy 패키지용 import 라이브러리
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeGenerator/parent/NumpyCodeGenerator'
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi'
], function(requirejs, sb, 
            NumpyCodeGenerator,
            NumpyStateApi) {
    "use strict";
    var sbCode = new sb.StringBuilder();
    var { fixNumpyParameterValue } = NumpyStateApi;

    /**
     * @class NpArrayCodeGenerator
     * @constructor
    */
    var NpMeanVarStdMaxMinPercentileMedianCodeGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    NpMeanVarStdMaxMinPercentileMedianCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     */
    NpMeanVarStdMaxMinPercentileMedianCodeGenerator.prototype.makeCode = function() {
        const { paramOption
                , paramData
                , returnVariable
                , isReturnVariable
                , funcId
                , indentSpaceNum
                , axis
                , indexQ
                , dtype } = this.numpyStateGenerator.getStateAll();
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

        // 각 funcId에 맞게 라우팅 되어 코드 실행
        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            numpyFunctionName: ``,
            paramStr: `${paramStr}`, 
            dtypeStr: ``,
            isPrintReturnVar: isReturnVariable
        }

        switch(funcId){
            case "JY200": {
                codeObject.numpyFunctionName = `mean`;
                codeObject.dtypeStr = dtype;
                this.makeNumpyFunctionCode(codeObject);
                break;
            }
            case "JY201": {
                codeObject.numpyFunctionName = `var`;
                codeObject.dtypeStr = dtype;
                this.makeNumpyFunctionCode(codeObject);
                break;
            }
            case "JY202": {
                codeObject.numpyFunctionName = `std`;
                codeObject.dtypeStr = dtype;
                this.makeNumpyFunctionCode(codeObject);
                break;
            }
            case "JY203": {
                codeObject.numpyFunctionName = `max`;
                delete codeObject.dtypeStr;
                this.makeNumpyFunctionCodeNoDtype(codeObject);
                break;
            }
            case "JY204": {
                codeObject.numpyFunctionName = `min`;
                delete codeObject.dtypeStr;
                this.makeNumpyFunctionCodeNoDtype(codeObject);
                break;
            }
            case "JY205": {
                codeObject.numpyFunctionName = `median`;
                delete codeObject.dtypeStr;
                this.makeNumpyFunctionCodeNoDtype(codeObject);
                break;
            }
            case "JY206": {
                codeObject.numpyFunctionName = `percentile`;
                codeObject.paramStr += `,${indexQ},axis=${axis}`;
                delete codeObject.dtypeStr;
                this.makeNumpyFunctionCodeNoDtype(codeObject);
                break;
            }
        }
    }

    return NpMeanVarStdMaxMinPercentileMedianCodeGenerator;
});
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
     * @class MakeArrayCodeGenerator
     * @constructor
    */
    var MakeArrayCodeGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    MakeArrayCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     */
    MakeArrayCodeGenerator.prototype.makeCode = function() {
        const { paramOption1
                , paramOption1_1
                , paramOption1_2
                , paramOption2
                , paramData
                , returnVariable
       
                , isReturnVariable
                , indentSpaceNum } = this.numpyStateGenerator.getStateAll();

        const { npArrayParamOneArray, npArrayParamTwoArray, npArrayParamThreeArray, 
                npArrayParamScalar, npArrayParamVariable,
            
                npArangeParam1Start, npArangeParam2Start, npArangeParam2Stop, npArangeParam3Start,
                npArangeParam3Stop, npArangeParam3Step,
            
                npReshapeParam1Length, npReshapeParam2Row, npReshapeParam2Col, npReshapeParam3Row,
                npReshapeParam3Col, npReshapeParam3Depth} = paramData;

        var numpyFunctionName;
        var paramStr1 = ``;
        switch(paramOption1){
            case "1": {
                numpyFunctionName = "array";
                if(paramOption1_1 === "1"){
                    sbCode.append(`[`);
                    npArrayParamOneArray.forEach(element => {
                        sbCode.append(`${fixNumpyParameterValue(element)},`);
                    });
                    sbCode.append(`]`);
                    paramStr1 += sbCode.toString();
                    sbCode.clear();
                } else if(paramOption1_1 === "2"){
                    sbCode.append(`[`);
                    npArrayParamTwoArray.forEach(element => {
                        sbCode.append(`[`);
                        element.forEach(innerElement => {
                            sbCode.append(`${fixNumpyParameterValue(innerElement)},`);
                        });
                        sbCode.append(`],`);
                    });
                    sbCode.append(`]`);
                    paramStr1 += sbCode.toString();
                    sbCode.clear();
                } else if(paramOption1_1 === "3"){
                    sbCode.append(`[`);
                    npArrayParamThreeArray.forEach(n2array => {
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

                } else if(paramOption1_1 === "4"){
                    paramStr1 += npArrayParamScalar;
                } else {
                    paramStr1 += npArrayParamVariable;
                }
                break;
            }
            case "2": {
                numpyFunctionName = "arange";
                if(paramOption1_2 === "1"){
                    paramStr1 += `${npArangeParam1Start}`;
                } else if(paramOption1_2 === "2"){
                    paramStr1 += `${npArangeParam2Start},${npArangeParam2Stop}`;
                } else {
                    paramStr1 += `${npArangeParam3Start},${npArangeParam3Stop},${npArangeParam3Step}`;
                }
                break;
            }
        }

        var paramStr2 = ``;
        switch(paramOption2){
            case "1": {
                paramStr2 += `${npReshapeParam1Length}`;
                break;
            }
            case "2": {
                paramStr2 += `${npReshapeParam2Row},${npReshapeParam2Col}`;
                break;
            }
            case "3": {
                paramStr2 += `${npReshapeParam3Row},${npReshapeParam3Col},${npReshapeParam3Depth}`;
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
            paramStr1: paramStr1, 
            paramStr2: paramStr2,
            isPrintReturnVar: isReturnVariable
        }

        this.makeNumpyMakeArrayCode(codeObject);
    }

    return MakeArrayCodeGenerator;
});


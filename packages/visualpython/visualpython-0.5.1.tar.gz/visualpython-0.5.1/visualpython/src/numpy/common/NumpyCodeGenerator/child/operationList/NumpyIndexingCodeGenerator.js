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
     * @class NumpyIndexingCodeGenerator
     * @constructor
    */
    var NumpyIndexingCodeGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    NumpyIndexingCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     * @param {Obejct} state 
     */
    NumpyIndexingCodeGenerator.prototype.makeCode = function(state) {
        const { paramOption
                , paramData
                , callVariable
                , returnVariable
                , isReturnVariable
                , indentSpaceNum } = this.numpyStateGenerator.getStateAll();
        const { paramOption1Start, paramOption1End 
                , paramOption2RowStart, paramOption2RowEnd, paramOption2ColStart, paramOption2ColEnd
                , paramOption3Array } = paramData;

        var paramStr = ``;
        switch (paramOption) {
            case "1": {
                paramStr += `${callVariable}[${paramOption1Start}:${paramOption1End}]`;
                break;
            }
            case "2": {
                paramStr += `${callVariable}[${paramOption2RowStart}:${paramOption2RowEnd}][${paramOption2ColStart}:${paramOption2ColEnd}]`;
                break;
            }

            case "3": {
                paramStr += `${callVariable}`;
                paramOption3Array.forEach(elementArray => {
                    sbCode.append(`[`);
                    elementArray.forEach((element,index) => {
                        // 비교 연산자 우선순위 설정 ex) (a > b) == (c < d)
                        var left = `(`;
                        var right = `)`;
                        if(index === 0) {
                            sbCode.append(`${left}${element.value}`);
                        } else {
                            // index가 짝수
                            if(index % 2 === 0){
                                sbCode.append(`${element.operator}${left}${element.value}`);
                            // index가 홀수
                            } else {
                                // isDisable === true
                                if(element.isDisable === true){
                                    sbCode.append(`${right}`);
                                // isDisable === false
                                } else {
                                    sbCode.append(`${element.operator}${element.value}${right}`);
                                }
                            
                            }
                        }
                    });
                    sbCode.append(`]`);
                });
                paramStr += sbCode.toString();
                sbCode.clear();
                break;
            }
            default: {
                break;
            }
        }

        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            paramStr: `${paramStr}`, 
            assignedValueStr: "",
            isPrintReturnVar: isReturnVariable
        }

        this.makeNumpyIndexingCode(codeObject);
    }

    return NumpyIndexingCodeGenerator;
});

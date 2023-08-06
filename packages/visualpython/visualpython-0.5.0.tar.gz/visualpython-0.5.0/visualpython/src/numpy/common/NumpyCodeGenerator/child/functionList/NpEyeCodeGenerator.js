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
     * @class NpEyeCodeGenerator
     * @constructor
    */
    var NpEyeCodeGenerator = function() {

    };

    /**
     * NumpyCodeGenerator 에서 상속
    */
    NpEyeCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);
    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     * @param {Obejct} state 
     */
    NpEyeCodeGenerator.prototype.makeCode = function(state) {
        const { paramData
                , returnVariable
                , dtype
                , isReturnVariable
                , indentSpaceNum } = this.numpyStateGenerator.getStateAll();
        const { paramRowCol, paramKIndex } = paramData;

        var paramStr = `${paramRowCol},k=${paramKIndex}`;
        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            numpyFunctionName: "eye",
            paramStr: `${paramStr}`, 
            dtypeStr: dtype,
            isPrintReturnVar: isReturnVariable
        }

        this.makeNumpyFunctionCode(codeObject);
    }

    return NpEyeCodeGenerator;
});

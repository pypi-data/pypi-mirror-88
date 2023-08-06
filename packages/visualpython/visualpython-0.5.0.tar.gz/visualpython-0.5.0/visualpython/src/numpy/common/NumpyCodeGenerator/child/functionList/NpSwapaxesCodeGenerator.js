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
     * @class NpSwapaxesCodeGenerator
     * @constructor
    */
    var NpSwapaxesCodeGenerator = function() {

    };

    /**
     * NumpyCodeGenerator 에서 상속
    */
    NpSwapaxesCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     * @param {Obejct} state 
     */
    NpSwapaxesCodeGenerator.prototype.makeCode = function(state) {
        const { paramData
                , returnVariable
                , isReturnVariable
                , indentSpaceNum } = this.numpyStateGenerator.getStateAll();
        const { paramVariable,
                paramAxis1, paramAxis2 } = paramData;

        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            numpyFunctionName: "swapaxes",
            paramStr: `${paramVariable},${paramAxis1},${paramAxis2}`, 
            isPrintReturnVar: isReturnVariable
        }

        this.makeNumpyFunctionCodeNoDtype(codeObject);
    }

    return NpSwapaxesCodeGenerator;
});

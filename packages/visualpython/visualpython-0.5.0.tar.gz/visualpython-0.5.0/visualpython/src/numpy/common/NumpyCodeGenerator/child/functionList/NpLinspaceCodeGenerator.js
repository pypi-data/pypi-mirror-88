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
     * @class NpLinspaceCodeGenerator
     * @constructor
    */
    var NpLinspaceCodeGenerator = function() {

    };

    /**
     * NumpyCodeGenerator 에서 상속
    */
    NpLinspaceCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);
    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     * @param {Obejct} state 
     */
    NpLinspaceCodeGenerator.prototype.makeCode = function(state) {
        const { paramData
                , returnVariable
                , dtype
                , isReturnVariable
                , indentSpaceNum } = this.numpyStateGenerator.getStateAll();

        const { paramStart, paramStop, paramNum, paramEndpoint, paramRetstep } = paramData;
        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            numpyFunctionName: "linspace",
            paramStr: `${paramStart},${paramStop},${paramNum},endpoint=${paramEndpoint},retstep=${paramRetstep}`, 
            dtypeStr: dtype,
            isPrintReturnVar: isReturnVariable
        }

        this.makeNumpyFunctionCode(codeObject);
    }

    return NpLinspaceCodeGenerator;
});

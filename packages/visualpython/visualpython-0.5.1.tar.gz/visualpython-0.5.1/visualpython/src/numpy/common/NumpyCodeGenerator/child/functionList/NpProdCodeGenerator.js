define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeGenerator/parent/NumpyCodeGenerator'
], function(requirejs, sb, 
            NumpyCodeGenerator) {

    "use strict";
    var sbCode = new sb.StringBuilder();

    /**
     * @class NpProdCodeGenerator
     * @constructor
    */
    var NpProdCodeGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    NpProdCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     * @param {Obejct} state 
     */
    NpProdCodeGenerator.prototype.makeCode = function(state) {
        const { paramData
                , returnVariable
                , axis
                , isReturnVariable
                , indentSpaceNum } = this.numpyStateGenerator.getStateAll();
        const { paramVariable } = paramData;

        var paramStr = `${paramVariable}, axis = ${axis}`;

        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            numpyFunctionName: "prod",
            paramStr: `${paramStr}`, 
            isPrintReturnVar: isReturnVariable
        }
        this.makeNumpyFunctionCodeNoDtype(codeObject);
    }

    return NpProdCodeGenerator;
});

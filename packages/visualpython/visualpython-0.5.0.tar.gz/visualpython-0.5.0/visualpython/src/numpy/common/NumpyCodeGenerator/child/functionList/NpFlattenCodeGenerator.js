define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeGenerator/parent/NumpyCodeGenerator'
], function(requirejs, sb, 
            NumpyCodeGenerator) {

    "use strict";
    var sbCode = new sb.StringBuilder();

    /**
     * @class NpFlattenCodeGenerator
     * @constructor
    */
    var NpFlattenCodeGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    NpFlattenCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     * @param {Obejct} state 
     */
    NpFlattenCodeGenerator.prototype.makeCode = function(state) {
        const { paramOption
                , paramData
                , returnVariable
                , callVariable
                , isReturnVariable
                , indentSpaceNum } = this.numpyStateGenerator.getStateAll();

        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0, 
            returnVarStrOrNull: returnVariable, 
            callVarStr : callVariable,
            numpyFunctionName: "flatten",
            paramStr: ``, 
            isPrintReturnVar: isReturnVariable
        }

        this.makeNumpyInstanceFunctionCode(codeObject);
    }

    return NpFlattenCodeGenerator;
});

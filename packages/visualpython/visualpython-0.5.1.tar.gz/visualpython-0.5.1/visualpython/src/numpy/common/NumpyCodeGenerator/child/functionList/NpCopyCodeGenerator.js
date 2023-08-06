define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeGenerator/parent/NumpyCodeGenerator'
], function(requirejs, sb, 
            NumpyCodeGenerator) {

    "use strict";
    var sbCode = new sb.StringBuilder();

    /**
     * @class NpCopyCodeGenerator
     * @constructor
    */
    var NpCopyCodeGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    NpCopyCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     */
    NpCopyCodeGenerator.prototype.makeCode = function() {
        const { paramData
                , returnVariable
                , isReturnVariable
                , indentSpaceNum } = this.numpyStateGenerator.getStateAll();
        const { paramVariable } = paramData;
        var codeObject = {
            indentSpaceNum: indentSpaceNum || 0
            , returnVarStrOrNull: returnVariable
            , numpyFunctionName: "copy"
            , paramStr: `${paramVariable}`
            , isPrintReturnVar: isReturnVariable
        }

        this.makeNumpyFunctionCodeNoDtype(codeObject);
    }

    return NpCopyCodeGenerator;
});

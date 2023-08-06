define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    // Numpy 패키지용 import 라이브러리
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeGenerator/parent/NumpyCodeGenerator'
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi'
], function(requirejs, sb, 
            NumpyCodeGenerator, NumpyStateApi) {
    "use strict";
    var sbCode = new sb.StringBuilder();
    var { fixNumpyParameterValue } = NumpyStateApi;

    /**
     * @class NumpyModeCodeGenerator
     * @constructor
    */
    var NumpyModeCodeGenerator = function() {

    };
    /**
     * NumpyCodeGenerator 에서 상속
    */
    NumpyModeCodeGenerator.prototype = Object.create(NumpyCodeGenerator.prototype);

    /**
     * NumpyCodeGenerator makeCode 메소드 오버라이드
     * @param {Obejct} state 
     */
    NumpyModeCodeGenerator.prototype.makeCode = function(state) {

    }

    return NumpyModeCodeGenerator;
});

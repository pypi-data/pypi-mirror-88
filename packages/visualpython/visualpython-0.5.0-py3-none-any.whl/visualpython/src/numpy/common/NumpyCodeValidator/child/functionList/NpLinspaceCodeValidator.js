define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";
    /**
     * @class NpLinspaceCodeValidator
     * @constructor
    */
    var NpLinspaceCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpLinspaceCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    */
    NpLinspaceCodeValidator.prototype.validate = function(state) {
        const { returnVariable
                , paramData
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramStart, paramStop, paramNum } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        if (this.checkIsNullString(paramStart) || this.checkIsString(paramStart)) {
            return false;
        }
        if (this.checkIsNullString(paramStop) || this.checkIsString(paramStop)) {
            return false;
        }
        if (this.checkIsNullString(paramNum) || this.checkIsString(paramNum)) {
            return false;
        }

        return true;
    }

    return NpLinspaceCodeValidator;
});

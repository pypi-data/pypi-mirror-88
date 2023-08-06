define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";
    /**
     * @class NpEyeCodeValidator
     * @constructor
    */
    var NpEyeCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpEyeCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    */
    NpEyeCodeValidator.prototype.validate = function(state) {
        const { paramData
                , returnVariable
                , dtype
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramRowCol, paramKIndex } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        // parameter : paramRowCol 값이 입력되지 않았거나 or 숫자가 아닌 순수 문자열로 되어 있으면 validation
        if (this.checkIsNullString(paramRowCol) || this.checkIsString(paramRowCol) ) {
            return false;
        }
        // subparameter : paramKIndex 값이 입력되지 않았거나 or 숫자가 아닌 순수 문자열로 되어 있으면 validation
        if (this.checkIsNullString(paramKIndex) || this.checkIsString(paramKIndex) ) {
            return false;
        }
        return true;
    }

    return NpEyeCodeValidator;
});

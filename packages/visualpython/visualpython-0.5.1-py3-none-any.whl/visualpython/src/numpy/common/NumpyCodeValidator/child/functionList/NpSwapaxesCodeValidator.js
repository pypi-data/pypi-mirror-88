define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class NpSwapaxesCodeValidator
     * @constructor
    */
    var NpSwapaxesCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpSwapaxesCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    * @return {boolean} true면 통과 false면 에러
    */
    NpSwapaxesCodeValidator.prototype.validate = function(state) {
        const { returnVariable
                , paramData
                , isReturnVariable
                , indentSpaceNum } = state;

        const { paramVariable, paramAxis1, paramAxis2 } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        if (this.checkIsNullString(paramAxis1) || this.checkIsString(paramAxis1) ) {
            return false;
        }

        if (this.checkIsNullString(paramAxis2) || this.checkIsString(paramAxis2) ) {
            return false;
        }

        return true;
    }

    return NpSwapaxesCodeValidator;
});

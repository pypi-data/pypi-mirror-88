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
    var NpFlattenCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpFlattenCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    */
    NpFlattenCodeValidator.prototype.validate = function(state) {
        const { returnVariable
                , callVariable
                , isReturnVariable
                , indentSpaceNum } = state;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }
        // if (this.checkisVarableReservedWord(callVariable) || this.checkIsNumberString(callVariable)) {
        //     return false;
        // }
        return true;
    }

    return NpFlattenCodeValidator;
});

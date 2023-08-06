define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";
    /**
     * @class NpFlipCodeValidator
     * @constructor
    */
    var NpFlipCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpFlipCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    */
    NpFlipCodeValidator.prototype.validate = function(state) {
        const { returnVariable
                , paramData
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramVariable } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(paramVariable) || this.checkIsNumberString(paramVariable)) {
            return false;
        }
        return true;
    }

    return NpFlipCodeValidator;
});

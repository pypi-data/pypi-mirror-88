define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class NpRavelCodeValidator
     * @constructor
    */
    var NpRavelCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpRavelCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    */
    NpRavelCodeValidator.prototype.validate = function(state) {
        const { returnVariable
                , order
                , paramData
                , isReturnVariable
                , indentSpaceNum } = state;

        const { paramVariable } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }
        // 사용자 정의 변수(param) 입력시, 입력값이 없는지 확인 or 숫자를 썼는지 화인, 예약어를 썼는지 확인
        if (this.checkIsNullString(paramVariable) || this.checkIsNumberString(paramVariable)
            || this.checkisVarableReservedWord(paramVariable)) {
            return false;
        };
        return true;
    }

    return NpRavelCodeValidator;
});

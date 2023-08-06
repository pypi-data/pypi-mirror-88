define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";
    
    /**
     * @class NpDiffCodeValidator
     * @constructor
    */
    var NpDiffCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpDiffCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    */
    NpDiffCodeValidator.prototype.validate = function(state) {
        const { returnVariable
                , paramData
                , indexN
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramVariable } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        // param 변수 입력시, 입력값이 존재하는지 확인 
        // or 예약어를 썼는지 확인 validation 
        // or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkIsNullString(paramVariable) || this.checkisVarableReservedWord(paramVariable) || this.checkIsNumberString(paramVariable)) {
            return false;
        }
        return true;
    }

    return NpDiffCodeValidator;
});

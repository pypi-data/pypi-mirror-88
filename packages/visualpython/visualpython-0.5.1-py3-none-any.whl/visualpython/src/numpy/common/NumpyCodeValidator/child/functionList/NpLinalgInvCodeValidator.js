define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";
    /**
     * @class NpLinalgInvCodeValidator
     * @constructor
    */
    var NpLinalgInvCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpLinalgInvCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);
        /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    */
    NpLinalgInvCodeValidator.prototype.validate = function(state) {
        const { paramOption
                , paramData
                , returnVariable
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramVariable, paramTwoArray } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }
        
        switch (paramOption) {
            case "1" : {
                if (this.checkIsNullString(paramVariable) || this.checkIsNumberString(paramVariable) ) {
                    return false;
                }
                break;
            }
            case "2" : {
                if (this.checkIsArrayLengthZero(paramTwoArray)) {
                    return false;
                }
                break;
            }
            default : {
                break;
            }
        }

        
        return true;
    }

    return NpLinalgInvCodeValidator;
});

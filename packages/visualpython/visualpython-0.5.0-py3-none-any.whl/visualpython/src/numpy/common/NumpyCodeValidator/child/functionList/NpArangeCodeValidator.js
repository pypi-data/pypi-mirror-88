define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class NpArangeCodeValidator
     * @constructor
    */
    var NpArangeCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpArangeCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
     * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
     * @param {Obejct} state 
    */
    NpArangeCodeValidator.prototype.validate = function(state) {
        const { paramOption
                , paramData
                , returnVariable
                , dtype
                , isReturnVariable
                , indentSpaceNum } = state;
                
        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        switch (paramOption) {
            case "1" : {
                if (this.checkIsNullString(paramData.paramOption1DataStart) || this.checkIsString(paramData.paramOption1DataStart) ) {
                    return false;
                }
                
                break;
            }
            case "2" : {
                if (this.checkIsNullString(paramData.paramOption2DataStart) || this.checkIsString(paramData.paramOption2DataStart) ) {
                    return false;
                }
                if (this.checkIsNullString(paramData.paramOption2DataStop) || this.checkIsString(paramData.paramOption2DataStop) ) {
                    return false;
                }

                break;
            }

            case "3" : {
                if (this.checkIsNullString(paramData.paramOption3DataStart) || this.checkIsString(paramData.paramOption3DataStart) ) {
                    return false;
                }
                if (this.checkIsNullString(paramData.paramOption3DataStop) || this.checkIsString(paramData.paramOption3DataStop) ) {
                    return false;
                }
                if (this.checkIsNullString(paramData.paramOption3DataStep) || this.checkIsString(paramData.paramOption3DataStep) ) {
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

    return NpArangeCodeValidator;
});

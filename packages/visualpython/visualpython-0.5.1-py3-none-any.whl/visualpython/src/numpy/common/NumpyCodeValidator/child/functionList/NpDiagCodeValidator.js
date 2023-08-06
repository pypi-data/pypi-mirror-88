define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class NpDiagCodeValidator
     * @constructor
    */
    var NpDiagCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpDiagCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
     * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
     * @param {Obejct} state 
    */
    NpDiagCodeValidator.prototype.validate = function(state) {
        const { paramOption
                , paramData
                , returnVariable
                , indexK
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramOneArray, paramTwoArray, paramVariable } = paramData;
        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }
        // indexK validation
        if (this.checkIsNullString(indexK) || this.checkIsString(indexK)) {
            return false;
        }

        switch (paramOption) {
            // param 옵션 1: 1차원 array validation
            case "1" : {
                if (this.validateOneArray(paramOneArray)) {
                    return false;
                }
                break;
            }
            // param 옵션 2: 2차원 array validation
            case "2" : {
                if (this.validateTwoArray(paramTwoArray)) {
                    return false;
                }
                break;
            }
            // param 옵션 3: 사용자 정의 함수 validation
            case "3" : { 
                if (this.checkIsNullString(paramVariable) || this.checkIsNumberString(paramVariable)
                    || this.checkisVarableReservedWord(paramVariable)) {
                    return false;
                };
                break;
            }
        }
        return true;
    }

    return NpDiagCodeValidator;
});

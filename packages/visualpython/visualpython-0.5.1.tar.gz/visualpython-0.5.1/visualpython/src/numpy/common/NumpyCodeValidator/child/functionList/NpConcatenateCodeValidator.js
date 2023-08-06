define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";
    /**
     * @class NpConcatenateCodeValidator
     * @constructor
    */
    var NpConcatenateCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpConcatenateCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    */
    NpConcatenateCodeValidator.prototype.validate = function(state) {
        const { paramOption
                , axis
                , paramData
                , returnVariable
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramOption1ParamVariable1
                , paramOption1ParamVariable2

                , paramOption2ParamVariable1
                , paramOption2ParamVariable2
                , paramOption2ParamVariable3

                , paramOption3ParamVariableArray  } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        switch (paramOption) {
            // param 옵션 1: validation
            case "1" : {
                if (this.checkIsNullString(paramOption1ParamVariable1) || this.checkIsNumberString(paramOption1ParamVariable1)
                    || this.checkisVarableReservedWord(paramOption1ParamVariable1)) {
                    return false;
                };
                if (this.checkIsNullString(paramOption1ParamVariable2) || this.checkIsNumberString(paramOption1ParamVariable2)
                    || this.checkisVarableReservedWord(paramOption1ParamVariable2)) {
                    return false;
                };
                break;
            }
            // param 옵션 2: validation
            case "2" : {
                if (this.checkIsNullString(paramOption2ParamVariable1) || this.checkIsNumberString(paramOption2ParamVariable1)
                    || this.checkisVarableReservedWord(paramOption2ParamVariable1)) {
                    return false;
                };
                if (this.checkIsNullString(paramOption2ParamVariable2) || this.checkIsNumberString(paramOption2ParamVariable2)
                    || this.checkisVarableReservedWord(paramOption2ParamVariable2)) {
                    return false;
                };
                if (this.checkIsNullString(paramOption2ParamVariable3) || this.checkIsNumberString(paramOption2ParamVariable3)
                    || this.checkisVarableReservedWord(paramOption2ParamVariable3)) {
                    return false;
                };         
                break;
            }
            // param 옵션 3: validation
            case "3" : {
                if (this.checkIsArrayLengthZero(paramOption3ParamVariableArray)) {
                    return false;
                }

                break;
            }
        }
        return true;
    }

    return NpConcatenateCodeValidator;
});

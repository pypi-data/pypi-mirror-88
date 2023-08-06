define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";
    /**
     * @class NpFullCodeValidator
     * @constructor
    */
    var NpFullCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpFullCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    */
    NpFullCodeValidator.prototype.validate = function(state) {
        const { paramOption
                , paramData
                , returnVariable
                , indexValue
                , dtype
                , isReturnVariable
                , indentSpaceNum } = state;

        // 예약어를 썼는지 확인 validation or 문자를 썼는지 확인 validation
        if (this.checkIsNullString(indexValue) || this.checkIsString(indexValue)){
            return false;
        }
        
        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        switch (paramOption) {
            case "1" : {
                if (this.checkIsNullString(paramData.paramOption1DataLength) || this.checkIsString(paramData.paramOption1DataLength) ) {
                    return false;
                }
                
                break;
            }
            case "2" : {
                if (this.checkIsNullString(paramData.paramOption2DataRow) || this.checkIsString(paramData.paramOption2DataRow) ) {
                    return false;
                }
                if (this.checkIsNullString(paramData.paramOption2DataCol) || this.checkIsString(paramData.paramOption2DataCol) ) {
                    return false;
                }

                break;
            }

            case "3" : {
                if (this.checkIsArrayLengthZero(paramData.paramOption3DataArray)) {
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
    return NpFullCodeValidator;
});

define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class NpReshapeCodeValidator
     * @constructor
    */
    var NpReshapeCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpReshapeCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    */
    NpReshapeCodeValidator.prototype.validate = function(state) {
        const { paramOption
                , paramData
                , returnVariable
                , callVariable
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramOption1DataLength
                , paramOption2DataRow , paramOption2DataCol
                , paramOption3DataRow , paramOption3DataCol, paramOption3DataDepth } = paramData;
                
        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }
        
        /**  call variable: call variable 값이 입력되지 않았거나 or  예약어를 썼거나
        *                or  순수 문자열이 아닌 숫자 문자열로 되어 있으면 validation
        */

        // if ( this.checkIsNullString(callVariable) || this.checkisVarableReservedWord(returnVariable) 
        //     || this.checkIsNumberString(callVariable) ) {
        //     return false;
        // }

        switch (paramOption) {
            // param 옵션 1 : narray를 1차원 배열로 reshape
            case "1": {
                if (this.checkIsNullString(paramOption1DataLength) || this.checkIsString(paramOption1DataLength) ) {
                    return false;
                }
                break;
            }
            // param 옵션 2 : narray를 2차원 배열로 reshape
            case "2": {
                if (this.checkIsNullString(paramOption2DataRow) || this.checkIsString(paramOption2DataRow) ) {
                    return false; 
                }
                if (this.checkIsNullString(paramOption2DataCol) || this.checkIsString(paramOption2DataCol) ) {
                    return false;
                }

                break;
            }
            // param 옵션 3 : narray를 3차원 배열로 reshape
            case "3": {
                if (this.checkIsNullString(paramOption3DataRow) || this.checkIsString(paramOption3DataRow) ) {
                    return false;
                }
                if (this.checkIsNullString(paramOption3DataCol) || this.checkIsString(paramOption3DataCol) ) {
                    return false;
                }
                if (this.checkIsNullString(paramOption3DataDepth) || this.checkIsString(paramOption3DataDepth) ) {
                    return false;
                }

                break;
            }
            default: {
                break;
            }
        }

        // validation 성공시 true 리턴
        return true;
    }

    return NpReshapeCodeValidator;
});
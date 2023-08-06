define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class NpDstackHstackVstackCodeValidator
     * @constructor
    */
    var NpDstackHstackVstackCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpDstackHstackVstackCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
     * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
     * @param {Obejct} state 
    */
    NpDstackHstackVstackCodeValidator.prototype.validate = function(state) {
        const { paramOption
                , paramData
                , returnVariable
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramOption1DataLength, 
                paramOption2DataRow, paramOption2DataCol,
                paramOption3DataRow, paramOption3DataCol, paramOption3DataDepth,
                paramOption4DataArray } = paramData;


        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }
        // param 변수 입력시, 값이 입력되었는지 확인 validation or 숫자를 썼는지 확인 validation or 파이썬 예약어를 썼는지 확인 
        // if (this.checkIsNullString(paramVariable) || this.checkIsNumberString(paramVariable)
        //     || this.checkisVarableReservedWord(paramVariable)) {
        //     return false;
        // };
        /**  return 변수 입력 값이 이상이 없거나,
         *   return 변수를 입력하지 않았다면 아래 코드로 넘어간다.
        */

        switch (paramOption) {
            // param 옵션 1:
            case "1" : {
                if (this.checkIsNullString(paramOption1DataLength) || this.checkIsNumberString(paramOption1DataLength) 
                    || this.checkisVarableReservedWord(paramOption1DataLength)) {
                    return false;
                }
                break;
            }
            // param 옵션 2: 
            case "2" : {
                if (this.checkIsNullString(paramOption2DataRow) || this.checkIsNumberString(paramOption2DataRow) 
                    || this.checkisVarableReservedWord(paramOption2DataRow)) {
                    return false;
                }
                if (this.checkIsNullString(paramOption2DataCol) || this.checkIsNumberString(paramOption2DataCol) 
                    || this.checkisVarableReservedWord(paramOption2DataCol)) {
                    return false;
                }
                break;
            }
            // param 옵션 3: 
            case "3" : {
                if (this.checkIsNullString(paramOption3DataRow) || this.checkIsNumberString(paramOption3DataRow) 
                    || this.checkisVarableReservedWord(paramOption3DataRow)) {
                    return false;
                }
                if (this.checkIsNullString(paramOption3DataCol) || this.checkIsNumberString(paramOption3DataCol) 
                    || this.checkisVarableReservedWord(paramOption3DataCol)) {
                    return false;
                }
                if (this.checkIsNullString(paramOption3DataDepth) || this.checkIsNumberString(paramOption3DataDepth) 
                    || this.checkisVarableReservedWord(paramOption3DataDepth)) {
                    return false;
                }
                break;
            }
            // param 옵션 4: 1차원 array validation
            case "4" : { 
                if (this.validateOneArrayTypeString(paramOption4DataArray)) {
                    return false;
                }

                break;
            }
        }
        return true;
    }

    return NpDstackHstackVstackCodeValidator;
});
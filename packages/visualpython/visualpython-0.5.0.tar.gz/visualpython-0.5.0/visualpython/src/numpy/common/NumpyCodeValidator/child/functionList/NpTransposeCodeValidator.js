// paramOption1Axis1: "",
// paramOption1Axis2: "",

// paramOption2Axis1: "",
// paramOption2Axis2: "",
// paramOption2Axis3: "",

// paramOption3DataArray: ["0"],
define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class NpTransposeCodeValidator
     * @constructor
    */
    var NpTransposeCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpTransposeCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    * @return {boolean} true면 통과 false면 에러
    */
    NpTransposeCodeValidator.prototype.validate = function(state) {
        const { paramOption
                , paramData
                , returnVariable
                , dtype
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramVariable, 
                paramOption1Axis1, paramOption1Axis2,
                paramOption2Axis1, paramOption2Axis2, paramOption2Axis3,
                paramOption3AxisArray } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }
        if (this.checkIsNullString(paramVariable) || this.checkIsNumberString(paramVariable)
            || this.checkisVarableReservedWord(paramVariable)) {
            return false;
        };
        
        switch (paramOption) {
            case "1" : {
                if (this.checkIsNullString(paramOption1Axis1) || this.checkIsString(paramOption1Axis1) ) {
                    return false;
                }
                if (this.checkIsNullString(paramOption1Axis2) || this.checkIsString(paramOption1Axis2) ) {
                    return false;
                }
                break;
            }
            case "2" : {
                if (this.checkIsNullString(paramOption2Axis1) || this.checkIsString(paramOption2Axis1) ) {
                    return false;
                }
                if (this.checkIsNullString(paramOption2Axis2) || this.checkIsString(paramOption2Axis2) ) {
                    return false;
                }
                if (this.checkIsNullString(paramOption2Axis3) || this.checkIsString(paramOption2Axis3) ) {
                    return false;
                }
                break;
            }

            case "3" : {
                if (this.checkIsArrayLengthZero(paramOption3AxisArray)) {
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

    return NpTransposeCodeValidator;
});

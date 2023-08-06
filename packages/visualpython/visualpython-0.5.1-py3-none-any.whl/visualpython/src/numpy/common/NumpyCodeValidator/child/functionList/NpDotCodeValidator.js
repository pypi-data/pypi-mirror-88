define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class NpDotCodeValidator
     * @constructor
    */
    var NpDotCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpDotCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
     * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
     * @param {Obejct} state 
    */
    NpDotCodeValidator.prototype.validate = function(state) {
        const { paramOption1
                , paramOption2
                , paramData
                , returnVariable

                , isReturnVariable
                , indentSpaceNum } = state;

        const { paramOneArray, paramTwoArray, paramThreeArray, paramScalar, paramVariable
                , param2OneArray, param2TwoArray, param2ThreeArray, param2Scalar, param2Variable } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        /**  return 변수 입력 값이 이상이 없거나,
         *   return 변수를 입력하지 않았다면 아래 코드로 넘어간다.
        */
        switch (paramOption1) {
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
            // param 옵션 3: n차원 array validation
            case "3" : {
                if (this.checkIsArrayLengthZero(paramThreeArray)) {
                    return false;
                }

                break;
            }
            // param 옵션 4: scalar 값 validaiton
            case "4" : { 
                if (this.checkIsNullString(paramScalar) || this.checkIsString(paramScalar)) {
                    return false;
                }

                break;
            }
            // param 옵션 5: 사용자 정의 함수 validation
            case "5" : { 
                if (this.checkIsNullString(paramVariable) || this.checkIsNumberString(paramVariable)
                    || this.checkisVarableReservedWord(paramVariable)) {
                    return false;
                };
                break;
            }
        }

        switch (paramOption2) {
            // param 옵션 6: 1차원 array validation
            case "1" : {
                if (this.validateOneArray(param2OneArray)) {
                    return false;
                }
                break;
            }
            // param 옵션 7: 2차원 array validation
            case "2" : {
                if (this.validateTwoArray(param2TwoArray)) {
                    return false;
                }
                break;
            }
            // param 옵션 8: n차원 array validation
            case "3" : {
                if (this.checkIsArrayLengthZero(param2ThreeArray)) {
                    return false;
                }

                break;
            }
            // param 옵션 9: scalar 값 validaiton
            case "4" : { 
                if (this.checkIsNullString(param2Scalar) || this.checkIsString(param2Scalar)) {
                    return false;
                }

                break;
            }
            // param 옵션 10: 사용자 정의 함수 validation
            case "5" : { 
                if (this.checkIsNullString(param2Variable) || this.checkIsNumberString(param2Variable)
                    || this.checkisVarableReservedWord(param2Variable)) {
                    return false;
                };
                break;
            }
        }
        return true;
    }

    return NpDotCodeValidator;
});

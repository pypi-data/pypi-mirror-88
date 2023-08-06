define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class NpMeanVarStdMaxMinMedianCodeValidator
     * @constructor
    */
    var NpMeanVarStdMaxMinMedianCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpMeanVarStdMaxMinMedianCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
     * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
     * @param {Obejct} state 
    */
    NpMeanVarStdMaxMinMedianCodeValidator.prototype.validate = function(state) {
        const { paramOption
                , paramData
                , returnVariable
                , dtype
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramOneArray, paramTwoArray, paramThreeArray, paramScalar, paramVariable } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }
        /**  return 변수 입력 값이 이상이 없거나,
         *   return 변수를 입력하지 않았다면 아래 코드로 넘어간다.
        */

        switch (paramOption) {
            // param 옵션 1: 1차원 array validation
            case "1" : {
                if (this.checkIsArrayLengthZero(paramOneArray)) {
                    return false;
                }
                
                break;
            }
            // param 옵션 2: 2차원 array validation
            case "2" : {
                if (this.checkIsArrayLengthZero(paramTwoArray)) {
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
        return true;
    }

    return NpMeanVarStdMaxMinMedianCodeValidator;
});

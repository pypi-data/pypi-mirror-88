define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";
    /**
     * @class NumpyIndexingCodeValidator
     * @constructor
    */
    var NumpyIndexingCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NumpyIndexingCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    * @return {boolean} true면 통과 false면 에러
    */
    NumpyIndexingCodeValidator.prototype.validate = function(state) {
        const { paramOption
                , paramData
                , callVariable
                , returnVariable
                , isReturnVariable
                , indentSpaceNum } = state;
        const { paramOption1Start, paramOption1End 
                , paramOption2RowStart, paramOption2RowEnd, paramOption2ColStart, paramOption2ColEnd
                , paramOption3Array } = paramData;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        /**  call variable: call variable 값이 입력되지 않았거나 or  예약어를 썼거나
        *                or  순수 문자열이 아닌 숫자 문자열로 되어 있으면 validation
        */
        if ( this.checkIsNullString(callVariable) || this.checkisVarableReservedWord(callVariable) 
            || this.checkIsNumberString(callVariable) ) {
            return false;
        }

        // numpy indexing parameter값은 없을 수도 있고,
        // numpy indexing parameter값은 문자가 올 수도 있고, 숫자가 올 수도 있음
        switch (paramOption) {
            case "1" : {
                if (this.checkisVarableReservedWord(paramOption1Start) ) {
                    return false;
                }
                if (this.checkisVarableReservedWord(paramOption1End) ) {
                    return false;
                }
                break;
            }
            case "2" : {
                if (this.checkisVarableReservedWord(paramOption2RowStart) ) {
                    return false;
                }
                if (this.checkisVarableReservedWord(paramOption2RowEnd) ) {
                    return false;
                }
                if (this.checkisVarableReservedWord(paramOption2ColStart) ) {
                    return false;
                }
                if (this.checkisVarableReservedWord(paramOption2ColEnd) ) {
                    return false;
                }

                break;
            }

            // Numpy Indexing N array validation
            case "3" : {
                if (this.checkIsArrayLengthZero(paramOption3Array)) {
                    return false;
                }

                var isValidationError = paramOption3Array.some(elementArray => {

                    // ex) n2array[], n2array[][] <-예시 처럼 [] 안에 아무 값도 없을때 validation
                    if(elementArray.length === 0){
                        this.alertErrorMessage('인덱싱 값을 넣어주세요');
                        return true;
                    }

                    // 파라미터를 제대로 작성하지 않았을 때
                    // 아래 예시처럼 != ( 다음에 파라미터를 작성하지 않은 미완성 상태일 때 validation
                    // ex) n2array[(a > b) != (]
                    if(elementArray.length !== 0 && elementArray.length % 2 !== 0){
                        this.alertErrorMessage('파라미터 작성을 완료해주세요');
                        return true;
                    }

                    var isError = false;
                    isError = elementArray.some((element, index) => {
                        // isDisable이 true 이면 value Null체크 검사를 하지 않고 건너뛴다.
                        if(element.isDisable === false && this.checkIsNullString(element.value)){
                            return true;
                        }
                        // index 0은 operator 키 값이 없음
                        // isDisable이 true 이면 operator Null체크 검사를 하지 않고 건너뛴다.
                        if(index > 0 && element.isDisable === false && this.checkisNullOperator(element.operator)){
                            return true;
                        }
                        return false;
                    });
                    if(isError === true) {
                        return true;
                    } else {
                        return false;
                    }
                });
                if(isValidationError === true) {
                    return false;
                } else {
                    return true;
                }

                break;
            }

            default : {
                break;
            }
        }
        return true;
    }

    return NumpyIndexingCodeValidator;

});

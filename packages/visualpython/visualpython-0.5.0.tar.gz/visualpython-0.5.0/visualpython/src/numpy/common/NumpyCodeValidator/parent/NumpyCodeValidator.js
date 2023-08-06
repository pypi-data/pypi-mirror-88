define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
], function(requirejs, vpCommon) {
    "use strict";

    /**
     * @class NumpyCodeValidator
     * @constructor
    */
    var NumpyCodeValidator = function() {

    };
    /** 자식 클래스에서 반드시! 오버라이드 되는 메소드
     *  nummpy 패키지에서 parameter 값 등을 검증하는 메소드.
     *  @param {Object} state
     */
    NumpyCodeValidator.prototype.validate = function(state) {
        /** FIXME: numpy에서 생성한 모든 state 입력값에 대해 검증하지 않음 */
        return true;
    }

    /** string 파라미터에 ""이 들어오는지 검사하는 함수
     *  ""이 들어온다는 것은 아무값도 입력하지 않았다는 뜻이므로 alertModal로 validation함
     * @param {string} string 
     * @param {string} msgString 
     */
    NumpyCodeValidator.prototype.checkIsNullString = function(string, msgString) { 
        if(string === ""){
            vpCommon.renderAlertModal(msgString || "변수나 파라미터 값을 입력해주세요"); 
            return true;
        } else {
            return false;
        }
    }
    /** numberString 파라미터에 문자열로 된 숫자가 들어오는지 검사하는 함수
     * 변수 이름을 validation할 때 사용
     * 변수 이름은 순수 문자열로 써야하는데 숫자 문자열로 쓰면 코드 실행시 에러가 나서 validation함
     * @param {string} numberString ex) "0" "120" "267" ...
     * @param {string} msgString 
     */
    NumpyCodeValidator.prototype.checkIsNumberString = function(numberString, msgString) { 
        if(!isNaN(parseInt(numberString))){
            vpCommon.renderAlertModal(msgString || "변수 이름에 숫자를 입력할 수 없습니다"); 
            return true;
        } else {
            return false;
        }
    }
    /** string 파라미터에 순수 문자열이 들어오는지 검사하는 함수
     * 숫자 값을 입력해야 하는 파라미터 검증할 때 사용
     * 숫자 문자열이 들어와야하는데, 순수 문자열이 들어오면 validation함
     * @param {string} string ex) "a" "array" "arrayVariable" ...
     * @param {string} msgString 
     */
    NumpyCodeValidator.prototype.checkIsString = function(string, msgString) { 
        if(isNaN(parseInt(string))){
            vpCommon.renderAlertModal(msgString || "파라미터에 문자를 입력할 수 없습니다"); 
            return true;
        } else {
            return false;
        }
    }
    /** array 파라미터 length가 0인지 확인하는 함수
     *  length가 0이면 배열 안에 입력한 데이터가 없으므로 validation함
     * @param {Array<number | string>} array 
     * @param {string} msgString 
     */
    NumpyCodeValidator.prototype.checkIsArrayLengthZero = function(array, msgString) { 
        if(array.length === 0){
            vpCommon.renderAlertModal(msgString || "파라미터 값을 입력해주세요"); 
            return true;
        } else {
            return false;
        }
    }

    /**
     * @param {Array<number | string>} array 
     * @param {string} msgString 
     */
    NumpyCodeValidator.prototype.validateOneArray = function(array, msgString) { 
        if (this.checkIsArrayLengthZero(array)) {
            return true;
        }
        var isValidationError = array.some(element => {
            if ( this.checkIsNullString(element) ) {
                return true;
            };
        });
        if(isValidationError){
            return true;
        }
    }

    /**
     * @param {Array<any>} array 
     * @param {string} msgString 
     */
    NumpyCodeValidator.prototype.validateOneArrayTypeString = function(array, msgString) { 
        if (this.checkIsArrayLengthZero(array)) {
            return true;
        }
        var isValidationError = array.some(element => {
            if ( this.checkIsNullString(element) || this.checkIsNumberString(element) || this.checkisVarableReservedWord(element) ) {
                return true;
            };
        });
        if(isValidationError){
            return true;
        }
    }

    /**
     * @param {Array<any>} array 
     * @param {string} msgString 
     */
    NumpyCodeValidator.prototype.validateOneArrayTypeNumber = function(array, msgString) { 
        if (this.checkIsArrayLengthZero(array)) {
            return true;
        }
        var isValidationError = array.some(element => {
            if ( this.checkIsNullString(element) || this.checkIsString(element) ) {
                return true;
            };
        });
        if(isValidationError){
            return true;
        }
    }

    /**
     * @param {Array<number | string>} array 
     * @param {string} msgString 
     */
    NumpyCodeValidator.prototype.validateTwoArray = function(array, msgString) { 
        if (this.checkIsArrayLengthZero(array)) {
            return true;
        }
        var isValidationError; 
        isValidationError = array.some(elementArray => {
            if(this.checkIsArrayLengthZero(elementArray)){
                return true;
            } else {
                var is = elementArray.some(element => {
                    if ( this.checkIsNullString(element) ) {
                        return true;
                    };
                });
                if(is === true) {
                    return true;
                }
            }
        });
        if(isValidationError){
            return true;
        }
    }
    /** 변수 이름으로 파이썬 예약어를 쓰면 syntax오류가 나기 때문에 validation함
     *  @param {string} string 
     *  @param {string} msgString 
     */
    NumpyCodeValidator.prototype.checkisVarableReservedWord = function(string, msgString) {
        if(string === "for" || string === "if" || string === "elif" || string === "else" || string === "while" || string === "as" || string === "def" || string === "class"
            || string === "in" || string === "return" || string === ":" || string === "$" || string === "import" || string === "try" || string === "catch" || string === "finally"
            || string === "break" || string === "continue" || string === "print") {
            vpCommon.renderAlertModal(msgString || "변수 이름에 예약어를 쓸 수 없습니다"); 
            return true;
        }
    }

    /** "array" "100" 같이 문자열 값이 "" 혹은 '' 따옴표로 되어있어 있지 않는 경우 validation함 
     *  @param {string} string 
     *  @param {string} msgString 
     */
    NumpyCodeValidator.prototype.checkisNotParamElementDoubleQuotesString = function(string, msgString) {
        const a = '"';

        if (isNaN(parseInt(string))) {
            if (string[0] === `"` && string[1] === `"` && string[string.length - 1] === `"` && string[string.length - 2] === `"`) {
                // console.log("check1", string, string[0] === `"`, string[1] === `"`,string[string.length - 1] === `"`,string[string.length - 2] === `"`);
                return false;
            } else if(string[0] === `'` && string[1] === `'` && string[string.length - 1] === `'` && string[string.length - 2] === `'`) {
                // console.log("check2", string, string[0] === `'`, string[1] === `'`,string[string.length - 1] === `'`,string[string.length - 2] === `'`);
                return false;
            } else {
                // console.log("string", string);
                vpCommon.renderAlertModal(msgString || "문자 요소값에 따옴표를 붙여야 합니다"); 
                return true;
            }
        } else {
            return false;
        }
    }


    /**
     *  @param {string} string 
     *  @param {string} msgString 
     */
    NumpyCodeValidator.prototype.checkisNullOperator = function(string, msgString) {
        if(string === ""){
            vpCommon.renderAlertModal(msgString || "연산자를 입력해주세요"); 
            return true;
        } else {
            return false;
        }
    }

    /** alert message를 띄운다
     *  @param {string} msgString 
     */
    NumpyCodeValidator.prototype.alertErrorMessage = function(msgString) {
        vpCommon.renderAlertModal(msgString); 
        return true;
    }

    return NumpyCodeValidator;
});

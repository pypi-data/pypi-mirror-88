define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class NpTCodeValidator
     * @constructor
    */
    var NpTCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    NpTCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
    * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
    * @param {Obejct} state 
    * @return {boolean} true면 통과 false면 에러
    */
    NpTCodeValidator.prototype.validate = function(state) {
        const { returnVariable
                , callVariable
                , isReturnVariable
                , indentSpaceNum } = state;

        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }
        /**  call variable: call variable 값이 입력되지 않았거나 or  예약어를 썼거나
        *                or  순수 문자열이 아닌 숫자 문자열로 되어 있으면 validation
        */
        // if ( this.checkIsNullString(callVariable) || this.checkisVarableReservedWord(callVariable) 
        //     || this.checkIsNumberString(callVariable) ) {
        //     return false;
        // }

        return true;
    }

    return NpTCodeValidator;
});

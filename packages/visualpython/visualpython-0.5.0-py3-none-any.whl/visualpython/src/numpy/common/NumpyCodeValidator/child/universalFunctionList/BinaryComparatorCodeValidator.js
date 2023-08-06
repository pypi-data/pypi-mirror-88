define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeValidator/parent/NumpyCodeValidator'
], function(requirejs, vpCommon, 
            NumpyCodeValidator ) {
    "use strict";

    /**
     * @class BinaryComparatorCodeValidator
     * @constructor
    */
    var BinaryComparatorCodeValidator = function() {

    };

    /**
     * NumpyCodeValidator 에서 상속
    */
    BinaryComparatorCodeValidator.prototype = Object.create(NumpyCodeValidator.prototype);

    /**
     * NumpyCodeValidator 클래스의 makeCode 메소드 오버라이드
     * @param {Obejct} state 
    */
    BinaryComparatorCodeValidator.prototype.validate = function(state) {
        return true;
    }

    return BinaryComparatorCodeValidator;
});

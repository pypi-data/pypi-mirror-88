define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/pandas/common/commonPandas'
    , 'nbextensions/visualpython/src/common/vpMakeDom'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    
], function ( $, vpCommon, vpConst, sb, 
              vpFuncJS, libPandas, vpMakeDom,
              api, config, constData, blockRenderer ) {


    var DomPool = function(uuid) {
        this.domList = []
    }
    // /**
    //  * vpFuncJS 에서 상속
    // */
    // // DomPool.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    // /**
    //  * 유효성 검사
    //  * @returns 유효성 검사 결과. 적합시 true
    // */
    // DomPool.prototype.optionValidation = function() {
    //     return true;
    // }
    DomPool.prototype.makeDom = function() {

    }

    return DomPool;
});


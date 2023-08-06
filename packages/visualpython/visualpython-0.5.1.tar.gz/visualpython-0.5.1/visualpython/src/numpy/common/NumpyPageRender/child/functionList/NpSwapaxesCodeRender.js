define ([
    'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'
], function( NumpyPageRender ) {

    'use strict';
    /**
     * @class NpSwapaxesCodeRender
     * @constructor
    */
    var NpSwapaxesCodeRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyAxisArray, numpyIndexValueArray, numpyEnumRenderEditorFuncType, 
                numpyTrueFalseArray, numpyRavelOrderArray } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyAxisArray = numpyAxisArray;
        this.numpyIndexValueArray = numpyIndexValueArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;
        this.numpyTrueFalseArray = numpyTrueFalseArray
        this.numpyRavelOrderArray = numpyRavelOrderArray;
        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
    */
    NpSwapaxesCodeRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    */
    NpSwapaxesCodeRender.prototype.pageRender = function(tagSelector) {
        const {  PARAM_INPUT_EDITOR_TYPE } = this.numpyEnumRenderEditorFuncType;
        this.rootTagSelector = tagSelector || this.getMainPageSelector();

        var numpyPageRenderThis = this;

        this.renderPrefixCode();
        
        this.renderRequiredInputOutputContainer();
        this.renderParamVarBlock();
        var bindFuncData = {
            numpyPageRenderThis: numpyPageRenderThis
            , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
            , stateParamNameStrOrStrArray: ['paramAxis1', 'paramAxis2'] 
            , paramNameStrArray: ['Axis1','Axis2']
            , placeHolderArray: ['숫자 입력', '숫자 입력']
        }

        /** 옵션 창 */
        this.renderAdditionalOptionContainer();
        this.renderInputIndexValueBlock('Input Axis', bindFuncData);
        this.renderReturnVarBlock();

        /** userOption 창 */
        this.renderUserOption();

        this.renderPostfixCode();
    }

    return NpSwapaxesCodeRender;
});

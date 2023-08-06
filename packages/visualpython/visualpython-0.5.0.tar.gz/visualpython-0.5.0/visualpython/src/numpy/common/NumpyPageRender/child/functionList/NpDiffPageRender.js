define ([
    'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'
], function( NumpyPageRender ) {

    'use strict';
    /**
     * @class NpDiffPageRender
     * @constructor
    */
    var NpDiffPageRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyAxisArray, numpyIndexValueArray, numpyEnumRenderEditorFuncType } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyAxisArray = numpyAxisArray;
        this.numpyIndexValueArray = numpyIndexValueArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;
        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
    */
   NpDiffPageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    */
    NpDiffPageRender.prototype.pageRender = function(tagSelector) {
        const { PARAM_INPUT_EDITOR_TYPE } = this.numpyEnumRenderEditorFuncType;

        this.rootTagSelector = tagSelector || this.getMainPageSelector();
        var numpyPageRenderThis = this;
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();
        // state의 paramData 객체의 키값을 string 배열로 리턴
        var stateParamNameStrArray = Object.keys(numpyStateGenerator.getState('paramData'));
        var bindFuncData = {
            numpyPageRenderThis: numpyPageRenderThis
            , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
            , stateParamNameStrOrStrArray: [stateParamNameStrArray[0]] 
            , paramNameStrArray: ['index N']
            , placeHolderArray: ['숫자 입력']
        }

        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderParamVarBlock();

        this.renderAdditionalOptionContainer();
        this.renderSelectIndexValueBlock('Input N index', bindFuncData);
        this.renderReturnVarBlock();

        /** userOption 창 */
        this.renderUserOption();

        this.renderPostfixCode();
    }

    return NpDiffPageRender;
});

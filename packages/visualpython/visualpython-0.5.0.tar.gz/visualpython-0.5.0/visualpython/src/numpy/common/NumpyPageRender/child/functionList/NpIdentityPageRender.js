define ([
    'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'
], function( NumpyPageRender ) {

    'use strict';
    /**
     * @class NpIdentityPageRender
     * @constructor
    */
    var NpIdentityPageRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyIndexValueArray, numpyEnumRenderEditorFuncType } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyIndexValueArray = numpyIndexValueArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;
        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
    */
    NpIdentityPageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    */
    NpIdentityPageRender.prototype.pageRender = function(tagSelector) {
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
            , paramNameStrArray: ['n행 x n열']
            , placeHolderArray: ['숫자 n 입력']
        }
        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderInputIndexValueBlock('Input Parameter Int Number', bindFuncData);

        /** 옵션 창 */
        this.renderAdditionalOptionContainer();
        this.renderDtypeBlock();
        this.renderReturnVarBlock();
        
        /** userOption 창 */
        this.renderUserOption();

        this.renderPostfixCode();
    }

    return NpIdentityPageRender;
});

define ([
    'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'
], function( NumpyPageRender ) {

    'use strict';
    /**
     * @class NpFullPageRender
     * @constructor
    */
    var NpFullPageRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyEnumRenderEditorFuncType } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;
        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
    */
    NpFullPageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    */
    NpFullPageRender.prototype.pageRender = function(tagSelector) {
        this.rootTagSelector = tagSelector || this.getMainPageSelector();

        var numpyPageRenderThis = this;
        const { PARAM_INPUT_EDITOR_TYPE, PARAM_ONE_ARRAY_INDEX_N_EDITOR_TYPE } = this.numpyEnumRenderEditorFuncType;
        // state의 paramData 객체의 키값을 string 배열로 리턴
        var stateParamNameStrArray = Object.keys(this.numpyStateGenerator.getState('paramData'));
        var tabTitle = 'Input Parameter';
        var tabBlockArray = [
            {
                tabNumber: 1
                , btnText: '1D Array '
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [stateParamNameStrArray[0]]
                    , paramNameStrArray: ['길이']
                    , placeHolderArray: ['숫자 입력']
                }
            },
            {
                tabNumber: 2
                , btnText: '2D Array'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [ stateParamNameStrArray[1], stateParamNameStrArray[2]]
                    , paramNameStrArray: ['행','열']
                    , placeHolderArray: ['숫자 입력', '숫자 입력']
                }
            },
            {
                tabNumber: 3
                , btnText: 'ND Array'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_ONE_ARRAY_INDEX_N_EDITOR_TYPE
                    , stateParamNameStrOrStrArray:  stateParamNameStrArray[3]
                }
            }
        ];
        var tabDataObj = {
            tabTitle,
            tabBlockArray
        }

        var bindFuncData = {
            numpyPageRenderThis: numpyPageRenderThis
            , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
            , stateParamNameStrOrStrArray: ['indexValue'] 
            , paramNameStrArray: ['배열에 채워 넣을 값']
            , placeHolderArray: ['숫자 입력']
        }

        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderParamTabBlock(tabDataObj);
        this.renderInputIndexValueBlock('Input Ndarray Value', bindFuncData);
        /** 옵션 창 */
        this.renderAdditionalOptionContainer();

        this.renderDtypeBlock();
        this.renderReturnVarBlock();

        /** userOption 창 */
        this.renderUserOption();

        this.renderPostfixCode();
    }

    return NpFullPageRender;
});

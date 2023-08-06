define ([
    'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'

    , 'nbextensions/visualpython/src/numpy/constData'
], function( NumpyPageRender
            , constData ) {
    const { STATE_paramOneArray
            , STATE_paramTwoArray
            , STATE_paramThreeArray
            , STATE_paramScalar
            , STATE_paramVariable } = constData;
    'use strict';
    /**
     * @class NpArrayPageRender
     * @constructor
    */
    var NpArrayPageRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyEnumRenderEditorFuncType } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;

        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
    */
    NpArrayPageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    */
    NpArrayPageRender.prototype.pageRender = function(tagSelector) {

        this.rootTagSelector = tagSelector || this.getMainPageSelector();
        var numpyPageRenderThis = this;
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();


        var tabTitle = 'Input Parameter';
        const { PARAM_ONE_ARRAY_EDITOR_TYPE, PARAM_TWO_ARRAY_EDITOR_TYPE,
                PARAM_THREE_ARRAY_EDITOR_TYPE, PARAM_INPUT_EDITOR_TYPE } = this.numpyEnumRenderEditorFuncType;
        var tabBlockArray = [
            {
                tabNumber: 1
                , btnText: '1D Array'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_ONE_ARRAY_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: STATE_paramOneArray
                }
            },
            {
                tabNumber: 2
                , btnText: '2D Array'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_TWO_ARRAY_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: STATE_paramTwoArray
                }
            },
            {
                tabNumber: 3
                , btnText: '3D Array'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_THREE_ARRAY_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: STATE_paramThreeArray
                }
            },
            {
                tabNumber: 4
                , btnText: 'Scalar Value'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [ STATE_paramScalar ]
                    , paramNameStrArray: ['스칼라 값']
                    , placeHolderArray: ['숫자 입력']
                }
   
            },
            {
                tabNumber: 5
                , btnText: 'Param Variable'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [ STATE_paramVariable ]
                    , paramNameStrArray: ['변수']
                    , placeHolderArray: ['변수 입력']
                }
            }
        ];
        
        var tabDataObj = {
            tabTitle,
            tabBlockArray
        }
    
        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderParamTabBlock(tabDataObj);

        this.renderAdditionalOptionContainer();
        this.renderDtypeBlock();
        this.renderReturnVarBlock();
        
        /** userOption 창 */
        this.renderUserOption();
        
        this.renderPostfixCode();
    }

    return NpArrayPageRender;
});

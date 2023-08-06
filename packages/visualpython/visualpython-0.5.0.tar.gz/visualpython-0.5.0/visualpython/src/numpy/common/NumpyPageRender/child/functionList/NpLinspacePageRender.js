define ([
    'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'
], function( NumpyPageRender ) {

    'use strict';
    /**
     * @class NpLinspacePageRender
     * @constructor
    */

    var NpLinspacePageRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyAxisArray, numpyIndexValueArray, numpyEnumRenderEditorFuncType, numpyTrueFalseArray } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyAxisArray = numpyAxisArray;
        this.numpyIndexValueArray = numpyIndexValueArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;
        this.numpyTrueFalseArray = numpyTrueFalseArray;
        NumpyPageRender.call(this);
    };
    /**
     * NumpyPageRender 에서 상속
    */
    NpLinspacePageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    */
    NpLinspacePageRender.prototype.pageRender = function(tagSelector) {
        const {  PARAM_INPUT_EDITOR_TYPE } = this.numpyEnumRenderEditorFuncType;
        this.rootTagSelector = tagSelector || this.getMainPageSelector();
        var numpyPageRenderThis = this;
        // state의 paramData 객체의 키값을 string 배열로 리턴
        var stateParamNameStrArray = Object.keys(this.numpyStateGenerator.getState('paramData'));
        var bindFuncData = {
            numpyPageRenderThis: numpyPageRenderThis
            , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
            , stateParamNameStrOrStrArray:[stateParamNameStrArray[0], stateParamNameStrArray[1], stateParamNameStrArray[2]]
            , paramNameStrArray: ['Start','Stop','Num']
            , placeHolderArray: ['숫자 입력', '숫자 입력','숫자 입력']
        }

        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderInputIndexValueBlock('Input Parameter', bindFuncData);

        /** 옵션 창 */
        this.renderAdditionalOptionContainer();
        // this.renderSelectIndexValueBlock('Select endpoint retstep', [
        //     {
        //         stateParamName: stateParamNameStrArray[3]
        //          , optionDataList: this.numpyTrueFalseArray
        //          ,selectParamName: 'endpoint'
        //     },
        //     {
        //         stateParamName: stateParamNameStrArray[4]
        //          , optionDataList: this.numpyTrueFalseArray
        //          , selectParamName: 'retstep'
        //     }
        // ]);
        this.renderSelectIndexValueBlock('Select endpoint', {
            stateParamName: stateParamNameStrArray[3]
             , optionDataList: this.numpyTrueFalseArray
             ,selectParamName: 'endpoint'
        });
        this.renderSelectIndexValueBlock('Select retstep', {
            stateParamName: stateParamNameStrArray[4]
            , optionDataList: this.numpyTrueFalseArray
            , selectParamName: 'retstep'
        });
        //     {
        //         stateParamName: stateParamNameStrArray[3]
        //          , optionDataList: this.numpyTrueFalseArray
        //          ,selectParamName: 'endpoint'
        //     },
        //     {
        //         stateParamName: stateParamNameStrArray[4]
        //          , optionDataList: this.numpyTrueFalseArray
        //          , selectParamName: 'retstep'
        //     }
        // ]);
        this.renderReturnVarBlock();
        
        /** userOption 창 */
        this.renderUserOption();

        this.renderPostfixCode();
    }

    return NpLinspacePageRender;
});

define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ){

    /**
     * @param {Object} tabDataObj 
     *      value1 {string} tabTitle ,
     *      value2 {Array<object>} tabBlockArray
     */
    var renderParamTitle = function(tabDataObj) {
        var tabTitle = tabDataObj.tabTitle;
        // var numpyBlock = $(`<div class='vp-numpy-option-block vp-spread' 
        //                          id='vp_blockArea'>
        //                     </div>`);
        // var numpyBlockTitle = $(`<div style='margin-top: 9px;
        //                                      margin-bottom: 9px;    
        //                                      font-size: 13px;'>
        //                             <span class='vp-multilang' 
        //                                   data-caption-id='${tabTitle}'>
                           
        //                             </span>
        //                         </div>`);
    //     <td>
    //     <div class='vp-numpy-requiredPageBlock-view'>
    //     </div>
    // </td>
         var numpyBlock = $(`<tr class='class='vp-numpy-option-block'>
                                <th>${tabTitle}</th>
                            
                            </tr>`);
        var numpyBlockTd =  $(`<td></td>`);
        numpyBlock.append(numpyBlockTd);
        return {
            numpyBlock, numpyBlockTd
        };
    }

    /**
     * @param {Document} numpyBlock 
     * @param {Object} tabDataObj 
     *      value1 {string} tabTitle ,
     *      value2 {Array<object>} tabBlockArray
     * @param {string} uuid 
     */
    var renderParamTabButtonBlock = function(numpyPageRenderThis, numpyBlock, tabDataObj, uuid) {
        const STR_SELECTED = 'selected';
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();
        var stateParamOptionName = tabDataObj.stateParamOptionName || 'paramOption';
        var paramOptionNum = -1;
        if (stateParamOptionName) {
            var paramOption = numpyStateGenerator.getState(stateParamOptionName);
            paramOptionNum = parseInt(paramOption);
        }
   
        
        var buttonContainer = $(`<select class='vp-numpy-tab vp-numpy-style-flex-row-around' 
                                      id='vp_numpyTabSelect${uuid}'></select>`);
        var tabBlockArray = tabDataObj.tabBlockArray;
        for (var i = 0; i < tabBlockArray.length; i++) {
            (function(j) {
                var isCheckedStr = '';
                if (paramOptionNum == j + 1) {
                    isCheckedStr = STR_SELECTED;
                }
                const { btnText } = tabBlockArray[j];
                var buttonDom = $(`<option class='vp-numpy-func_btn vp-numpy-padding-1rem 
                                                  vp-numpyTabBtn-${uuid}-${j+1} black' 
                                           value='${j}'
                                           ${isCheckedStr}
                           
                                    style='display: inline-block;'>
                                        <span class='vp-multilang' 
                                                    data-caption-id='${btnText}'>
                                            ${btnText}
                                        </span>
                                    </option>`);
                buttonContainer.append(buttonDom);
            })(i);
        }
        numpyBlock.append(buttonContainer);
    }

    /**
     * @param {Document} numpyBlock 
     * @param {Object} tabDataObj 
     *      value1 {string} tabTitle ,
     *      value2 {Array<object>} tabBlockArray
     * @param {string} uuid 
     */
    var renderParamTabViewBlock = function(numpyBlock, tabDataObj, uuid) {
        var viewContainer = $(`<div class='vp-numpy-tab' id='vp_numpyTab'>`);
        var tabBlockArray = tabDataObj.tabBlockArray;
        for (var i = 0; i < tabBlockArray.length; i++) {
            (function(j) {
                const { btnText } = tabBlockArray[j];
                var viewDom = $(`<div class='vp-numpy-tab-block-element-${uuid}-${j+1} 
                                    vp-numpy-tab-block-element-${uuid}' 
                                      id='vp_numpyTabBlock'>
                      
                                        <div class='vp-numpy-tab-block-element-${uuid}-${j+1}-view'>
                                        </div>
                                    </div>`);
                viewContainer.append(viewDom);                    
            })(i);
        }
        numpyBlock.append(viewContainer);
    }

    /**
     * 
     * @param {numpyPageRender this} numpyPageRenderThis 
     * @param {Object} tabDataObj 
     *      value1 {string} tabTitle ,
     *      value2 {Array<object>} tabBlockArray
     * @param {string} uuid 
     */
    var bindParamEditorFunc = function( numpyPageRenderThis, tabDataObj, uuid ) {
        var _mapNumpyPageRenderFunc = function(tagSelector, tabBlockArray) {
            const { bindFuncData } = tabBlockArray;
            const { numpyPageRenderThis, numpyPageRenderFuncType, stateParamNameStrOrStrArray } = bindFuncData;
            const { PARAM_ONE_ARRAY_EDITOR_TYPE, PARAM_TWO_ARRAY_EDITOR_TYPE,
                    PARAM_THREE_ARRAY_EDITOR_TYPE, PARAM_INPUT_EDITOR_TYPE, PARAM_ONE_ARRAY_INDEX_N_EDITOR_TYPE } 
                    = numpyPageRenderThis.numpyEnumRenderEditorFuncType;
     
            switch(numpyPageRenderFuncType){
                case PARAM_ONE_ARRAY_EDITOR_TYPE: {
                    numpyPageRenderThis.renderParamOneArrayEditor(tagSelector, stateParamNameStrOrStrArray);
                    break;
                }
                case PARAM_TWO_ARRAY_EDITOR_TYPE: {
                    numpyPageRenderThis.renderParamTwoArrayEditor(tagSelector, stateParamNameStrOrStrArray);
                    break;
                }
                case PARAM_THREE_ARRAY_EDITOR_TYPE: {
                    numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamNameStrOrStrArray);
                    break;
                }
                case PARAM_INPUT_EDITOR_TYPE: {
                    numpyPageRenderThis.renderParamInputArrayEditor(tagSelector, bindFuncData);
                    break;
                }
                case PARAM_ONE_ARRAY_INDEX_N_EDITOR_TYPE: {
                    numpyPageRenderThis.renderParamOneArrayIndexValueEditor(tagSelector, stateParamNameStrOrStrArray);
                    break;
                }

                // case PARAM_INDEXING_EDITOR_TYPE: {
                    // numpyPageRenderThis.renderIndexingEditor(tagSelector, stateParamNameStrOrStrArray);
                    // break;
                // }
            }
        }
        
        var numpyPageRenderThis = numpyPageRenderThis;
        var importPackageThis = numpyPageRenderThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();
        var tabBlockArray = tabDataObj.tabBlockArray;
        var stateParamOptionName = tabDataObj.stateParamOptionName || 'paramOption';

        $(document).off('change', '#' + `vp_numpyTabSelect${uuid}`);
        $(document).on('change', '#' + `vp_numpyTabSelect${uuid}`, function(event) {
            const STR_COLON_SELECTED = ':selected';
            var selectedValue = parseInt($(STR_COLON_SELECTED, this).val());
            // console.log('selectedValue',selectedValue);

            $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}`)).css('display','none');
            $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}-${selectedValue+1}`)).css('display','block');

            var tagSelector = `.vp-numpy-tab-block-element-${uuid}-${selectedValue+1}-view`;
      
            _mapNumpyPageRenderFunc(tagSelector, tabBlockArray[selectedValue]);

            numpyStateGenerator.setState({
                [`${stateParamOptionName}`]: `${selectedValue+1}`
            });
        });

        if (stateParamOptionName) { 
            var paramOption = numpyStateGenerator.getState(stateParamOptionName);
            var paramOptionNum = parseInt(paramOption);
            _mapNumpyPageRenderFunc(`.vp-numpy-tab-block-element-${uuid}-${paramOptionNum}-view`, tabBlockArray[paramOptionNum-1]);
       
            $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}`)).css('display','none');
            $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}-${paramOptionNum}`)).css('display','block');
    
        } 

        // html init render  init HTML 초기 설정
        _mapNumpyPageRenderFunc(`.vp-numpy-tab-block-element-${uuid}-${paramOptionNum}-view`, tabBlockArray[paramOptionNum-1]);
       
        $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}`)).css('display','none');
        $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}-${paramOptionNum}`)).css('display','block');
        // _mapNumpyPageRenderFunc(`.vp-numpy-tab-block-element-${uuid}-1-view`, tabBlockArray[0]);
       
        // $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}`)).css('display','none');
        // $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}-1`)).css('display','block');
        
    }

    /**
     * 
     * @param {numpyPageRender this} numpyPageRenderThis 
     * @param {Object} tabDataObj 
     *      value1 {string} tabTitle ,
     *      value2 {Array<object>} tabBlockArray
     */
    var renderParamTabBlock = function(numpyPageRenderThis, tabDataObj) {
        var uuid = vpCommon.getUUID();
        var numpyPageRenderThis = numpyPageRenderThis
        var importPackageThis = numpyPageRenderThis.getImportPackageThis();
        var rootTagSelector = numpyPageRenderThis.getRequiredPageSelector();
        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));
    
        const{numpyBlock, numpyBlockTd} = renderParamTitle(tabDataObj);
        // var numpyBlock = $(`<div class='vp-numpy-option-block vp-spread' 
        //                          id='vp_blockArea'>
        //                     </div>`);

        renderParamTabButtonBlock(numpyPageRenderThis, numpyBlockTd, tabDataObj, uuid);
        renderParamTabViewBlock(numpyBlockTd, tabDataObj, uuid);

        mainPage.append(numpyBlock);

        bindParamEditorFunc(numpyPageRenderThis, tabDataObj, uuid);
    }

    return renderParamTabBlock;
});

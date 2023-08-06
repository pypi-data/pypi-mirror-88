define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'
    , 'nbextensions/visualpython/src/common/component/vpTableLayoutVerticalSimple'
    , 'nbextensions/visualpython/src/common/component/vpTableLayoutHorizontalSimple'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb, vpSuggestInputText, vpTableLayoutVerticalSimple, vpTableLayoutHorizontalSimple

              , api
              , config
              , constData
              , blockRenderer
              , baseComponent ) {

    const { ChangeOldToNewState
        , FindStateValue

        , CreateOneArrayValueAndGet
        , UpdateOneArrayValueAndGet
        , DeleteOneArrayValueAndGet

        , DestructureFromBlockArray

        , MakeFirstCharToUpperCase
        , MapTypeToName
        , RemoveSomeBlockAndGetBlockList
        , ShuffleArray
        , GetImageUrl
        , ControlToggleInput } = api;

    const { PROCESS_MODE } = config;

    const { GenerateIfConditionList, RenderInputRequiredColor, RenderSelectRequiredColor } = blockRenderer;

    const { BLOCK_DIRECTION
            , BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE

            , IF_BLOCK_CONDITION_TYPE
            , IF_BLOCK_SELECT_VALUE_ARG_TYPE

            , STR_COLON_SELECTED
            , STR_NULL
            , STR_FOR
            , STR_INPUT
            , STR_SELECTED 
            , STR_DISABLED
            , STR_CLICK
            , STR_CHANGE
            , STR_CHANGE_KEYUP_PASTE

            , STR_VARIABLE
            , STR_OPERATOR

            , STATE_ifConditionList
            , STATE_elifConditionList

            , VP_CLASS_STYLE_FLEX_ROW
            , VP_CLASS_STYLE_FLEX_ROW_CENTER    
            , VP_CLASS_STYLE_FLEX_ROW_BETWEEN

            , VP_CLASS_STYLE_WIDTH_5PERCENT
            , VP_CLASS_STYLE_WIDTH_10PERCENT
            , VP_CLASS_STYLE_WIDTH_15PERCENT
            , VP_CLASS_STYLE_WIDTH_20PERCENT
            , VP_CLASS_STYLE_WIDTH_25PERCENT
            , VP_CLASS_STYLE_WIDTH_30PERCENT
            , VP_CLASS_STYLE_WIDTH_35PERCENT
            , VP_CLASS_STYLE_WIDTH_40PERCENT
            , VP_CLASS_STYLE_WIDTH_45PERCENT
            , VP_CLASS_STYLE_WIDTH_50PERCENT
            , VP_CLASS_STYLE_WIDTH_55PERCENT
            , VP_CLASS_STYLE_WIDTH_60PERCENT
            , VP_CLASS_STYLE_WIDTH_65PERCENT
            , VP_CLASS_STYLE_WIDTH_70PERCENT
            , VP_CLASS_STYLE_WIDTH_75PERCENT
            , VP_CLASS_STYLE_WIDTH_80PERCENT
            , VP_CLASS_STYLE_WIDTH_85PERCENT
            , VP_CLASS_STYLE_WIDTH_90PERCENT
            , VP_CLASS_STYLE_WIDTH_95PERCENT
            , VP_CLASS_STYLE_WIDTH_100PERCENT

            , VP_CLASS_STYLE_BGCOLOR_C4C4C4

            , VP_CLASS_STYLE_OPACITY_0
            , VP_CLASS_STYLE_OPACITY_1

            , VP_CLASS_STYLE_MARGIN_LEFT_15PX

            , VP_ID_PREFIX
            , VP_ID_APIBLOCK_OPTION_IF_ARG
            , VP_ID_APIBLOCK_OPTION_IF_ARG_1
            , VP_ID_APIBLOCK_OPTION_IF_ARG_2
            , VP_ID_APIBLOCK_OPTION_IF_ARG_3
            , VP_ID_APIBLOCK_OPTION_IF_ARG_4
            , VP_ID_APIBLOCK_OPTION_IF_ARG_5
            , VP_ID_APIBLOCK_OPTION_IF_ARG_6
            , VP_ID_APIBLOCK_OPTION_IF_USER_INPUT
            , VP_ID_APIBLOCK_OPTION_IF_PLUS
            , VP_ID_APIBLOCK_OPTION_IF_PLUS_USER_INPUT
            , VP_ID_APIBLOCK_OPTION_IF_DELETE

            , COMPARISON_OPERATOR_IF_ARG2
            , COMPARISON_OPERATOR_IF_ARG4
            , COMPARISON_OPERATOR_IF_ARG6 } = constData;

    const { MakeOptionContainer
            , MakeOptionDeleteButton
            , MakeOptionPlusButton
            , MakeVpSuggestInputText_apiblock
            , MakeOptionInput
            , MakeOptionSelectBox } = baseComponent;

            var InitIfBlockOption = function(thatBlock, optionPageSelector) {
                var uuid = thatBlock.getUUID();
                var blockContainerThis = thatBlock.getBlockContainerThis();
                var ifConditionListState = thatBlock.getState(STATE_ifConditionList);  
           
                /** --------------------------------- If Option 이벤트 함수 바인딩 ---------------------------------- */           
        
                /** if 변경 이벤트 함수 바인딩 */
                ifConditionListState.forEach( ( condition, index ) => {
                    var uuid = thatBlock.getUUID();
                    const { conditionType } = condition;
    
   /**
                         * @event_function
                         * iF arg2 선택 변경 
                         */
                        $(document).off(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid);
                        $(document).on(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid, function(event) {
                            // RenderInputRequiredColor(this);
                            var ifConditionListState = thatBlock.getState(STATE_ifConditionList);
                            var ifConditionState = ifConditionListState[index];
                            var selectedValue = $(STR_COLON_SELECTED, this).val();
                            if (selectedValue == 'none') {
                                selectedValue = STR_NULL;
                            }
                            var updatedValue = {
                                ...ifConditionState
                                ,arg2: selectedValue
                            }
                            ifConditionListState = UpdateOneArrayValueAndGet(ifConditionListState, index, updatedValue);
                            thatBlock.setState({
                                ifConditionList: ifConditionListState
                            });

                            var whileBlockCode = GenerateIfConditionList(thatBlock);
                            $(`.vp-block-header-${uuid}`).html(whileBlockCode);
                            blockContainerThis.renderBlockOptionTab();
                            event.stopPropagation();
                        });

                        /**
                         * @event_function
                         * iF arg4 선택 변경 
                         */
                        $(document).off(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid);
                        $(document).on(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid, function(event) {
                            // RenderInputRequiredColor(this);
                            var ifConditionListState = thatBlock.getState(STATE_ifConditionList);
                            var ifConditionState = ifConditionListState[index];
                            var selectedValue = $(STR_COLON_SELECTED, this).val();
                            if (selectedValue == 'none') {
                                selectedValue = STR_NULL;
                            }
                            var updatedValue = {
                                ...ifConditionState
                                ,arg4: selectedValue
                            }
                            ifConditionListState = UpdateOneArrayValueAndGet(ifConditionListState, index, updatedValue);
                            thatBlock.setState({
                                ifConditionList: ifConditionListState
                            });

                            var whileBlockCode = GenerateIfConditionList(thatBlock);
                            $(`.vp-block-header-${uuid}`).html(whileBlockCode);
                            blockContainerThis.renderBlockOptionTab();
                            event.stopPropagation();
                        });
                    // IF_BLOCK_CONDITION_TYPE
                    if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                        for (var k = 1; k < 7; k++) {
                            ((i) => {
            
                                /** arg1 arg2 arg3 arg4 arg5 arg6 */
                                /** If arg input 입력 변경 이벤트 함수 바인딩 */
                                    $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG +i+ index + uuid);
                                    $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG +i+ index + uuid, function(event) {
                            
                                        var ifConditionListState = thatBlock.getState(STATE_ifConditionList);
                                        var ifConditionState = ifConditionListState[index];
                                        var inputValue = $(this).val();
            
                                        var updatedValue;
                                        if (i == 1) {
                                            updatedValue = {
                                                ...ifConditionState
                                                , arg1: inputValue
                                            }
                                            // RenderInputRequiredColor(this);
                                        } else if (i == 2) {
                                            updatedValue = {
                                                ...ifConditionState
                                                , arg2: inputValue 
                                            }
                                            // RenderInputRequiredColor(this);
                                        } else if (i == 3) {
                                            updatedValue = {
                                                ...ifConditionState
                                                , arg3: inputValue 
                                            }
                                            // RenderInputRequiredColor(this);
                                        }  else if (i == 4) {
                                            
                                            updatedValue = {
                                                ...ifConditionState
                                                ,arg4: inputValue
                                            }
                                            if (inputValue == '') {
                                                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid).addClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                                                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).addClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                                                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).attr("disabled", true);
                                            } else {
                                                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid).removeClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                                                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).removeClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                                                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).attr("disabled", false);
                                            }
                                        } else if (i == 5) {
                                            updatedValue = {
                                                ...ifConditionState
                                                , arg5: inputValue 
                                            }
                                        } else {
                                            updatedValue = {
                                                ...ifConditionState
                                                , arg6: inputValue
                                            }
                                            // RenderInputRequiredColor(this);
                                        }
            
                                        ifConditionListState = UpdateOneArrayValueAndGet(ifConditionListState, index, updatedValue);
                                        thatBlock.setState({
                                            ifConditionList: ifConditionListState
                                        });
                                        var ifConditionCode = GenerateIfConditionList(thatBlock,BLOCK_CODELINE_TYPE.IF);
                                        $(`.vp-block-header-${thatBlock.getUUID()}`).html(ifConditionCode);
                                    
                                        event.stopPropagation();
                                    });
                
                            })(k);
                        }       
                    } else {
                        /** codeline arg6 */
                        /** If USER input 변경 이벤트 함수 바인딩 */
                        $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_USER_INPUT + index + uuid);
                        $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_USER_INPUT + index + uuid, function(event) {
                 
                            // RenderInputRequiredColor(this);
                   
                            var ifConditionListState = thatBlock.getState(STATE_ifConditionList);
                            var ifConditionState = ifConditionListState[index];
                            var inputValue = $(this).val();
        
                            var updatedValue= {
                                ...ifConditionState
                                , codeLine: inputValue
                            }
                       
        
                            ifConditionListState = UpdateOneArrayValueAndGet(ifConditionListState, index, updatedValue);
                            thatBlock.setState({
                                ifConditionList: ifConditionListState
                            });
                            var ifConditionCode = GenerateIfConditionList(thatBlock,BLOCK_CODELINE_TYPE.IF);
                            $(`.vp-block-header-${thatBlock.getUUID()}`).html(ifConditionCode);
                        
                            event.stopPropagation();
                        });
        
        
                        $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_6 + index + uuid);
                        $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_6 + index + uuid, function(event) {
                 
                            // RenderInputRequiredColor(this);
                   
                            var ifConditionListState = thatBlock.getState(STATE_ifConditionList);
                            var ifConditionState = ifConditionListState[index];
                            var inputValue = $(this).val();
        
                            var updatedValue = {
                                ...ifConditionState
                                , arg6: inputValue
                            }
        
                            ifConditionListState = UpdateOneArrayValueAndGet(ifConditionListState, index, updatedValue);
                            thatBlock.setState({
                                ifConditionList: ifConditionListState
                            });
                            var ifConditionCode = GenerateIfConditionList(thatBlock,BLOCK_CODELINE_TYPE.IF);
                            $(`.vp-block-header-${thatBlock.getUUID()}`).html(ifConditionCode);
                        
                            event.stopPropagation();
                        });
                    }
                           
                    /** 삭제 if condition */
                    $(document).off(STR_CLICK, vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_DELETE + index + uuid));
                    $(document).on(STR_CLICK, vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_DELETE + index + uuid), function(event) {
                        var ifConditionListState = thatBlock.getState(STATE_ifConditionList);
        
                        if (ifConditionListState.length == 1) {
                            return;
                        }
                        
                        ifConditionListState = DeleteOneArrayValueAndGet(ifConditionListState, index);
        
                        thatBlock.setState({
                            ifConditionList: ifConditionListState
                        });
                        var ifConditionCode = GenerateIfConditionList(thatBlock, BLOCK_CODELINE_TYPE.IF);
                        $(`.vp-block-header-${thatBlock.getUUID()}`).html(ifConditionCode);
        
                        blockContainerThis.renderBlockOptionTab();
        
                        event.stopPropagation();
                    }); 
                });
                
                /** 생성 if condition - arg1, arg2, arg3, arg4, arg5, arg6*/
                $(document).off(STR_CLICK, vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_PLUS + uuid));
                $(document).on(STR_CLICK, vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_PLUS + uuid), function(event) {
        
                    var ifConditionListState = thatBlock.getState(STATE_ifConditionList);
                    thatBlock.addVariableIndex();
                    // var variableIndex = thatBlock.getVariableIndex();
                    var newCondition = {
                        arg1: ''
                        , arg2: ''
                        , arg3: ''
                        , arg4: ''
                        , arg5: ''
                        , arg6: ''
                        , conditionType: IF_BLOCK_CONDITION_TYPE.ARG
                    }
                    ifConditionListState = CreateOneArrayValueAndGet(ifConditionListState, ifConditionListState.length, newCondition);
                    thatBlock.setState({
                        ifConditionList: ifConditionListState
                    });
                    var ifConditionCode = GenerateIfConditionList(thatBlock, BLOCK_CODELINE_TYPE.IF);
                    $(`.vp-block-header-${thatBlock.getUUID()}`).html(ifConditionCode);
                    
                    blockContainerThis.renderBlockOptionTab();
                    event.stopPropagation();
                });
        
                /** 생성 if condition - User Input ,arg6*/
                $(document).off(STR_CLICK, vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_PLUS_USER_INPUT + uuid));
                $(document).on(STR_CLICK, vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_PLUS_USER_INPUT + uuid), function(event) {
        
                    var ifConditionListState = thatBlock.getState(STATE_ifConditionList);
                    thatBlock.addVariableIndex();
                
                    var newCondition = {
                        codeLine: ''
                        , arg6: ''
                        , conditionType: IF_BLOCK_CONDITION_TYPE.USER_INPUT
                    }
                    ifConditionListState = CreateOneArrayValueAndGet(ifConditionListState, ifConditionListState.length, newCondition);
                    thatBlock.setState({
                        ifConditionList: ifConditionListState
                    });
                    var ifConditionCode = GenerateIfConditionList(thatBlock, BLOCK_CODELINE_TYPE.IF);
                    $(`.vp-block-header-${thatBlock.getUUID()}`).html(ifConditionCode);
                    
                    blockContainerThis.renderBlockOptionTab();
                    event.stopPropagation();
                });
        
                /** arg1, arg2, arg3, arg4, arg5, arg6 select 변경 if condition */
                var bindSelectValueEventFunc_if = function(selectedValue, index, type) {
                    var ifConditionListState = thatBlock.getState(STATE_ifConditionList);
                    var ifConditionState = ifConditionListState[index];
                    var updatedValue;
                    if (type == IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG1) {
                        updatedValue = {
                            ...ifConditionState
                            , arg1: selectedValue 
                        }
                        // RenderSelectRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_1 + index + uuid, selectedValue);
                    } else if (type == IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG2) {
                        if (selectedValue == 'none') {
                            selectedValue = STR_NULL;
                        }
                        updatedValue = {
                            ...ifConditionState
                            , arg2: selectedValue 
                        }
                        // RenderSelectRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid, selectedValue);
                    } else if (type == IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG3) {
                        updatedValue = {
                            ...ifConditionState
                            , arg3: selectedValue 
                        }
                        // RenderSelectRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_3 + index + uuid, selectedValue);
                    } else if (type == IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG4) {
               
                        if (selectedValue == 'none') {
                            selectedValue = STR_NULL;
                        }
                        updatedValue = {
                            ...ifConditionState
                            , arg4: selectedValue 
                        }
                        if (selectedValue == STR_NULL) {
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid).addClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).addClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).attr(STR_DISABLED, true);
                        } else {
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid).removeClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).removeClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).attr(STR_DISABLED, false);
                        }
        
                    } else if (type == IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG5) {
                        updatedValue = {
                            ...ifConditionState
                            , arg5: selectedValue 
                        }
                    } else {
                        updatedValue = {
                            ...ifConditionState
                            , arg6: selectedValue 
                        }
                        // RenderSelectRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_6 + index + uuid, selectedValue);
                    }
                    ifConditionListState = UpdateOneArrayValueAndGet(ifConditionListState, index, updatedValue);
                    thatBlock.setState({
                        ifConditionList: ifConditionListState
                    });
                    var ifConditionCode = GenerateIfConditionList(thatBlock, BLOCK_CODELINE_TYPE.IF);
                    $(`.vp-block-header-${thatBlock.getUUID()}`).html(ifConditionCode);

                    // if (IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG2 == type) {
                    //     // $(document).off(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid);
                    //     $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid);
                    //     blockContainerThis.renderBlockOptionTab();
                    // }
                    // if (IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG4 == type) {
                    //     // $(document).off(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid);
                    //     $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid);
                    //     blockContainerThis.renderBlockOptionTab();
                    // }
    
                }
        
                /** --------------------------------- Else Option 이벤트 함수 바인딩 ---------------------------------- */  
                /** Else block 생성, 삭제 이벤트 함수 바인딩 */
                // blockContainerThis.bindElseBlockEvent(thatBlock, BLOCK_CODELINE_TYPE.ELSE);
        
        
        
        
        
        
        
        
        
                // ifConditionListState.forEach( (condition,index) => {

                // });
        
        
                /** If option 렌더링 */
                var renderThisComponent = function() {
                    // console.log('if render');
                    var optionContainerDom = MakeOptionContainer();
                    /* --------------------------- if ----------------------------- */
                    var loadedVariableNameList = blockContainerThis.getKernelLoadedVariableNameList();
                    // var variableIndex = thatBlock.getVariableIndex();
        
                    var ifConditionListState = thatBlock.getState(STATE_ifConditionList);   
                    ifConditionListState.forEach( (condition, index) => {
                     

                        const { conditionType } = condition; 
             
                        var sbCondition = new sb.StringBuilder();
                        sbCondition.appendFormatLine("<div class='{0}'  ", VP_CLASS_STYLE_FLEX_ROW_BETWEEN);
                        sbCondition.appendFormatLine("     style='{0}'  >",'');
        
                        var sbConditionLeft = new sb.StringBuilder();
                        sbConditionLeft.appendFormatLine("<div class='{0}'  ", VP_CLASS_STYLE_FLEX_ROW_BETWEEN);
                        sbConditionLeft.appendFormatLine("     style='{0}'  >",'width:80%;');
                        // var sbConditionDom = $(sbCondition.toString());
                        if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                            const { arg1, arg2, arg3, arg4, arg5, arg6 } = condition; 
                            var loadedVariableNameList_arg1 = [ `'i${index + 1}'`, ...loadedVariableNameList];
                            var loadedVariableNameList_arg3 = [ `'j${index + 1}'`, ...loadedVariableNameList];
                            var loadedVariableNameList_arg5 = [ `'k${index + 1}'`, ...loadedVariableNameList];
                            var suggestInputArg1 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_IF_ARG_1 + index + uuid
                                                                                    , arg1
                                                                                    , loadedVariableNameList_arg1
                                                                                    , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                                    , STR_VARIABLE
                                                                                    , function(selectedValue) {
                                                                                        bindSelectValueEventFunc_if(selectedValue, 
                                                                                                                    index,
                                                                                                                    IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG1);
                                                                                        });  
                                                                                        
                            var filterd_IF_OPERATOR_ARG2 = COMPARISON_OPERATOR_IF_ARG2.filter(arg => {
                                if (arg == 'none') {
                                    return false;
                                } else {
                                    return true;
                                }
                            });
                            var isSuggestInput = filterd_IF_OPERATOR_ARG2.some(arg => {
                                if (arg == arg2) {
                                    return true;
                                }
                            });                                                                   
                            var sbIfArg2;
            
                            // console.log('arg2',arg2);
                            // if (isSuggestInput == true) {
                            //     sbIfArg2 = MakeOptionSelectBox(VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid
                            //                                 , VP_CLASS_STYLE_WIDTH_15PERCENT
                            //                                 , arg2
                            //                                 , COMPARISON_OPERATOR_IF_ARG2);

                            // } else {
                                sbIfArg2 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid
                                                , arg2
                                                , COMPARISON_OPERATOR_IF_ARG2
                                                , VP_CLASS_STYLE_WIDTH_15PERCENT
                                                , STR_OPERATOR
                                                , function(selectedValue) {
                                                bindSelectValueEventFunc_if(selectedValue, 
                                                                            index,
                                                                            IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG2);
                                                });     
                            // }
                                                              
                            var suggestInputArg3 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_IF_ARG_3 + index + uuid
                                                                                    , arg3
                                                                                    , loadedVariableNameList_arg3
                                                                                    , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                                    , STR_VARIABLE
                                                                                    , function(selectedValue) {
                                                                                        bindSelectValueEventFunc_if(selectedValue, 
                                                                                                                    index,
                                                                                                                    IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG3);
                                                                                        });   
                            // var filterd_IF_OPERATOR_ARG4 = COMPARISON_OPERATOR_IF_ARG4.filter(arg => {
                            //     if (arg == 'none') {
                            //         return false;
                            //     } else {
                            //         return true;
                            //     }
                            // });
                            // var isSuggestInput = filterd_IF_OPERATOR_ARG4.some(arg => {
                            //     if (arg == arg4) {
                            //         return true;
                            //     }
                            // });
                            var sbIfArg4;
                            // if (isSuggestInput == true) {
                                // sbIfArg4 = MakeOptionSelectBox(VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid
                                //                             , VP_CLASS_STYLE_WIDTH_15PERCENT
                                //                             , arg4
                                //                             , COMPARISON_OPERATOR_IF_ARG4);

                            // } else {
                                sbIfArg4 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid
                                    , arg4
                                    , COMPARISON_OPERATOR_IF_ARG4
                                    , VP_CLASS_STYLE_WIDTH_15PERCENT
                                    , STR_OPERATOR
                                    , function(selectedValue) {
                                        bindSelectValueEventFunc_if(selectedValue, 
                                            index,
                                            IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG4);
                                    });    
                            // }

                            var suggestInputArg5 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid
                                                                                    , arg5
                                                                                    , loadedVariableNameList_arg5
                                                                                    , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                                    , STR_VARIABLE
                                                                                    , function(selectedValue) {
                                                                                        bindSelectValueEventFunc_if(selectedValue, 
                                                                                                                    index,
                                                                                                                    IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG5);
                                                                                        });    
        
                            var suggestInputArg6 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_IF_ARG_6 + index + uuid
                                                                                        , arg6
                                                                                        , COMPARISON_OPERATOR_IF_ARG6
                                                                                        , VP_CLASS_STYLE_WIDTH_10PERCENT
                                                                                        , STR_OPERATOR
                                                                                        , function(selectedValue) {
                                                                                            bindSelectValueEventFunc_if(selectedValue, 
                                                                                                index,
                                                                                                IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG6);
                                                                                    });      
                            sbConditionLeft.appendLine(suggestInputArg1);
                            sbConditionLeft.appendLine(sbIfArg2);
                            sbConditionLeft.appendLine(suggestInputArg3);
                            sbConditionLeft.appendLine(sbIfArg4);
                            sbConditionLeft.appendLine(suggestInputArg5);
                            sbConditionLeft.appendLine("</div>");
        
                            sbCondition.appendLine(sbConditionLeft.toString());
                            sbCondition.appendLine(suggestInputArg6);
        
                            var deleteConditionButton = MakeOptionDeleteButton(VP_ID_APIBLOCK_OPTION_IF_DELETE + index + uuid);
                            sbCondition.appendLine(deleteConditionButton);
        
                            sbCondition.appendLine("</div>");
                        } else {
                            const { arg6, codeLine } = condition;
              
                            var sbOptionInput = MakeOptionInput(VP_ID_APIBLOCK_OPTION_IF_USER_INPUT + index + uuid
                                                                , VP_CLASS_STYLE_WIDTH_100PERCENT
                                                                , codeLine
                                                                , 'Type user code');
                            sbConditionLeft.appendLine(sbOptionInput);
                            sbConditionLeft.appendLine("</div>");
                            var suggestInputArg6 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_IF_ARG_6 + index + uuid
                                                                    , arg6
                                                                    , COMPARISON_OPERATOR_IF_ARG6
                                                                    , VP_CLASS_STYLE_WIDTH_10PERCENT
                                                                    , STR_OPERATOR
                                                                    , function(selectedValue) {
                                                                        bindSelectValueEventFunc_if(selectedValue, 
                                                                            index,
                                                                            IF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG6);
                                                                });    
                            sbCondition.appendLine(sbConditionLeft.toString());
                            sbCondition.appendLine(suggestInputArg6);
        
                            var deleteConditionButton = MakeOptionDeleteButton(VP_ID_APIBLOCK_OPTION_IF_DELETE + index + uuid);
                            sbCondition.appendLine(deleteConditionButton);
        
                            sbCondition.appendLine("</div>");
                        }
        
                        var tblLayout = new vpTableLayoutVerticalSimple.vpTableLayoutVerticalSimple();
                        tblLayout.setTHWidth("5%");
                        tblLayout.addClass(VP_CLASS_STYLE_WIDTH_100PERCENT);
                        tblLayout.addRow(index + 1, sbCondition.toString());
        
         
                        optionContainerDom.append(tblLayout.toTagString());              
                    });
                 
        
        
                    var sbButtonContainer = new sb.StringBuilder();
                    sbButtonContainer.appendFormatLine("<div class='{0}' style='{1}' >", VP_CLASS_STYLE_FLEX_ROW, 'margin-top:15px;');
                    sbButtonContainer.appendLine("</div>");
                    var sbButtonContainerDom = $(sbButtonContainer.toString());
        
                    var plusButton = MakeOptionPlusButton(VP_ID_APIBLOCK_OPTION_IF_PLUS + uuid, '+ Condition');
                    var plusButton_userInput = MakeOptionPlusButton(VP_ID_APIBLOCK_OPTION_IF_PLUS_USER_INPUT + uuid, '+ User Input', VP_CLASS_STYLE_MARGIN_LEFT_15PX);
                    sbButtonContainerDom.append(plusButton);
                    sbButtonContainerDom.append(plusButton_userInput);
        
                    optionContainerDom.append(sbButtonContainerDom);
                    /** bottom block option 탭에 렌더링된 dom객체 생성 */
                    $(optionPageSelector).append(optionContainerDom);
        
                    /** 새로 IF OPTION을 열었을때,
                     * 
                     *  1. arg value 값 넣기, 
                     *  2. none disabled 설정, 
                     *  3. none opacity 0 설정
                     *  4. 입력되지 않은 값 border alert 처리
                     *  */
                    var ifConditionListState = thatBlock.getState(STATE_ifConditionList);   
                    ifConditionListState.forEach( (condition,index) => {
                        const { arg1, arg2, arg3, arg4, arg5, arg6 } = condition;
        
                        $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_1 + index + uuid).val(arg1);
                  
                        $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_3 + index + uuid).val(arg3);
               
                        $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).val(arg5);
                        // if (arg2 == 'none') {
                        //     $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid).val(STR_NULL);
                        // } else {
                        //     $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid).val(arg2);
                        // }
                        $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid).val(arg2);
                        if (arg4 == '') {
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid).val(STR_NULL);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid).addClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).attr(STR_DISABLED, true);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).addClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                        } else {
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid).val(arg4);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_4 + index + uuid).removeClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).attr(STR_DISABLED, false);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_5 + index + uuid).removeClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                        }     
      
                        if ( ifConditionListState.length -1 == index ) {
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_6 + index + uuid).addClass(VP_CLASS_STYLE_OPACITY_0);
                        } else {
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_6 + index + uuid).val(arg6);
                            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_6 + index + uuid).addClass(VP_CLASS_STYLE_OPACITY_1);
                        }
              
                        // RenderInputRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_1 + index + uuid);
                        // RenderInputRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_2 + index + uuid);
                        // RenderInputRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_3 + index + uuid);
                        // RenderInputRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_ARG_6 + index + uuid);
        
                        // RenderInputRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_IF_USER_INPUT + index + uuid);
                    });
                }
        
                renderThisComponent();
            }
        
            return InitIfBlockOption;
        });
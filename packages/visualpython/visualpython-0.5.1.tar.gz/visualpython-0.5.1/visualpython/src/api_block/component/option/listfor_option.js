define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpTableLayoutVerticalSimple'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb, vpTableLayoutVerticalSimple, 
              api, config, constData, 
              blockRenderer, baseComponent ) {

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

    const { GenerateListforConditionList
            ,GenerateForParam  } = blockRenderer;

    const { BLOCK_CODELINE_BTN_TYPE
                , BLOCK_CODELINE_TYPE
                , FOR_BLOCK_TYPE
                , FOR_BLOCK_ARG3_TYPE
                , FOR_BLOCK_SELECT_VALUE_ARG_TYPE
    
                , VP_ID_PREFIX
                , VP_ID_APIBLOCK_OPTION_FOR_TYPE_SELECT
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_1
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_2
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_3
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_4
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_5
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_6
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_7
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_10
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_11
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_12
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_13
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_14
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15

                , VP_ID_APIBLOCK_OPTION_LIST_FOR_PLUS
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_RETURN_VAR
                , VP_ID_APIBLOCK_OPTION_LIST_FOR_PREV_EXPRESSION

                , VP_CLASS_PREFIX
                , VP_CLASS_STYLE_FLEX_ROW
                , VP_CLASS_STYLE_FLEX_ROW_CENTER
                , VP_CLASS_STYLE_FLEX_ROW_WRAP
                , VP_CLASS_STYLE_FLEX_ROW_CENTER_WRAP
                , VP_CLASS_STYLE_FLEX_ROW_BETWEEN
                , VP_CLASS_STYLE_FLEX_ROW_AROUND
                , VP_CLASS_STYLE_FLEX_ROW_EVENLY
                , VP_CLASS_STYLE_FLEX_ROW_BETWEEN_WRAP
                , VP_CLASS_STYLE_FLEX_ROW_END
                , VP_CLASS_STYLE_FLEX_COLUMN
                , VP_CLASS_STYLE_FLEX_COLUMN_CENTER
                , VP_CLASS_STYLE_FLEX_COLUMN_CENTER_WRAP
                , VP_CLASS_STYLE_MARGIN_TOP_5PX
    
    
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
    
                , VP_CLASS_APIBLOCK_OPTION_INPUT
                , VP_CLASS_APIBLOCK_BLOCK_HEADER 

                , VP_CLASS_STYLE_OPACITY_0
                , VP_CLASS_STYLE_OPACITY_1
                
                , VP_CLASS_STYLE_BGCOLOR_C4C4C4

                , STR_NULL
                , STR_COLON_SELECTED
                , STR_FOR
                , STR_CHANGE
                , STR_CHANGE_KEYUP_PASTE
                , STR_SELECTED
                , STR_STRONG
                , STR_FLEX
                , STR_NONE
                , STR_DISPLAY
                , STR_VARIABLE
                , STR_OPERATOR
                , STR_VALUE 
                , STR_CLICK
                , STATE_forParam
                , STATE_forBlockOptionType
                , STATE_listforConditionList
                , STATE_listforReturnVar
                , STATE_listforPrevExpression
            
                , COMPARISON_OPERATOR_IF_ARG2
                , COMPARISON_OPERATOR_IF_ARG4
                , COMPARISON_OPERATOR_IF_ARG6 } = constData;

    const { MakeOptionContainer
                , MakeOptionDeleteButton
                , MakeOptionPlusButton
                , MakeVpSuggestInputText_apiblock
                , MakeOptionInput
                , MakeOptionSelectBox  } = baseComponent;    

    var InitListForBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();
        var blockContainerThis = thatBlock.getBlockContainerThis();

        /** --------------------------------- List for Option 이벤트 함수 바인딩 ---------------------------------- */    
        var listforConditionListState = thatBlock.getState(STATE_listforConditionList);  
        listforConditionListState.forEach((listforParam, index) => {


            /** List for condition 삭제  이벤트 함수
             * @event_function
             */
            $(document).off(STR_CLICK, vpCommon.wrapSelector(`#vpApiblockDeleteButton${index}${uuid}`));
            $(document).on(STR_CLICK, vpCommon.wrapSelector(`#vpApiblockDeleteButton${index}${uuid}`), function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
            
                if (listforConditionListState.length == 1) {
                     return;
                }
                            
                listforConditionListState = DeleteOneArrayValueAndGet(listforConditionListState, index);
            
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);
            
                blockContainerThis.renderBlockOptionTab();
            
                event.stopPropagation();
            }); 

       /**
             * @event_function
             * List for arg1 변경 
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_1 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_1 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];

                var updatedValue = {
                    ...listforConditionState
                    , arg1 : $(this).val()
                }
     
                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });
         

                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);

                event.stopPropagation();
            });
            /**
             * @event_function
             *  for arg2 변경 
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_2 +index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_2 +index + uuid, function(event) {
                // RenderInputRequiredColor(this);
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];

                var updatedValue = {
                    ...listforConditionState
                    , arg2 : $(this).val()
                }
      
                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    [STATE_listforConditionList]: listforConditionListState
                });
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);

                event.stopPropagation();
            });
            /**
             * @event_function
             *  for arg3 변경 
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_3 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_3 + index + uuid, function(event) {
                // RenderInputRequiredColor(this);
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];

                var updatedValue = {
                    ...listforConditionState
                    , arg3 : $(this).val()
                }
      
                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    [STATE_listforConditionList]: listforConditionListState
                });
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);

                event.stopPropagation();
            });

            $(document).off(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_3 + index  + uuid);
            $(document).on(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_3 + index  + uuid, function(event) {
                 // RenderInputRequiredColor(this);
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];
 
                var selectedValue = $(STR_COLON_SELECTED, this).val();
                if (selectedValue == FOR_BLOCK_ARG3_TYPE.ZIP
                    || selectedValue == FOR_BLOCK_ARG3_TYPE.RANGE
                    || selectedValue == FOR_BLOCK_ARG3_TYPE.ENUMERATE
                    || selectedValue == FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                        var updatedValue = {
                            ...listforConditionState
                            , arg3 : $(STR_COLON_SELECTED, this).val()  
                        }
              
                        listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                        thatBlock.setState({
                            [STATE_listforConditionList]: listforConditionListState
                        });
                        var listforConditionCode = GenerateListforConditionList(thatBlock);
                        $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);
                        blockContainerThis.renderBlockOptionTab();
                }

                event.stopPropagation();
            });
            /**
             * @event_function
             * List for arg4 변경 
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_4 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_4 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];

                var updatedValue = {
                    ...listforConditionState
                    , arg4 : $(this).val()
                }
                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });

                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);

                event.stopPropagation();
            });


            /**
             * @event_function
             * List for arg5 변경 
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_5 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_5 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];

                var updatedValue = {
                    ...listforConditionState
                    , arg5 : $(this).val()
                }
                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });

                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);

                event.stopPropagation();
            });


            /**
             * @event_function
             * List for arg6 변경
             */
            // $(document).off(STR_CHANGE_KEYUP_PASTE, `.vp_apiblockBlockoptionListforArg6${index}${uuid}`);
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_6 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_6 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];

                var updatedValue = {
                    ...listforConditionState
                    , arg6 : $(this).val()
                }
                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });

                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);

                event.stopPropagation();
            });


            /**
             * @event_function
             * List for arg7 변경 
             */
            // $(document).off(STR_CHANGE_KEYUP_PASTE, `.vp_apiblockBlockoptionListforArg7${index}${uuid}`);
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_7 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_7 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];

                var updatedValue = {
                    ...listforConditionState
                    , arg7 : $(this).val()
                }
                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });

                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);

                event.stopPropagation();
            });


            /**
             * @event_function
             * List for arg10 autocomplete 입력 변경 이벤트 함수
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_10 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_10 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];

                var updatedValue = {
                    ...listforConditionState
                    , arg10 :  $(this).val()
                }

                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);
                blockContainerThis.renderBlockOptionTab();
                event.stopPropagation();
            });

            /** List for arg11 변경 */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_11 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_11 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];
            
                var updatedValue = {
                    ...listforConditionState
                    , arg11 : $(this).val()
                }
                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });
            
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);
            
                event.stopPropagation();
            });


            /**
             * @event_function
             * List for arg12 선택 변경 이벤트 함수
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_12 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_12 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];

                var updatedValue = {
                    ...listforConditionState
                    , arg12 :  $(this).val()
                }

                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);

                event.stopPropagation();
            });


            /** 
             * @event_function
             * List for arg13 변경 
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_13 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_13 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];
            
                var updatedValue = {
                    ...listforConditionState
                    , arg13 : $(this).val()
                }
                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });
            
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);
            
                event.stopPropagation();
            });



             /**
             * @event_function
             * List for arg14 선택 변경 이벤트 함수
             */
            // $(document).off(STR_CHANGE, `.vp_apiblockBlockoptionListforArg14${index}${uuid}`);
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_14 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_14 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];

                var updatedValue = {
                    ...listforConditionState
                    , arg14 :  $(this).val()
                }

                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);

                event.stopPropagation();
            });


            /**
             * @event_function
             * List for arg15 변경 
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid, function(event) {
                var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
                var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];
            
                var updatedValue = {
                    ...listforConditionState
                    , arg15 : $(this).val()
                }
                listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
                thatBlock.setState({
                    listforConditionList: listforConditionListState
                });
            
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);
            
                event.stopPropagation();
            });
        });


        /** 
         * @event_function
         * List For condition 생성 이벤트 함수 바인딩 
         */
        $(document).off(STR_CLICK, vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_PLUS + uuid));
        $(document).on(STR_CLICK, vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_PLUS + uuid), function() {
            var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
            var listforConditionLength = listforConditionListState.length;

            thatBlock.addVariableIndex();
            
            var newCondition = {
                arg1:  ''
                , arg2: ''
                , arg3: FOR_BLOCK_ARG3_TYPE.INPUT_STR
                , arg4: ''
                , arg5: ''
                , arg6: ''
                , arg7: ''

                , arg10: 'none'
                , arg11: ''
                , arg12: ''
                , arg13: ''
                , arg14: 'none'
                , arg15: ''

                , arg3InputStr: ''
                , arg3Default: ''

                , arg10InputStr: ''
            }
            listforConditionListState = CreateOneArrayValueAndGet(listforConditionListState, listforConditionLength, newCondition);
            thatBlock.setState({
                listforConditionList: listforConditionListState
            });

            var listforfConditionCode = GenerateListforConditionList(thatBlock);
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforfConditionCode);

            blockContainerThis.renderBlockOptionTab();
        });

        /**
         * @event_function
         * List for 리턴 변수 이름 변경 이벤트 함수
         */
        $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_RETURN_VAR + uuid);
        $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_RETURN_VAR + uuid, function(event) {
            thatBlock.setState({
                listforReturnVar: $(this).val()
            });

            var listforfConditionCode = GenerateListforConditionList(thatBlock);
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforfConditionCode);

            event.stopPropagation();
        });

        /**
         * @event_function
         * List for 선행 조건값 변경 이벤트 함수
         */
        $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_PREV_EXPRESSION + uuid);
        $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_PREV_EXPRESSION + uuid, function(event) {
            thatBlock.setState({
                listforPrevExpression: $(this).val()
            });

            var listforfConditionCode = GenerateListforConditionList(thatBlock);
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforfConditionCode);

            event.stopPropagation();
        });

        /**
         * @event_function
         * For or List for 선택 이벤트 함수
         */
        $(document).off(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_FOR_TYPE_SELECT +uuid);
        $(document).on(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_FOR_TYPE_SELECT +uuid, function(event) {
            var selectedVal = $(STR_COLON_SELECTED, this).val();

            thatBlock.setState({
                forBlockOptionType: $(STR_COLON_SELECTED, this).val()
            });

            if ( selectedVal == FOR_BLOCK_TYPE.FOR ) {
                var forParamStr = GenerateForParam(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(forParamStr);
                thatBlock.getBlockHeaderDom().find(STR_STRONG).css(STR_DISPLAY, STR_FLEX);
            } else {
                var listForStr = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listForStr);
                thatBlock.getBlockHeaderDom().find(STR_STRONG).css(STR_DISPLAY, STR_NONE);
            }

            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });


        var bindSelectValueEventFunc_for = function(selectedValue, index, argType) {
            var listforConditionListState = thatBlock.getState(STATE_listforConditionList);
            var listforConditionState = thatBlock.getState(STATE_listforConditionList)[index];
            var updatedValue;
        
            if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG1 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg1 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG2 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg2 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG3 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg3 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG4 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg4 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG5 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg5 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG6 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg6 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG7 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg7 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG10 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg10 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG11 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg11 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG12 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg12 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG13 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg13 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG14 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg14 : selectedValue
                }
                if (selectedValue == 'none' || selectedValue == STR_NULL) {
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_14 + index + uuid).addClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid).attr("disabled", true);
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid).addClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                } else {
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_14 + index + uuid).removeClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid).attr("disabled", false);
                
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid).removeClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                }   
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG15 == argType) {
                updatedValue = {
                    ...listforConditionState
                    , arg15 : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG3_DEFAULT == argType) {
                updatedValue = {
                    ...forParam
                    , arg3Default : selectedValue
                }
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG3_INPUT_STR == argType) {
                updatedValue = {
                    ...forParam
                    , arg3InputStr : selectedValue
                }
            }
            else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.RETURN_VAR == argType) {
                thatBlock.setState({
                    listforReturnVar: selectedValue
                });
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);
                return;
            } else if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.PREV_EXPRESSION == argType) {
                thatBlock.setState({
                    listforPrevExpression: selectedValue
                });
                var listforConditionCode = GenerateListforConditionList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);
                return;
            }
        
            listforConditionListState = UpdateOneArrayValueAndGet(listforConditionListState, index, updatedValue);
            thatBlock.setState({
                [STATE_listforConditionList]: listforConditionListState
            });
        
            var listforConditionCode = GenerateListforConditionList(thatBlock);
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(listforConditionCode);

            if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG3 == argType) {
                $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_3 + index+ uuid);
                blockContainerThis.renderBlockOptionTab();
            }
            if (FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG10 == argType) {
                $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_10 + index+ uuid);
                blockContainerThis.renderBlockOptionTab();
            }
        }

        /** List For option 렌더링 */
        var renderThisComponent = function() {

            var forBlockOption = MakeOptionContainer();

            var forBlockOptionType = thatBlock.getState(STATE_forBlockOptionType);
            var listforReturnVarState = thatBlock.getState(STATE_listforReturnVar);
            var listforPrevExpression = thatBlock.getState(STATE_listforPrevExpression);

            /* ------------- For html dom 생성 ------------------ */
            var forName = 'List For';

            var selectedFor = forBlockOptionType == FOR_BLOCK_TYPE.FOR 
                                    ? STR_SELECTED 
                                    : STR_NULL;
            var selectedListfor = forBlockOptionType == FOR_BLOCK_TYPE.LIST_FOR
                                    ? STR_SELECTED 
                                    : STR_NULL;
    
            var sbforNameDom = new sb.StringBuilder();
            sbforNameDom.appendFormatLine("<div class='{0}'>", 'vp-apiblock-style-margin-top-5px');
            sbforNameDom.appendFormatLine("<div class='{0}'>", 'vp-apiblock-tab-navigation-node-block-title');

            sbforNameDom.appendFormatLine("<span class='{0}'>", 'vp-apiblock-optionpage-name');
            sbforNameDom.appendFormatLine("{0}", forName);
            sbforNameDom.appendLine("</span>");

            sbforNameDom.appendFormatLine("<select id='{0}'>", VP_ID_APIBLOCK_OPTION_FOR_TYPE_SELECT + uuid);
            sbforNameDom.appendFormatLine("<option value='{0}' '{1}'>", 'listfor', selectedListfor);
            sbforNameDom.appendFormatLine("{0}", 'listfor');
            sbforNameDom.appendFormatLine("<option value='{0}' '{1}'>", STR_FOR, selectedFor);
            sbforNameDom.appendFormatLine("{0}", STR_FOR);
            sbforNameDom.appendLine("</option>");
   
            sbforNameDom.appendLine("</option>");
            sbforNameDom.appendLine("</select>");
            sbforNameDom.appendLine("</div>");
            sbforNameDom.appendLine("</div>");
            forBlockOption.append(sbforNameDom.toString());

            /**----------------------------------------------------- */
            var loadedVariableNameList = blockContainerThis.getKernelLoadedVariableNameList();
            var loadedVariableNameList_returnVar = [ `list_0`, ...loadedVariableNameList];
            var loadedVariableNameList_listforPrevExpression = [ `a + b`,`a - b`, `a * b`, `a / b`, ...loadedVariableNameList];


            var sbListforReturnVar = new sb.StringBuilder();
            sbListforReturnVar.appendFormatLine("<div class='{0}'  ", VP_CLASS_STYLE_FLEX_ROW);
            sbListforReturnVar.appendFormatLine("      style='{0}'  >",'');


            /** List For Return var */
             var sbforParamReturnVar = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_RETURN_VAR + uuid
                                                                        ,listforReturnVarState
                                                                        ,loadedVariableNameList_returnVar
                                                                        , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                        , 'Return Var'
                                                                        , function(selectedValue) {
                                                                            bindSelectValueEventFunc_for(selectedValue,
                                                                                0 
                                                                                , FOR_BLOCK_SELECT_VALUE_ARG_TYPE.RETURN_VAR);
                                                                        });


            sbListforReturnVar.appendLine(sbforParamReturnVar);
  
            var sbAssign = new sb.StringBuilder();
            sbAssign.appendFormatLine("<div class='{0}'  ", VP_CLASS_STYLE_FLEX_COLUMN_CENTER);
            sbAssign.appendFormatLine("     style='{0} {1} {2}'  >",'margin-left: 5px;', 'margin-right: 5px;','text-align: center;');
            sbAssign.appendLine("=");
            sbAssign.appendLine("</div>");

            sbListforReturnVar.appendLine(sbAssign.toString());

            var listforFirstBracket = `<div class='vp-apiblock-style-flex-row'>
                                                <span class='vp-apiblock-style-flex-column-center'
                                                    style='margin-left: 5px; margin-right: 5px;
                                                    color:#E85401;'> [
                                                </span>
                                        </div>`;
            sbListforReturnVar.appendLine(listforFirstBracket);

            /** List For PrevExpression */
            var sbforParamPrevExpression = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_PREV_EXPRESSION + uuid
                                                                        ,listforPrevExpression
                                                                        ,loadedVariableNameList_listforPrevExpression
                                                                        , VP_CLASS_STYLE_WIDTH_50PERCENT
                                                                        , 'a + b'
                                                                        , function(selectedValue) {
                                                                            bindSelectValueEventFunc_for(selectedValue, 
                                                                                0
                                                                                , FOR_BLOCK_SELECT_VALUE_ARG_TYPE.PREV_EXPRESSION);
                                                                        });


            sbListforReturnVar.appendLine(sbforParamPrevExpression);

            sbListforReturnVar.appendLine("</div>");

            forBlockOption.append(sbListforReturnVar.toString());

            var listforParamDomBody = $('<div></div>');
            var listforConditionListState = thatBlock.getState(STATE_listforConditionList);  
            listforConditionListState.forEach((listforParam, index) => {
                var listforParamDomContainer = $(`<div class='vp-apiblock-blockoption-block 
                                                              vp-apiblock-style-flex-column-center'>
                                                  </div>`);

                // console.log('listforParam',listforParam);
                const { arg1, arg2, arg3, arg4, arg5, arg6, arg7,
                        arg10, arg11, arg12, arg13, arg14, arg15 } = listforParam;
                var loadedVariableNameList = blockContainerThis.getKernelLoadedVariableNameList();
                var loadedVariableNameList_arg1 = [ ...loadedVariableNameList,  `i${index + 1}`];
                var loadedVariableNameList_arg4 = [ ...loadedVariableNameList,  `j${index + 1}`];
                var loadedVariableNameList_arg3 = [ ...Object.values( FOR_BLOCK_ARG3_TYPE )];
                /** 0,1,2,3 */
                var loadedVariableNameList_arg5 = [ ...loadedVariableNameList, '0','1','2','3'];
                /** 9 */
                var loadedVariableNameList_arg6 = [ ...loadedVariableNameList, '9'];
                /** 내부변수 */
                var loadedVariableNameList_arg2 = [ ...loadedVariableNameList, '0','1','2','3'];
                var loadedVariableNameList_arg7 = [ ...loadedVariableNameList, '0','1','2','3'];
                var loadedVariableNameList_arg10 = [ 'none','if'];
                var loadedVariableNameList_arg11 = [ ...loadedVariableNameList, `'i${index + 1}'`]; 
                var loadedVariableNameList_arg13 = [ ...loadedVariableNameList, `'J${index + 1}'`];
                var loadedVariableNameList_arg15 = [ ...loadedVariableNameList, `'K${index + 1}'`];

                /**----------------------------Condition1 ------------------------- */

                var sbListForCondition1 = new sb.StringBuilder();
                sbListForCondition1.appendFormatLine("<div class='{0}'  ", VP_CLASS_STYLE_FLEX_ROW_BETWEEN);
                sbListForCondition1.appendFormatLine("     style='{0}'  >",'');

                var sbFor = new sb.StringBuilder();
                sbFor.appendFormatLine("<div class='{0}'  ", VP_CLASS_STYLE_FLEX_COLUMN_CENTER);
                sbFor.appendFormatLine("     style='{0} {1}'  >",'margin-left: 5px;', '');
                sbFor.appendLine("for");
                sbFor.appendLine("</div>");
                sbListForCondition1.appendLine(sbFor.toString());

                var sbforVariableContainer = new sb.StringBuilder();
                sbforVariableContainer.appendFormatLine("<div class='{0} {1}'>", VP_CLASS_STYLE_FLEX_ROW_BETWEEN 
                                                                            , VP_CLASS_STYLE_WIDTH_60PERCENT);
                /** For arg1 */
                var sbforParamArg1Input = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_1 + index + uuid
                                                                            ,arg1
                                                                            ,loadedVariableNameList_arg1
                                                                            , VP_CLASS_STYLE_WIDTH_100PERCENT
                                                                            , STR_VARIABLE
                                                                            , function(selectedValue) {
                                                                                bindSelectValueEventFunc_for(selectedValue,
                                                                                    index 
                                                                                    , FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG1);
                                                                            });


                sbforVariableContainer.appendLine(sbforParamArg1Input);
                var sbforParamArg1Input4 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_4 + index  + uuid
                                                                            ,arg4
                                                                            ,loadedVariableNameList_arg4
                                                                            , VP_CLASS_STYLE_WIDTH_100PERCENT
                                                                            , STR_VARIABLE
                                                                            , function(selectedValue) {
                                                                                bindSelectValueEventFunc_for(selectedValue, 
                                                                                    index
                                                                                    , FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG4);
                                                                            });


                sbforVariableContainer.appendLine(sbforParamArg1Input4);
                sbforVariableContainer.appendLine("</div>");
                sbListForCondition1.appendLine(sbforVariableContainer.toString());

                var deleteConditionButton = MakeOptionDeleteButton('vpApiblockDeleteButton' + index + uuid);
                sbListForCondition1.appendLine(deleteConditionButton);

                sbListForCondition1.appendLine("</div>");

                var tblLayout = new vpTableLayoutVerticalSimple.vpTableLayoutVerticalSimple();
                tblLayout.setTHWidth("5%");
                tblLayout.addClass(VP_CLASS_STYLE_WIDTH_100PERCENT);
                tblLayout.addRow(index + 1, sbListForCondition1.toString());

                var $sbListForCondition1 = $(tblLayout.toTagString());

                /**----------------------------List For Condition2 ------------------------- */

                var sbListForCondition2 = new sb.StringBuilder();
                sbListForCondition2.appendFormatLine("<div class='{0}'  ", VP_CLASS_STYLE_FLEX_ROW_BETWEEN);
                sbListForCondition2.appendFormatLine("     style='{0}'  >",'');
                // sbListForCondition2.appendLine("</span>");
      
                /** For in */
                var sbforParamInDom = new sb.StringBuilder();
                sbforParamInDom.appendFormatLine("<div class='{0}'", VP_CLASS_STYLE_FLEX_COLUMN_CENTER);
                sbforParamInDom.appendFormatLine("style='{0} {1}'>", 'width: 5%;', 'text-align:center;');
                sbforParamInDom.appendFormatLine("{0}", 'in');
                sbforParamInDom.appendLine("</div>");

                sbListForCondition2.append(sbforParamInDom.toString());

                var sbListForCondition2ArgContainer = new sb.StringBuilder();
                sbListForCondition2ArgContainer.appendFormatLine("<div class='{0} {1}'>", VP_CLASS_STYLE_FLEX_ROW_BETWEEN 
                                                                            , VP_CLASS_STYLE_WIDTH_80PERCENT);

                var sbforParamArg3 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_3 + index + uuid
                                                                    , arg3
                                                                    , loadedVariableNameList_arg3
                                                                    , VP_CLASS_STYLE_WIDTH_40PERCENT
                                                                    , 'Method'
                                                                    , function(selectedValue) {
                                                                        bindSelectValueEventFunc_for(selectedValue, 
                                                                            index
                                                                            ,FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG3);
                                                                    });    

                sbListForCondition2ArgContainer.appendLine(sbforParamArg3);
                // var sbforParamArg3; 
                if (arg3 == FOR_BLOCK_ARG3_TYPE.ZIP 
                    || arg3 == FOR_BLOCK_ARG3_TYPE.RANGE 
                    || arg3 == FOR_BLOCK_ARG3_TYPE.ENUMERATE) {

                } else{
                    var sbforParamArg2 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_2  + index + uuid
                                                                            ,arg2
                                                                            ,loadedVariableNameList_arg2
                                                                            , VP_CLASS_STYLE_WIDTH_40PERCENT
                                                                            , STR_VALUE
                                                                            , function(selectedValue) {
                                                                                bindSelectValueEventFunc_for(selectedValue
                                                                                    , index
                                                                                    , FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG2);
                                                                            });
                    sbListForCondition2ArgContainer.appendLine(sbforParamArg2);   
                }

                if (arg3 == FOR_BLOCK_ARG3_TYPE.RANGE) {
                    var sbforParamArg5 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_5 + index + uuid
                                                                            ,arg5
                                                                            ,loadedVariableNameList_arg5
                                                                            , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                            , 'Value'
                                                                            , function(selectedValue) {
                                                                                bindSelectValueEventFunc_for(selectedValue
                                                                                    , index
                                                                                    , FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG5);
                                                                            });
                
                    sbListForCondition2ArgContainer.appendLine(sbforParamArg5);
                }            
                // arg3 == STR_NULL
                // || 
                if (arg3 == FOR_BLOCK_ARG3_TYPE.ZIP 
                    || arg3 == FOR_BLOCK_ARG3_TYPE.RANGE 
                    || arg3 == FOR_BLOCK_ARG3_TYPE.ENUMERATE) {
                    var sbforParamArg2 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_2 + index + uuid
                                                                            ,arg2
                                                                            ,loadedVariableNameList_arg2
                                                                            , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                            , 'Value'
                                                                            , function(selectedValue) {
                                                                                bindSelectValueEventFunc_for(selectedValue
                                                                                    , index
                                                                                    , FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG2);
                                                                            });
         
                    sbListForCondition2ArgContainer.appendLine(sbforParamArg2);
                }   
                if (arg3 == FOR_BLOCK_ARG3_TYPE.ZIP) {
                    var sbforParamArg7 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_7 + index + uuid
                                                                        ,arg7
                                                                        ,loadedVariableNameList_arg7
                                                                        , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                        , 'Value'
                                                                        , function(selectedValue) {
                                                                            bindSelectValueEventFunc_for(selectedValue, 
                                                                                index
                                                                                ,FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG7);
                                                                        });
    
                    sbListForCondition2ArgContainer.appendLine(sbforParamArg7);
                }  
                if (arg3 == FOR_BLOCK_ARG3_TYPE.RANGE) {
                    var sbforParamArg6 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_6 + index + uuid
                                                                        , arg6
                                                                        , loadedVariableNameList_arg6
                                                                        , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                        , 'Value'
                                                                        , function(selectedValue) {
                                                                            bindSelectValueEventFunc_for(selectedValue, 
                                                                                index
                                                                                ,FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG6);
                                                                        });
           
                    sbListForCondition2ArgContainer.appendLine(sbforParamArg6);
                }    
                sbListForCondition2ArgContainer.appendLine("</div>");
                sbListForCondition2.appendLine(sbListForCondition2ArgContainer.toString());

                sbListForCondition2.appendLine("</div>");

                var tblLayout2 = new vpTableLayoutVerticalSimple.vpTableLayoutVerticalSimple();
                tblLayout2.setTHWidth("5%");
                tblLayout2.addClass(VP_CLASS_STYLE_WIDTH_100PERCENT);
                tblLayout2.addRow('', sbListForCondition2.toString());
                var $sbListForCondition2 = $(tblLayout2.toTagString());

                /**----------------------------List For Condition3 ------------------------- */
                var sbListForCondition3 = new sb.StringBuilder();
                sbListForCondition3.appendFormatLine("<div class='{0}'  ", VP_CLASS_STYLE_FLEX_ROW_BETWEEN);
                sbListForCondition3.appendFormatLine("     style='{0}'  >",'');
                var suggestInputArg10 = MakeOptionSelectBox(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_10  + index + uuid
                                        , VP_CLASS_STYLE_WIDTH_15PERCENT
                                        , arg10
                                        , loadedVariableNameList_arg10);
   
                sbListForCondition3.appendLine(suggestInputArg10);
        
                if (arg10 == 'if') {
                    var suggestInputArg11 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_11 + index + uuid
                                                                            , arg11
                                                                            , loadedVariableNameList_arg11
                                                                            , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                            , STR_VARIABLE
                                                                            , function(selectedValue) {
                                                                                bindSelectValueEventFunc_for(selectedValue, 
                                                                                                            index,
                                                                                                            FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG11);
                                                                                });   
                    var suggestInputArg12 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_12 + index + uuid
                                                                            , arg12
                                                                            , COMPARISON_OPERATOR_IF_ARG2
                                                                            , VP_CLASS_STYLE_WIDTH_15PERCENT
                                                                            , STR_OPERATOR
                                                                            , function(selectedValue) {
                                                                                bindSelectValueEventFunc_for(selectedValue, 
                                                                                                        index,
                                                                                                        FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG12);
                                                                            });                                                               
                    var suggestInputArg13 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_13 + index + uuid
                                                                            , arg13
                                                                            , loadedVariableNameList_arg13
                                                                            , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                            , STR_VARIABLE
                                                                            , function(selectedValue) {
                                                                                bindSelectValueEventFunc_for(selectedValue, 
                                                                                                            index,
                                                                                                            FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG13);
                    });   
                    var suggestInputArg14 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_14 + index + uuid
                                                                            , arg14
                                                                            , COMPARISON_OPERATOR_IF_ARG4
                                                                            , VP_CLASS_STYLE_WIDTH_15PERCENT
                                                                            , STR_OPERATOR
                                                                            , function(selectedValue) {
                                                                                bindSelectValueEventFunc_for(selectedValue, 
                                                                                    index,
                                                                                    FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG14);
                    });    
                    var suggestInputArg15 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid
                                                                            , arg15
                                                                            , loadedVariableNameList_arg15
                                                                            , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                            , STR_VARIABLE
                                                                            , function(selectedValue) {
                                                                                bindSelectValueEventFunc_for(selectedValue, 
                                                                                                            index,
                                                                                                            FOR_BLOCK_SELECT_VALUE_ARG_TYPE.ARG15);
                    });
                    sbListForCondition3.appendLine(suggestInputArg11);
                    sbListForCondition3.appendLine(suggestInputArg12);
                    sbListForCondition3.appendLine(suggestInputArg13);
                    sbListForCondition3.appendLine(suggestInputArg14);
                    sbListForCondition3.appendLine(suggestInputArg15);
                }  

                sbListForCondition3.appendLine("</div>");

                var tblLayout3 = new vpTableLayoutVerticalSimple.vpTableLayoutVerticalSimple();
                tblLayout3.setTHWidth("5%");
                tblLayout3.addClass(VP_CLASS_STYLE_WIDTH_100PERCENT);
                tblLayout3.addRow('', sbListForCondition3.toString());

                var $sbListForCondition3 = $(tblLayout3.toTagString());
    
                listforParamDomContainer.append($sbListForCondition1);
                listforParamDomContainer.append($sbListForCondition2);
                listforParamDomContainer.append($sbListForCondition3 );
                listforParamDomBody.append(listforParamDomContainer);
            });
            forBlockOption.append(listforParamDomBody);

            var listforLastBracket = $(`<div class='vp-apiblock-style-flex-row'>
                                            <span class='vp-apiblock-style-flex-column-center'
                                                style='margin-left: 5px; 
                                                color:#E85401;'> ]
                                            </span>
                                      </div>`);
            forBlockOption.append(listforLastBracket);

            var plusButton = MakeOptionPlusButton(VP_ID_APIBLOCK_OPTION_LIST_FOR_PLUS + uuid, '+ Condition');
            forBlockOption.append(plusButton);

            $(optionPageSelector).append(forBlockOption);

            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_RETURN_VAR + uuid).val(listforReturnVarState);
            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_PREV_EXPRESSION + uuid).val(listforPrevExpression);

            var listforConditionListState = thatBlock.getState(STATE_listforConditionList);  
            listforConditionListState.forEach((listforParam, index) => {
                const { arg1, arg2, arg3, arg4, arg5, arg6, arg7,
                        arg10, arg11, arg12, arg13, arg14, arg15 } = listforParam;
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_1 + index + uuid).val(arg1);
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_2 + index + uuid).val(arg2);
                if (arg3 == FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_3 + index + uuid).val(STR_NULL);
                } else {
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_3 + index + uuid).val(arg3);
                }
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_4 + index + uuid).val(arg4);
    
                /** For arg4 */
                if (arg3 == FOR_BLOCK_ARG3_TYPE.ENUMERATE) {
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_4 + index + uuid).addClass(VP_CLASS_STYLE_OPACITY_1);
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_4 + index + uuid).css('margin-left','5px');
                } else {
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_4 + index + uuid).addClass(VP_CLASS_STYLE_OPACITY_0);
                }
    
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_5 + index + uuid).val(arg5);
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_6 + index + uuid).val(arg6);
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_7 + index + uuid).val(arg7);

                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_10 + index + uuid).val(arg10);
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_11 + index + uuid).val(arg11);
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_12 + index + uuid).val(arg12);
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_13 + index + uuid).val(arg13);
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_14 + index + uuid).val(arg14);
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid).val(arg15);

                if (arg14 == 'none' || arg14 == STR_NULL) {
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_14 + index + uuid).addClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid).attr("disabled", true);
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid).addClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                } else {
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_14 + index + uuid).removeClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid).attr("disabled", false);
                
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LIST_FOR_ARG_15 + index + uuid).removeClass(VP_CLASS_STYLE_BGCOLOR_C4C4C4);
                }   
            });

        }

        renderThisComponent();
    }

    return InitListForBlockOption;
});
define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpLineNumberTextArea'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb, vpLineNumberTextArea, vpSuggestInputText
    
                , api, config, constData, blockRenderer, baseComponent ) {
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
            , ControlToggleInput
            , SetTextareaLineNumber_apiBlock } = api;

    const { PROCESS_MODE } = config;

    const { GenerateLambdaParamList } = blockRenderer;

    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , FOR_BLOCK_TYPE

            , STR_NULL
            , STR_COLON_SELECTED
            , STR_FOR
            , STR_SELECTED
            , STR_CHANGE_KEYUP_PASTE
            , STR_CLICK
            , STR_CHANGE
            , STR_STRONG
            , STR_FLEX
            , STR_NONE
            , STR_DISPLAY
            , STR_LAMBDA
            , STR_VALUE
            , STR_VARIABLE

            , LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE

            , VP_ID_PREFIX 
            , VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_1
            , VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_2
            , VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_2_M
            , VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_3
            , VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_4
            
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
            , STATE_lambdaArg1
            , STATE_lambdaArg2List
            , STATE_lambdaArg2m_List
            , STATE_lambdaArg3
            , STATE_lambdaArg4List

            , COLOR_LIST
             } = constData;

    const { MakeOptionContainer
            , MakeOptionDeleteButton
            , MakeOptionPlusButton
            , MakeVpSuggestInputText_apiblock
            , MakeLineNumberTextArea_apiblock
            , MakeOptionInput
            , MakeOptionButton_type2 } = baseComponent;

    var $lineNumberTextArea = null;
    var InitLambdaBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();
        var blockContainerThis = thatBlock.getBlockContainerThis();
        var importPackageThis = blockContainerThis.getImportPackageThis();


        var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2List);
        lambdaArg2ListState.forEach((lambdaArg2, index) => {

            /**
             * @event_function
             * Lambda arg2 변경 이벤트 함수
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_2 +index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_2 +index + uuid, function(event) {
                var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2List);

                var updatedValue =  $(this).val();
 
                lambdaArg2ListState = UpdateOneArrayValueAndGet(lambdaArg2ListState, index, updatedValue);
                thatBlock.setState({
                    [STATE_lambdaArg2List]: lambdaArg2ListState
                });

                var lambdaCode = GenerateLambdaParamList(thatBlock);
                $(`.vp-block-header-${uuid}`).html(lambdaCode);
  
                event.stopPropagation();
            });
        });


        var lambdaArg2mListState = thatBlock.getState(STATE_lambdaArg2m_List);
        lambdaArg2mListState.forEach((lambdaArg2, index) => {
            /**
             * @event_function
             * Lambda arg2 m 변경 이벤트 함수
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_2_M +index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_2_M +index + uuid, function(event) {
                var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2m_List);

                var updatedValue =  $(this).val();
   
                lambdaArg2ListState = UpdateOneArrayValueAndGet(lambdaArg2ListState, index, updatedValue);
                thatBlock.setState({
                    [STATE_lambdaArg2m_List]: lambdaArg2ListState
                });

                var lambdaCode = GenerateLambdaParamList(thatBlock);
                $(`.vp-block-header-${uuid}`).html(lambdaCode);
             

                event.stopPropagation();
            });
        });
       /** 
         * @event_function
         * Lambda arg2 생성 이벤트 함수 바인딩 
         */
        $(document).off(STR_CLICK, vpCommon.wrapSelector(`.vp-block-lambda-arg2-plus-button-${uuid}`));
        $(document).on(STR_CLICK, vpCommon.wrapSelector(`.vp-block-lambda-arg2-plus-button-${uuid}`), function(event) {
            var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2List);
            var lambdaArg2ListLength = lambdaArg2ListState.length;

            // thatBlock.addVariableIndex();
            // var variableIndex = thatBlock.getVariableIndex();
            var newLambdaArg2 = ''

            lambdaArg2ListState = CreateOneArrayValueAndGet(lambdaArg2ListState, lambdaArg2ListLength, newLambdaArg2);
            thatBlock.setState({
                lambdaArg2List: lambdaArg2ListState
            });

            var lambdaCode = GenerateLambdaParamList(thatBlock);
            $(`.vp-block-header-${uuid}`).html(lambdaCode);

            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });


        /** 
         * @event_function
         * Lambda arg2 삭제 이벤트 함수 바인딩 
         */
        $(document).off(STR_CLICK, vpCommon.wrapSelector(`.vp-block-lambda-arg2-delete-button-${uuid}`));
        $(document).on(STR_CLICK, vpCommon.wrapSelector(`.vp-block-lambda-arg2-delete-button-${uuid}`), function(event) {
            var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2List);
            var lambdaArg2ListLength = lambdaArg2ListState.length;
            // if (lambdaArg2ListState.length == 1) {
            //     return;
            // }
            
            lambdaArg2ListState = DeleteOneArrayValueAndGet(lambdaArg2ListState, lambdaArg2ListLength-1);
            thatBlock.setState({
                lambdaArg2List: lambdaArg2ListState
            });

            var lambdaCode = GenerateLambdaParamList(thatBlock);
            $(`.vp-block-header-${uuid}`).html(lambdaCode);

            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });


        /** 
         * @event_function
         * Lambda arg2 m 생성 이벤트 함수 바인딩 
         */
        $(document).off(STR_CLICK, vpCommon.wrapSelector(`.vp-block-lambda-arg2-m-plus-button-${uuid}`));
        $(document).on(STR_CLICK, vpCommon.wrapSelector(`.vp-block-lambda-arg2-m-plus-button-${uuid}`), function(event) {
            var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2m_List);
            var lambdaArg2ListLength = lambdaArg2ListState.length;

            // thatBlock.addVariableIndex();
            // var variableIndex = thatBlock.getVariableIndex();
            var newLambdaArg2 = '';

            lambdaArg2ListState = CreateOneArrayValueAndGet(lambdaArg2ListState, lambdaArg2ListLength, newLambdaArg2);
            thatBlock.setState({
                [STATE_lambdaArg2m_List]: lambdaArg2ListState
            });

            var lambdaCode = GenerateLambdaParamList(thatBlock);
            $(`.vp-block-header-${uuid}`).html(lambdaCode);

            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });


        /** 
         * @event_function
         * Lambda arg2 m 삭제 이벤트 함수 바인딩 
         */
        $(document).off(STR_CLICK, vpCommon.wrapSelector(`.vp-block-lambda-arg2-m-delete-button-${uuid}`));
        $(document).on(STR_CLICK, vpCommon.wrapSelector(`.vp-block-lambda-arg2-m-delete-button-${uuid}`), function(event) {
            var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2m_List);
            var lambdaArg2ListLength = lambdaArg2ListState.length;
            // if (lambdaArg2ListState.length == 1) {
            //     return;
            // }
            
            lambdaArg2ListState = DeleteOneArrayValueAndGet(lambdaArg2ListState, lambdaArg2ListLength-1);
            thatBlock.setState({
                [STATE_lambdaArg2m_List]: lambdaArg2ListState
            });

            var lambdaCode = GenerateLambdaParamList(thatBlock);
            $(`.vp-block-header-${uuid}`).html(lambdaCode);

            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });

         /**
          * @event_function
          * Lambda arg3변경 이벤트 함수
          */
        $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_3 + uuid);
        $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_3 + uuid, function(event) {
            
            var updatedValue =  $(this).val();
            thatBlock.setState({
                lambdaArg3: updatedValue
            });

            var lambdaCode = GenerateLambdaParamList(thatBlock);
            $(`.vp-block-header-${uuid}`).html(lambdaCode);

            event.stopPropagation();
        });

        var lambdaArg4ListState = thatBlock.getState(STATE_lambdaArg4List);
        lambdaArg4ListState.forEach((lambdaArg4,index) => {
            /**
             * @event_function
             * Lambda arg4 변경 이벤트 함수
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_4 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_4 + index + uuid, function(event) {
                var lambdaArg4ListState = thatBlock.getState(STATE_lambdaArg4List);

                var updatedValue =  $(this).val();

                lambdaArg4ListState = UpdateOneArrayValueAndGet(lambdaArg4ListState, index, updatedValue);
                thatBlock.setState({
                    lambdaArg4List: lambdaArg4ListState
                });

                var lambdaCode = GenerateLambdaParamList(thatBlock);
                $(`.vp-block-header-${uuid}`).html(lambdaCode);

                event.stopPropagation();
            });
    
        });

    
        /** 
         * @event_function
         * Lambda arg4 생성 이벤트 함수 바인딩 
         */
        $(document).off(STR_CLICK, vpCommon.wrapSelector(`#vp-apiblock-plus-button-${uuid}`));
        $(document).on(STR_CLICK, vpCommon.wrapSelector(`#vp-apiblock-plus-button-${uuid}`), function(event) {
            var lambdaArg4ListState = thatBlock.getState(STATE_lambdaArg4List);
            var lambdaArg4ListLength = lambdaArg4ListState.length;
            
            var newLambdaArg4 = '';

            lambdaArg4ListState = CreateOneArrayValueAndGet(lambdaArg4ListState, lambdaArg4ListLength, newLambdaArg4);
            thatBlock.setState({
                lambdaArg4List: lambdaArg4ListState
            });

            var lambdaCode = GenerateLambdaParamList(thatBlock);
            $(`.vp-block-header-${uuid}`).html(lambdaCode);

            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });

        /** 
         * @event_function
         * Lambda arg4 삭제 이벤트 함수 바인딩 
         */
        $(document).off(STR_CLICK, vpCommon.wrapSelector(`#vp-apiblock-delete-button-${uuid}`));
        $(document).on(STR_CLICK, vpCommon.wrapSelector(`#vp-apiblock-delete-button-${uuid}`), function(event) {
            var lambdaArg4ListState = thatBlock.getState(STATE_lambdaArg4List);
            var lambdaArg4ListLength = lambdaArg4ListState.length;
            if (lambdaArg4ListState.length == 1) {
                return;
            }
            
            lambdaArg4ListState = DeleteOneArrayValueAndGet(lambdaArg4ListState, lambdaArg4ListLength-1);

            thatBlock.setState({
                lambdaArg4List: lambdaArg4ListState
            });

            var lambdaCode = GenerateLambdaParamList(thatBlock);
            $(`.vp-block-header-${uuid}`).html(lambdaCode);

            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });


        /**
         * @event_function
         * List for 리턴 변수(arg1) 이름 변경 이벤트 함수
         */
        $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_1 + uuid);
        $(document).on(STR_CHANGE_KEYUP_PASTE,VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_1 + uuid, function(event) {
            thatBlock.setState({
                lambdaArg1: $(this).val()
            });

            var lambdaCode = GenerateLambdaParamList(thatBlock);
            $(`.vp-block-header-${uuid}`).html(lambdaCode);

            event.stopPropagation();
        });

        var bindSelectValueEventFunc_lambda = function(selectedValue, index, argType) {
      
            if (LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE.ARG1 == argType) {
                thatBlock.setState({
                    lambdaArg1: selectedValue
                });
            
            } else if (LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE.ARG2 == argType) {
                var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2List);
                lambdaArg2ListState = UpdateOneArrayValueAndGet(lambdaArg2ListState, index, selectedValue);
                thatBlock.setState({
                    [STATE_lambdaArg2List]: lambdaArg2ListState
                });

            } else if (LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE.ARG2_M == argType) {
                var lambdaArg2ListState_m = thatBlock.getState(STATE_lambdaArg2m_List);
                lambdaArg2ListState_m = UpdateOneArrayValueAndGet(lambdaArg2ListState_m, index, selectedValue);
                thatBlock.setState({
                    [STATE_lambdaArg2m_List]: lambdaArg2ListState_m
                });

            } else if (LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE.ARG3 == argType) {
                thatBlock.setState({
                    lambdaArg3: selectedValue
                });

            } else if (LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE.ARG4 == argType) {
                var lambdaArg4ListState = thatBlock.getState(STATE_lambdaArg4List);
                lambdaArg4ListState = UpdateOneArrayValueAndGet(lambdaArg4ListState, index, selectedValue);
                thatBlock.setState({
                    [STATE_lambdaArg4List]: lambdaArg4ListState
                });
            }

            var lambdaCode = GenerateLambdaParamList(thatBlock);
            $(`.vp-block-header-${uuid}`).html(lambdaCode);

            // if (LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE.ARG4 == argType) {
            //     $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_4 + index+ uuid);
            //     blockContainerThis.renderBlockOptionTab();
            // }
        }

        /** Lambda option 렌더링 */
        var renderThisComponent = function() {
            var loadedVariableNameList = blockContainerThis.getKernelLoadedVariableNameList();
            var loadedVariableNameList_arg1 = [ ...loadedVariableNameList, `lambda_func`];
            var loadedVariableNameList_arg4 = [ 'list','map','reduce','filter'];
            var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2List);
            var lambdaArg2m_ListState = thatBlock.getState(STATE_lambdaArg2m_List);
            var lambdaArg3State = thatBlock.getState(STATE_lambdaArg3);
            var lambdaArg4ListState = thatBlock.getState(STATE_lambdaArg4List);

            var lambdaBlockOption = MakeOptionContainer();

            var lambdaArg1State = thatBlock.getState(STATE_lambdaArg1);
            var sbforParamArg1 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_1 + uuid
                                                                ,lambdaArg2ListState
                                                                ,loadedVariableNameList_arg1
                                                                , VP_CLASS_STYLE_WIDTH_30PERCENT
                                                                , 'Return Var'
                                                                , function(selectedValue) {
                                                                    bindSelectValueEventFunc_lambda(selectedValue,
                                                                        0 
                                                                        ,LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE.ARG1);
                                                                });
            var lambdaArg1Dom = $(`<div class='vp-apiblock-style-flex-row'
                                           style='margin-top:5px;'>
                                        ${sbforParamArg1}
                           

                                        <span class='vp-apiblock-style-flex-column-center'
                                            style='margin-left: 5px;
                                                   margin-right: 5px;'> 
                                            =
                                        </span>

                                    </div>`);
  
            var lambdaConditionContainer = $(`<div class='vp-apiblock-style-flex-row-wrap'   
                                                   style='margin-top: 5px;'></div>`);
            var lambdaConditionContainer2 = $(`<div class='vp-apiblock-style-flex-row-wrap'
                                                    style='margin-top: 5px;'></div>`);        
            var lambdaConditionContainer3 = $(`<div id='vp_apiblock_lambda_arg3_container'
                                                    class='vp-apiblock-style-flex-row'
                                                    style='margin-top: 5px;'></div>`);
            var lambdaConditionContainer4 = $(`<div class='vp-apiblock-style-flex-row-wrap'
                                                    style='margin-top: 5px;'></div>`);


            var leftBracketDom = $(`<span class='vp-apiblock-style-flex-column-center'
                                          style='margin-left: 5px;'>
                                            (
                                    </span>`);
                                    
            lambdaConditionContainer2.append(leftBracketDom);                                            
            var lambdaArg2ContainerDom = $(`<div class='vp-apiblock-style-flex-row'>

                                                        <span class='vp-apiblock-style-flex-column-center'
                                                            style='margin-left: 5px;'>
                                                            lambda
                                                        </span>

                                                        <button class='vp-apiblock-option-button-type2
                                                                       vp-block-lambda-arg2-plus-button-${uuid}'
                                                                style='margin-left: 5px; 
                                                                    color:#E85401;'>
                                                            +
                                                        </button>

                                                        <button class='vp-apiblock-option-button-type2
                                                                       vp-block-lambda-arg2-delete-button-${uuid}'
                                                                style='margin-left: 5px; 
                                                                        color:#E85401;'>
                                                            -
                                                        </button>
                                                     
                                                    </div>`);

            lambdaConditionContainer2.append(lambdaArg2ContainerDom);
            lambdaArg2ListState.forEach((lambdaArg2, arg2Index) => {

                var loadedVariableNameList_arg2 = [ ...loadedVariableNameList, `lam_x${arg2Index + 1}`];
               
                if ( arg2Index != 0 ) {
                    var comma = $(`<span class='vp-apiblock-style-flex-column-center'
                                        style='margin-left: 5px;'>
                                        ,
                                    </span>`);
                    lambdaConditionContainer2.append(comma); 
                } 
                var sbforParamArg2 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_2 + arg2Index + uuid
                                                                    ,lambdaArg2
                                                                    ,loadedVariableNameList_arg2
                                                                    , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                    , STR_VARIABLE + ' ' +arg2Index
                                                                    , function(selectedValue) {
                                                                        bindSelectValueEventFunc_lambda(selectedValue,
                                                                            arg2Index 
                                                                            ,LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE.ARG2);
                                                                    });

                // var lambdaArg2Dom = $(`<input class='vp-apiblock-option-input
                //                                      vp-apiblock-blockoption-lambda-arg2-${arg2Index}-${uuid}'
                //                                 style='margin-left: 5px; width:15%;'
                //                                 value='${lambdaArg2}'
                //                                 placeholder='var_${arg2Index}'>
                //                         </input>`);
    
                lambdaConditionContainer2.append(sbforParamArg2); 
            });      
     
            var lastBracketDom = $(`<span class='vp-apiblock-style-flex-column-center'
                                                style='margin-left: 5px;'>
                                                ) 
                                            </span>
                                            <span class='vp-apiblock-style-flex-column-center'
                                                style='margin-left: 5px;'>
                                                :
                                            </span>`);

            lambdaConditionContainer2.append(lastBracketDom);

            lambdaArg4ListState.forEach((lambdaArg4, index) => {
                var sbforParamArg4 = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_4 + index + uuid
                                                                ,lambdaArg4
                                                                ,loadedVariableNameList_arg4
                                                                , VP_CLASS_STYLE_WIDTH_100PERCENT
                                                                , `Method ${index}`
                                                                , function(selectedValue) {
                                                                    bindSelectValueEventFunc_lambda(selectedValue,
                                                                        index 
                                                                        ,LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE.ARG4);
                                                                });
                var lambdaMethodDom = $(`<div class='vp-apiblock-style-flex-row'
                                                style='width:25%;'>

                           
                                    
                                        </div>`);
                var lambdaMethodLeftBracketDom = $(`<span class='vp-apiblock-style-flex-column-center'
                                                        style=' margin-left: 5px;'>
                                                        ( 
                                                    </span>`);
                lambdaMethodDom.append(sbforParamArg4);
                lambdaMethodDom.append(lambdaMethodLeftBracketDom);
                lambdaConditionContainer.append(lambdaMethodDom); 
            });

            // var lineNumberTextArea = new vpLineNumberTextArea.vpLineNumberTextArea(`vp_apiblockLambdaArg3${uuid}`, 
            //                                                                         '');
            var lineNumberTextArea = MakeLineNumberTextArea_apiblock(VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_3 + uuid,lambdaArg3State)
            // var lineNumberTextArea = $(`<input class='vp-apiblock-option-input'
            //                                     id='vp_apiblockLambdaArg3${uuid}' 
            //                                    value='${lambdaArg3State}' 
            //                                    style='height:60px;'
            //                                    placeholder='str(x1) if x1 % 2 == 0 else x1'>
            //                                 </input>`);
            lambdaConditionContainer3.append( lineNumberTextArea);
            // $lineNumberTextArea = lineNumberTextArea.toTagString(); 
            // lambdaConditionContainer3.append( $lineNumberTextArea);

            lambdaArg4ListState.forEach( (_,index) => {
                if ( index == 0) {
                    if (lambdaArg2m_ListState.length != 0) {
                        var leftBracketDom = $(`<span class='vp-apiblock-style-flex-column-center'
                                                        style='margin-left: 5px;'>
                                                    (
                                                </span>`);
                        lambdaConditionContainer4.append(leftBracketDom);
                    }
                    var lambdaArg2ContainerDom = $(`<div class='vp-apiblock-style-flex-row'>

                                                        <button class='vp-apiblock-option-button-type2
                                                                    vp-block-lambda-arg2-m-plus-button-${uuid}'
                                                                style='margin-left: 5px; 
                                                                    color:#E85401;'>
                                                            +
                                                        </button>

                                                        <button class='vp-apiblock-option-button-type2
                                                                        vp-block-lambda-arg2-m-delete-button-${uuid}'
                                                                style='margin-left: 5px; 
                                                                        color:#E85401;'>
                                                            -
                                                        </button>
                                                        
                                                    </div>`);
                    lambdaConditionContainer4.append(lambdaArg2ContainerDom); 

                    lambdaArg2m_ListState.forEach((lambdaArg2_m, arg2Index) => {
                        var loadedVariableNameList_arg2_m = [ ...loadedVariableNameList, `lam_y${arg2Index + 1}`];
                        if (arg2Index == 0) {
                          
                        } else {
                            var comma = $(`<span class='vp-apiblock-style-flex-column-center'
                                                    style='margin-left: 5px;'>
                                                    ,
                                               </span>`);
                            lambdaConditionContainer4.append(comma); 
                        }
                        var sbforParamArg2_m = MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_2_M + arg2Index + uuid
                                                                        , lambdaArg2_m
                                                                        , loadedVariableNameList_arg2_m
                                                                        , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                        , 'Return Var' + arg2Index
                                                                        , function(selectedValue) {
                                                                            bindSelectValueEventFunc_lambda(selectedValue,
                                                                                arg2Index 
                                                                                ,LAMBDA_BLOCK_SELECT_VALUE_ARG_TYPE.ARG2_M);
                                                                        });
                        // var lambdaArg2Dom = $(`<input class='vp-apiblock-option-input
                        //                                      vp-apiblock-blockoption-lambda-arg2-m-${arg2Index}-${uuid}'
                        //                               style='margin-left: 5px; width:15%;'
                        //                               value='${lambdaArg2}'
                        //                               placeholder='var_${arg2Index}'>
                        //                        </input>`);
                        lambdaConditionContainer4.append(sbforParamArg2_m);
                        // lambdaConditionContainer4.append(lambdaArg2Dom);                      
                    });    
                    if (lambdaArg2ListState.length != 0) {
                        var rightBracketDom = $(`<span class='vp-apiblock-style-flex-column-center'
                                                    style='margin-left: 5px;'>
                                                    ) 
                                                </span>`);
                        lambdaConditionContainer4.append(rightBracketDom);
                    }
                }
                var lastBracketDom = $(`<span class='vp-apiblock-style-flex-column-center'
                                              style='margin-left: 5px;'>
                                                ) 
                                        </span>`);
                lambdaConditionContainer4.append(lastBracketDom);
            });

            var plusBtn = MakeOptionButton_type2(`vp-apiblock-plus-button-${uuid}`, '' , '+');
            var deleteBtn = MakeOptionButton_type2(`vp-apiblock-delete-button-${uuid}`, '' , '-');

            lambdaArg1Dom.append(plusBtn);
            lambdaArg1Dom.append(deleteBtn);

            /** Lambda option arg1 리턴 변수 렌더링 생성 */
            lambdaBlockOption.append(lambdaArg1Dom);
      
            /** Lambda condition 렌더링 생성 */
            lambdaBlockOption.append(lambdaConditionContainer);
            lambdaBlockOption.append(lambdaConditionContainer2);
            lambdaBlockOption.append(lambdaConditionContainer3);
            lambdaBlockOption.append(lambdaConditionContainer4);

            $(optionPageSelector).append(lambdaBlockOption);

            var lambdaArg1 = thatBlock.getState(STATE_lambdaArg1);
            var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2List);
            var lambdaArg2m_ListState = thatBlock.getState(STATE_lambdaArg2m_List);
            var lambdaArg3State = thatBlock.getState(STATE_lambdaArg3);
            var lambdaArg4ListState = thatBlock.getState(STATE_lambdaArg4List);

            $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_1 + uuid).val(lambdaArg1);

            lambdaArg2ListState.forEach((arg2, arg2Index) => {
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_2 + arg2Index + uuid).val(arg2);
            });
            lambdaArg2m_ListState.forEach((arg2_m, arg2Index_m) => {
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_2_M + arg2Index_m + uuid).val(arg2_m);
            });

            var indexArg4 = lambdaArg4ListState.length;
            // while(indexArg4 -- != 0) {
            //     console.log('indexArg4',indexArg4, lambdaArg4ListState[indexArg4]);
            //     $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_4 + indexArg4 + uuid).val(lambdaArg4ListState[indexArg4]);
            // }
            lambdaArg4ListState.forEach((arg4, arg4Index) => {
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_4 + arg4Index + uuid).val(arg4);
            });

            SetTextareaLineNumber_apiBlock(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_LAMBDA_ARG_3 + uuid, lambdaArg3State);
        }

        renderThisComponent();
    }

    return InitLambdaBlockOption;
});
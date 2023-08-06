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
            api, config, constData, blockRenderer, baseComponent ) {
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

    const {  RenderOptionPageName

            , RenderInputRequiredColor  

            , GenerateClassInParamList
            , GenerateDefInParamList
            , GenerateReturnOutParamList
            , GenerateIfConditionList
            , GenerateForParam } = blockRenderer;

    const { BLOCK_DIRECTION
            , BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , DEF_BLOCK_ARG4_TYPE
            , DEF_BLOCK_ARG4_TYPE_EXCEPT_INPUT_STR
            , DEF_BLOCK_ARG6_TYPE
            , DEF_BLOCK_SELECT_VALUE_ARG_TYPE

            , VP_ID_PREFIX
            , VP_ID_APIBLOCK_OPTION_DEF_ARG_3
            , VP_ID_APIBLOCK_OPTION_DEF_ARG_4
            , VP_ID_APIBLOCK_OPTION_DEF_ARG_5
            , VP_ID_APIBLOCK_OPTION_DEF_ARG_6
            , VP_ID_APIBLOCK_OPTION_DEF_RETURN_TYPE
            , VP_CLASS_PREFIX 
            , VP_CLASS_APIBLOCK_BLOCK_HEADER
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

            , VP_CLASS_APIBLOCK_PARAM_DELETE_BTN
            , VP_CLASS_APIBLOCK_PARAM_PLUS_BTN

            , STR_COLON_SELECTED
            , STR_NULL
            , STR_FOR
            , STR_VARIABLE
            , STR_INPUT
            , STR_CLICK
            , STR_CHANGE
            , STR_CHANGE_KEYUP_PASTE

            , STATE_defName
            , STATE_defInParamList
            , STATE_defReturnType
            , STATE_customCodeLine
        
            , DEF_PARAM_TYPE_LIST} = constData;

    const { MakeOptionContainer
                , MakeOptionDeleteButton
                , MakeOptionPlusButton
                , MakeVpSuggestInputText_apiblock
                , MakeOptionInput
                , MakeOptionSelectBox } = baseComponent;

    var InitDefBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();
        var blockContainerThis = thatBlock.getBlockContainerThis();

        /** Def 이름 변경 이벤트 함수 */
        $(document).off(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-input-def-name-${uuid}`);
        $(document).on(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-input-def-name-${uuid}`, function(event) {
            RenderInputRequiredColor(this);

            thatBlock.setState({
                defName: $(this).val()
            });

            $(`.vp-block-header-def-name-${thatBlock.getUUID()}`).html($(this).val());
            event.stopPropagation();
        });

        /** Def block property 변경 이벤트 함수 */
        $(document).off(STR_INPUT, `.vp-apiblock-defproperty-input-${uuid}`);
        $(document).on(STR_INPUT, `.vp-apiblock-defproperty-input-${uuid}`, function(event) {
            var inputValue = $(this).val();
            var propertyBlock = thatBlock.getPropertyBlockFromDef();
            var prevBlockFromDef = null;
                
            /** property block 삭제 */
            if ( inputValue == STR_NULL 
                 && thatBlock.getPrevBlock() != null ) {
                prevBlockFromDef = thatBlock.getPrevBlock();
                /** property block이 root block일 경우 */
                if (prevBlockFromDef.getPrevBlock() == null) {
                    if ( prevBlockFromDef ) {
                    var nextBlockList = prevBlockFromDef.getNextBlockList();
                        nextBlockList.some(( nextBlock, index) => {
                            if (nextBlock.getUUID() == thatBlock.getUUID()) {
                                nextBlockList.splice(index, 1)
                                return true;
                            }
                        });
                    }
    
                    thatBlock.setPrevBlock(null);
                    thatBlock.setDirection(BLOCK_DIRECTION.ROOT);
                    prevBlockFromDef._deleteBlockDomAndData();
    
                    thatBlock.setPropertyBlockFromDef(null);
                    /** property block이 root block이 아닐 경우 */      
                } else {
                    prevBlockFromDef.deleteLowerDepthChildBlocks();
                    thatBlock.setPropertyBlockFromDef(null);
                }
            } else {
                /** property block 생성 */  
                if ( propertyBlock == null ) {
                    prevBlockFromDef = thatBlock.getPrevBlock();
                    var defBlockDirection = thatBlock.getDirection();
                    var newBlock = null;

                    newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.PROPERTY);
                    thatBlock.setPropertyBlockFromDef(newBlock);

                     /** this block이 root block이 아닐 경우 */   
                    if (prevBlockFromDef != null) {
                        prevBlockFromDef.appendBlock(newBlock, defBlockDirection);
                        /** this block이 root block일 경우 */   
                    }  else {
                        newBlock.appendBlock(thatBlock, BLOCK_DIRECTION.DOWN);
                    }
         
                    newBlock.setState({
                        customCodeLine : inputValue
                    });
                    newBlock.bindEventAll();
           
                    blockContainerThis.reRenderBlockList();
                    blockContainerThis.renderBlockLineNumberInfoDom(true);
                    blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
                    $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(newBlock.getState(STATE_customCodeLine));
                /** property block 변경 */  
                } else {
                    propertyBlock.setState({
                        customCodeLine : inputValue
                    });
                    propertyBlock.bindEventAll();
                    $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(propertyBlock.getState(STATE_customCodeLine));
                }
            }
    
            blockContainerThis.reRenderBlockList();
            blockContainerThis.renderBlockLineNumberInfoDom(true);
            blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
            event.stopPropagation();
        });


        /**
         * @event_function
         * Def block 파라미터 생성 
         */
        $(document).off(STR_CLICK, vpCommon.wrapSelector(VP_ID_PREFIX + VP_CLASS_APIBLOCK_PARAM_PLUS_BTN + uuid));
        $(document).on(STR_CLICK, vpCommon.wrapSelector(VP_ID_PREFIX + VP_CLASS_APIBLOCK_PARAM_PLUS_BTN + uuid), function(event) {

            var inParamList = thatBlock.getState(STATE_defInParamList);

            var newData = {
                arg3: STR_NULL
                , arg4: STR_NULL
                , arg5: STR_NULL
                , arg6: DEF_BLOCK_ARG6_TYPE.NONE
            }
            thatBlock.setState({
                [STATE_defInParamList]: [ ...inParamList, newData ]
            });

            var defInParamStr = GenerateDefInParamList(thatBlock);
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(defInParamStr);
            blockContainerThis.renderBlockOptionTab(); 
            
            event.stopPropagation();
        });

        var defInParamList = thatBlock.getState(STATE_defInParamList);
        defInParamList.forEach((_, index ) => {
            /**
             * @event_function
             * Def block 파라미터 삭제 
             */
            $(document).off(STR_CLICK, VP_ID_PREFIX + VP_CLASS_APIBLOCK_PARAM_DELETE_BTN + index + uuid);
            $(document).on(STR_CLICK, VP_ID_PREFIX + VP_CLASS_APIBLOCK_PARAM_DELETE_BTN + index + uuid, function() {
                var inParamList = thatBlock.getState(STATE_defInParamList);
                // var index = inParamList.length-1;
                thatBlock.setState({
                    [`${STATE_defInParamList}`]:  DeleteOneArrayValueAndGet(inParamList, index)
                });
        
                blockContainerThis.renderBlockOptionTab(); 
                var inParamStr = GenerateDefInParamList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(inParamStr);
            });
            /** 
             * @event_function
             * def 이름 변경 이벤트 함수 바인딩 arg3
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE,  VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_3+ index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE,  VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_3+ index + uuid, function() {
                var defInParam = thatBlock.getState(STATE_defInParamList)[index];
                RenderInputRequiredColor(this);
                var changedParamName = $(this).val();
            
                var updatedData = {
                    ...defInParam
                    , arg3: changedParamName
               
                }
   
                thatBlock.setState({
                    defInParamList:   UpdateOneArrayValueAndGet( thatBlock.getState(STATE_defInParamList), index, updatedData)
                });
                var defInParamStr = GenerateDefInParamList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(defInParamStr);
            });

            /** 
             * @event_function
             * def custom param type select 변경 이벤트 함수 바인딩 arg4
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_4 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_4 + index + uuid, function(event) {
                var defInParam = thatBlock.getState(STATE_defInParamList)[index];
                var paramCustomTypeVal = $(this).val();
                var updatedData = {
                    ...defInParam
                    , arg4: paramCustomTypeVal
                }
       
                thatBlock.setState({
                    [STATE_defInParamList]:   UpdateOneArrayValueAndGet( thatBlock.getState(STATE_defInParamList), index, updatedData)
                });
                var defInParamStr = GenerateDefInParamList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(defInParamStr);

                event.stopPropagation();
            });

            /** 
             * @event_function
             * def default value 변경 이벤트 함수 바인딩 
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE,  VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_5 + index + uuid);
            $(document).on(STR_CHANGE_KEYUP_PASTE,  VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_5 + index + uuid, function() {
                var defInParam = thatBlock.getState(STATE_defInParamList)[index];
                var changedDefaultVal = $(this).val();
            
                var updatedData = {
                    ...defInParam
                    , arg5 : changedDefaultVal
                    
                }
                thatBlock.setState({
                    defInParamList:  UpdateOneArrayValueAndGet( thatBlock.getState(STATE_defInParamList), index, updatedData)
                });
                var defInParamStr = GenerateDefInParamList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(defInParamStr);
            });

            /** 
             * @event_function
             * def param type select 변경 이벤트 함수 바인딩  arg4
             */
            $(document).off(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_6+ index + uuid);
            $(document).on(STR_CHANGE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_6+ index + uuid, function() {
                var defInParam = thatBlock.getState(STATE_defInParamList)[index];
                var updatedData = {
                    ...defInParam
                    , arg6 : $(STR_COLON_SELECTED, this).val()   
                }
           
                thatBlock.setState({
                    defInParamList:   UpdateOneArrayValueAndGet( thatBlock.getState(STATE_defInParamList), index, updatedData)
                });
                var defInParamStr = GenerateDefInParamList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(defInParamStr);
                blockContainerThis.renderBlockOptionTab();
            });

        });

        /** 
            * @event_function
            * def Return Type 입력 변경 이벤트 함수 바인딩 
        */
        $(document).off(STR_CHANGE_KEYUP_PASTE,  VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_RETURN_TYPE + uuid);
        $(document).on(STR_CHANGE_KEYUP_PASTE,  VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_RETURN_TYPE + uuid, function() {

            var changedValue = $(this).val();
            
            thatBlock.setState({
                [STATE_defReturnType]: changedValue
            });
      
            var defInParamStr = GenerateDefInParamList(thatBlock);
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(defInParamStr);
        });

        var bindSelectValueEventFunc_def = function(selectedValue, index, argType) {
            var defParamListState = thatBlock.getState(STATE_defInParamList);
            var defParamState = defParamListState[index];
            var updatedValue;

            if (argType == DEF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG3) {
                updatedValue = {
                    ...defParamState
                    , arg3: selectedValue 
                }
        
            } else if (argType == DEF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG4) {
                updatedValue = {
                    ...defParamState
                    , arg4: selectedValue 
                }
            } else if (argType == DEF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG5) {
                updatedValue = {
                    ...defParamState
                    , arg5: selectedValue 
                }
       
            } else if (argType == DEF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG6) {
                updatedValue = {
                    ...defParamState
                    , arg6: selectedValue 
                }
                
            } else if (argType == DEF_BLOCK_SELECT_VALUE_ARG_TYPE.RETURN_TYPE){
                thatBlock.setState({
                    [STATE_defReturnType]: selectedValue
                });
          
                var defInParamStr = GenerateDefInParamList(thatBlock);
                $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(defInParamStr);
                $(document).off(STR_CHANGE_KEYUP_PASTE, VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_RETURN_TYPE + uuid);
                blockContainerThis.renderBlockOptionTab();
                return;
            }

            defParamListState = UpdateOneArrayValueAndGet(defParamListState, index, updatedValue);
            thatBlock.setState({
                [STATE_defInParamList]: defParamListState
            });
            var defParamCode = GenerateDefInParamList(thatBlock);
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + uuid).html(defParamCode);
        
        }

        /** Def option 렌더링 */
        var renderThisComponent = function() {

            var defBlockOption = MakeOptionContainer();
            var defReturnTypeState = thatBlock.getState(STATE_defReturnType);

            /** def property */

            var propertyBlock = null;
            var propertyCodeLineState = STR_NULL;
            /** def block 바로 위에 property block이 있을 경우 */
            if (thatBlock.getPrevBlock() 
                 && thatBlock.getPrevBlock().getBlockCodeLineType() == BLOCK_CODELINE_TYPE.PROPERTY ) {
                thatBlock.setPropertyBlockFromDef(thatBlock.getPrevBlock());
                propertyBlock = thatBlock.getPropertyBlockFromDef();
                propertyCodeLineState = propertyBlock.getState(STATE_customCodeLine);
            /** def block 바로 위에 property block이 없을 경우 */      
            } else {
                thatBlock.setPropertyBlockFromDef(null);
            }
     
            var defPropertyDom = $(`<div class='vp-apiblock-blockoption-block 
                                             vp-apiblock-style-flex-row-end'>
                                    <span class='vp-block-optiontab-name 
                                                 vp-apiblock-style-flex-column-center'
                                          style='margin-right: 5px;'>
                                        Property
                                    </span>     
                                    <span class='vp-apiblock-style-flex-column-center'
                                          style='margin-right: 5px;'>
                                        @
                                    </span>                                     
                                </div>`);
     
            var inputDom = $(`<input class='vp-apiblock-option-input
                                            vp-apiblock-defproperty-input-${uuid}'
                                    style='width:25%; 
                                          margin-right: 5px;' 
                                    value="${propertyCodeLineState}"
                                    placeholder='input' >
                                </input> `);
     
        
            var propertyDeleteButton = MakeOptionDeleteButton(uuid);                            
            $(propertyDeleteButton).click(function() {
                var propertyBlock = thatBlock.getPropertyBlockFromDef();
                if (propertyBlock) {
                    propertyBlock.deleteLowerDepthChildBlocks();
                }
                blockContainerThis.renderBlockOptionTab();
            });     
     
            defPropertyDom.append(inputDom);
            defPropertyDom.append(propertyDeleteButton);
    
            /**  def 이름 function name */
            var defName = thatBlock.getState(STATE_defName);
            var defNameDom = RenderOptionPageName(thatBlock, defName, BLOCK_CODELINE_TYPE.DEF);
          
            defBlockOption.append( defPropertyDom );
            defBlockOption.append(defNameDom);
          
    
            var loadedVariableNameList = blockContainerThis.getKernelLoadedVariableNameList();
            var loadedVariableNameList_arg4 = [ ...Object.values( DEF_BLOCK_ARG4_TYPE ) ];
            var loadedVariableNameList_returnType = [ ...Object.values( DEF_BLOCK_ARG4_TYPE ) ];
            var loadedVariableNameList_arg5 = [ '0','1','2','3', '[1,2,3]', ...loadedVariableNameList ];
            var loadedVariableNameList_arg6 = [ ...Object.values( DEF_BLOCK_ARG6_TYPE ) ];

            /** Def Return param */
            var outParamDom = $(`<div class='vp-apiblock-blockoption-block 
                                            vp-apiblock-style-flex-row-between'>
                                                <span class='vp-block-optiontab-name 
                                                                vp-apiblock-style-flex-column-center'>
                                                    Return Type
                                                </span>
                                            </div>`);
            var suggestInputReturnType;                                     
            suggestInputReturnType =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_DEF_RETURN_TYPE + uuid
                                                                    , defReturnTypeState
                                                                    , loadedVariableNameList_returnType
                                                                    , VP_CLASS_STYLE_WIDTH_30PERCENT
                                                                    , 'Type'
                                                                    , function(selectedValue) {
                                                                        bindSelectValueEventFunc_def(selectedValue, 
                                                                                                    0,
                                                                                DEF_BLOCK_SELECT_VALUE_ARG_TYPE.RETURN_TYPE);
                                                                    });  
            outParamDom.append(suggestInputReturnType.toString());

            defBlockOption.append(outParamDom);
            
            var inParamDom = $(`<div class='vp-apiblock-blockoption-block 
                                         vp-apiblock-style-flex-row-between'>
                                    <span class='vp-block-optiontab-name 
                                                 vp-apiblock-style-flex-column-center'>
                                        In param
                                    </span>
                                </div>`);

            var defInParamContainer = $(`<div class='vp-apiblock-tab-navigation-node-block-title'>
                                         
                                                <div class='vp-apiblock-style-flex-row-center' >
 
                                          
                                                </div>
                                            </div>`);
            defBlockOption.append(inParamDom);
            /** Def defInParam 갯수만큼 bottom block 옵션에 렌더링 */
            var defInParamBody = $(`<div class='vp-apiblock-parambody'>
                                    </div>`);

            /** Def param */
            var defInParamList = thatBlock.getState(STATE_defInParamList);
            defInParamList.forEach((defInParams, index ) => {
                var loadedVariableNameList_arg3 = [ `arg${index + 1}`, ...loadedVariableNameList ];
      
         

                const { arg3, arg4, arg5, arg6 } = defInParams;

                var sbDefParam = new sb.StringBuilder();
                sbDefParam.appendFormatLine("<div class='{0}'  ", VP_CLASS_STYLE_FLEX_ROW_BETWEEN);
                sbDefParam.appendFormatLine("     style='{0}'  >",'');
       

                var sbDefVariable = new sb.StringBuilder();
                sbDefVariable.appendFormatLine("<div class='{0} {1}'>", VP_CLASS_STYLE_FLEX_ROW_BETWEEN 
                                                                            , VP_CLASS_STYLE_WIDTH_25PERCENT);
                if (arg6 == DEF_BLOCK_ARG6_TYPE.ARGS) {
                    sbDefVariable.appendLine("<span class='vp-apiblock-style-flex-column-center'>*</span>");
                } else if (arg6 == DEF_BLOCK_ARG6_TYPE.KWARGS) {
                    sbDefVariable.appendLine("<span class='vp-apiblock-style-flex-column-center'>**</span>");
                }                                                
                var suggestInputArg3 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_DEF_ARG_3 + index + uuid
                                                                                    , arg3
                                                                                    , loadedVariableNameList_arg3
                                                                                    , VP_CLASS_STYLE_WIDTH_100PERCENT
                                                                                    , STR_VARIABLE
                                                                                    , function(selectedValue) {
                                                                                        bindSelectValueEventFunc_def(selectedValue, 
                                                                                                                    index,
                                                                                                                    DEF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG3);
                                                                                        });   
                sbDefVariable.appendLine(suggestInputArg3.toString());
                sbDefVariable.appendLine("</div>");   
                
                sbDefParam.appendLine(sbDefVariable.toString());

                var suggestInputArg4;

                suggestInputArg4 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_DEF_ARG_4 + index + uuid
                                                                    , arg4
                                                                    , loadedVariableNameList_arg4
                                                                    , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                    , 'Type'
                                                                    , function(selectedValue) {
                                                                        bindSelectValueEventFunc_def(selectedValue, 
                                                                                                    index,
                                                                                                    DEF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG4);
                                                                });   
                sbDefParam.appendLine(suggestInputArg4.toString());   
                var suggestInputArg5 =  MakeVpSuggestInputText_apiblock(VP_ID_APIBLOCK_OPTION_DEF_ARG_5 + index + uuid
                                                                                            , arg5
                                                                                            , loadedVariableNameList_arg5
                                                                                            , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                                            , 'Default Val'
                                                                                            , function(selectedValue) {
                                                                                                bindSelectValueEventFunc_def(selectedValue, 
                                                                                                                            index,
                                                                                                                            DEF_BLOCK_SELECT_VALUE_ARG_TYPE.ARG5);
                                                                        }); 
                sbDefParam.appendLine(suggestInputArg5.toString());                                                                  
                var sbselectBoxArg6 = MakeOptionSelectBox(VP_ID_APIBLOCK_OPTION_DEF_ARG_6 + index + uuid
                                                                            , VP_CLASS_STYLE_WIDTH_20PERCENT
                                                                            , arg6
                                                                            , loadedVariableNameList_arg6);
                sbDefParam.appendLine(sbselectBoxArg6.toString());  
                
         
          
                                    
                var deleteButton = MakeOptionDeleteButton(VP_CLASS_APIBLOCK_PARAM_DELETE_BTN + index + uuid);
                sbDefParam.appendLine(deleteButton);
                sbDefParam.appendLine("</div>");

                var tblLayout = new vpTableLayoutVerticalSimple.vpTableLayoutVerticalSimple();
                tblLayout.setTHWidth("5%");
                tblLayout.addClass(VP_CLASS_STYLE_WIDTH_100PERCENT);
                tblLayout.addRow(index + 1, sbDefParam.toString());

                defInParamBody.append(tblLayout.toTagString());

            });
            defInParamContainer.append(defInParamBody);



            defBlockOption.append(defInParamContainer);
 
            var defPlusButton = MakeOptionPlusButton(VP_CLASS_APIBLOCK_PARAM_PLUS_BTN + uuid, '+ Param');
            defBlockOption.append(defPlusButton);
    

            /** bottom block option 탭에 렌더링된 dom객체 생성 */
            $(optionPageSelector).append(defBlockOption);
    

            var defInParamList = thatBlock.getState(STATE_defInParamList);  
            var defReturnTypeState = thatBlock.getState(STATE_defReturnType);
            defInParamList.forEach( (param,index) => {
                const { arg3, arg4, arg5, arg6 } = param;
        
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_3 + index + uuid).val(arg3);

                if (arg4 == DEF_BLOCK_ARG4_TYPE.INPUT_STR || arg4 == 'none') {
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_4 + index + uuid).val(STR_NULL);
                } else {
                    $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_4 + index + uuid).val(arg4);
                }
    
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_5 + index + uuid).val(arg5);
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_ARG_6 + index + uuid).val(arg6);
                
            });
            if (defReturnTypeState == DEF_BLOCK_ARG4_TYPE.INPUT_STR) {
                $(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_RETURN_TYPE + uuid).val(STR_NULL);
            } else {
                $( VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_DEF_RETURN_TYPE + uuid).val(defReturnTypeState);
            }
            // RenderInputRequiredColor(`.vp-apiblock-input-param-${index}-${thatBlock.getUUID()}`);
            /** def 파라미터 삭제 이벤트 함수 바인딩 */
            // blockContainerThis.bindDeleteParamEvent(thatBlock, BLOCK_CODELINE_TYPE.DEF);
            // inParamList.forEach( (_,index) => {
            //     RenderInputRequiredColor( STR_DOT + VP_CLASS_APIBLOCK_INPUT_PARAM + '-' + `${index}` + '-' + `${block.getUUID()}`);
            // });
            // RenderInputRequiredColor(STR_DOT + VP_CLASS_APIBLOCK_INPUT_PARAM + '-' + `${inParamList.length}` + '-' + `${block.getUUID()}`);
        
        }

        renderThisComponent();
    }

    return InitDefBlockOption;
});
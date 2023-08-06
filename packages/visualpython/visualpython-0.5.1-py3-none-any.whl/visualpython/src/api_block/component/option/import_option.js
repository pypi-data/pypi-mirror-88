define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb, 

              api
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

    const { RenderDefaultOrDetailButton
            , RenderInputRequiredColor

            , RenderDefaultImportDom
            , RenderCustomImportDom
            , RenderDefaultOrCustomImportContainer
            , ShowImportListAtBlock } = blockRenderer;

    const { BLOCK_DIRECTION
            , BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , IMPORT_BLOCK_TYPE

            , STR_COLON_SELECTED
            , STR_NULL
            , STR_FOR
            , STR_INPUT
            , STR_CLICK
            , STR_CHANGE
            , STR_CHANGE_KEYUP_PASTE

            , STR_BLOCK
            , STR_DISPLAY
            , STR_NONE

            
            , STATE_isBaseImportPage
            , STATE_baseImportList
            , STATE_customImportList } = constData;

    const { MakeOptionContainer
                , MakeOptionDeleteButton
                , MakeOptionPlusButton
                , MakeVpSuggestInputText_apiblock
                , MakeOptionInput } = baseComponent;
    /**
     * @param {Block} thatBlock Block
     * @param {string} optionPageSelector  Jquery 선택자
     */
    var InitImportBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();
        var blockContainerThis = thatBlock.getBlockContainerThis();
        var defaultImportContainer;
        var customImportContainer;
        var baseImportList = thatBlock.getState(STATE_baseImportList);
        var customImportList = thatBlock.getState(STATE_customImportList);
        
        /**
         * @event_function 
         */
        $(document).off(STR_CLICK, `.vp-apiblock-custom-import-plus-btn`);
        $(document).on(STR_CLICK, `.vp-apiblock-custom-import-plus-btn`, function(event) {

            var newData = {
                baseAcronyms : ''
                , baseImportName : 'numpy'
                , isImport : false
            }
            thatBlock.setState({
                customImportList: [ ...thatBlock.getState(STATE_customImportList), newData ]
            });
            var importCode = ShowImportListAtBlock(thatBlock);
            $(`.vp-block-header-${uuid}`).html(importCode);
            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });

        /**
         * default 옵션 클릭
         * @event_function 
         */
        $(document).off(STR_CLICK, `.vp-apiblock-default-option-${uuid}`);
        $(document).on(STR_CLICK, `.vp-apiblock-default-option-${uuid}`, function(event) {

            $(defaultImportContainer).css(STR_DISPLAY, STR_BLOCK);
            $(customImportContainer).css(STR_DISPLAY, STR_NONE);
            thatBlock.setState({
                isBaseImportPage: true
            });

            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });

        /**
         * detail 옵션 클릭
         * @event_function 
         */
        $(document).off(STR_CLICK, `.vp-apiblock-detail-option-${uuid}`);
        $(document).on(STR_CLICK, `.vp-apiblock-detail-option-${uuid}`, function(event) {

            $(customImportContainer).css(STR_DISPLAY, STR_BLOCK);
            $(defaultImportContainer).css(STR_DISPLAY, STR_NONE);
            thatBlock.setState({
                isBaseImportPage: false
            });
        
            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });

        customImportList.forEach((customImportData, index) => {
            const { isImport, baseImportName, baseAcronyms } = customImportData;

            /**
             * @event_function 
             */
            $(document).off(STR_CLICK, `.vp-apiblock-blockoption-custom-import-input-${index}`);
            $(document).on(STR_CLICK, `.vp-apiblock-blockoption-custom-import-input-${index}`, function(event) {
                var _isImport = isImport === true ? false : true;
                var updatedData = {
                    baseAcronyms: thatBlock.getState(STATE_customImportList)[index].baseAcronyms
                    , baseImportName
                    , isImport: _isImport
                }
                thatBlock.setState({
                    customImportList: UpdateOneArrayValueAndGet(thatBlock.getState(STATE_customImportList), index, updatedData)
                });
                var importCode = ShowImportListAtBlock(thatBlock);
                $(`.vp-block-header-${uuid}`).html(importCode);
                blockContainerThis.renderBlockOptionTab();

                event.stopPropagation();
            });

            /**
             * @event_function 
             */
            $(document).off(STR_CHANGE, `.vp-apiblock-blockoption-custom-import-select-${index}`);
            $(document).on(STR_CHANGE, `.vp-apiblock-blockoption-custom-import-select-${index}`, function(event) {    
                var updatedData = {
                    baseAcronyms: thatBlock.getState(STATE_customImportList)[index].baseAcronyms
                    , baseImportName : $(STR_COLON_SELECTED, this).val()
                    , isImport
                }
                
                thatBlock.setState({
                    customImportList: UpdateOneArrayValueAndGet(thatBlock.getState(STATE_customImportList), index, updatedData)
                });
                var importCode = ShowImportListAtBlock(thatBlock);
                $(`.vp-block-header-${uuid}`).html(importCode);
                blockContainerThis.renderBlockOptionTab();

                event.stopPropagation();
            });

            /**
             * @event_function 
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-blockoption-custom-import-textinput-${index}`);
            $(document).on(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-blockoption-custom-import-textinput-${index}`, function(event) {
                RenderInputRequiredColor(this);

                var updatedData = {
                    baseAcronyms : $(this).val()
                    , baseImportName 
                    , isImport
                }
                thatBlock.setState({
                    customImportList: UpdateOneArrayValueAndGet(thatBlock.getState(STATE_customImportList), index, updatedData)
                });
                var importCode = ShowImportListAtBlock(thatBlock);
                $(`.vp-block-header-${uuid}`).html(importCode);
                event.stopPropagation();
            });
        });
        
        baseImportList.forEach((_, index) => {

           /**
            * @event_function 
            */
            $(document).off(STR_CLICK, `.vp-apiblock-blockoption-default-import-input-${index}`);
            $(document).on(STR_CLICK, `.vp-apiblock-blockoption-default-import-input-${index}`, function(event) {
                var isImport = thatBlock.getState(STATE_baseImportList)[index].isImport;
                var baseImportName = thatBlock.getState(STATE_baseImportList)[index].baseImportName;
                var baseAcronyms = thatBlock.getState(STATE_baseImportList)[index].baseAcronyms;

                isImport = isImport === true ? false : true;
                var updatedData = {
                    isImport
                    , baseImportName
                    , baseAcronyms
                }
                thatBlock.setState({
                    baseImportList: UpdateOneArrayValueAndGet(thatBlock.getState(STATE_baseImportList), index, updatedData)
                });
                var importCode = ShowImportListAtBlock(thatBlock);
                $(`.vp-block-header-${uuid}`).html(importCode);
                blockContainerThis.renderBlockOptionTab();

                event.stopPropagation();
            }); 
        });

        /** Import option 렌더링 */
        var renderThisComponent = function() {
            var uuid = thatBlock.getUUID();
            var baseImportList = thatBlock.getState(STATE_baseImportList);

            var importBlockOption = MakeOptionContainer();
            var defaultOrDetailButton = RenderDefaultOrDetailButton(thatBlock, uuid, BLOCK_CODELINE_TYPE.IMPORT);
  
            importBlockOption.append(defaultOrDetailButton);

            /* ------------- import -------------- */
            var countisImport = 0;
            baseImportList.forEach(baseImportData => {
                if (baseImportData.isImport == true ) {
                    countisImport += 1;
                };
            });

            defaultImportContainer = RenderDefaultOrCustomImportContainer(IMPORT_BLOCK_TYPE.DEFAULT, countisImport);
            var defaultImportBody = $('<div><div>');
            baseImportList.forEach((baseImportData, index) => {
                var defaultImportDom = RenderDefaultImportDom(baseImportData, index);
                defaultImportBody.append(defaultImportDom);                        
            });

            /** -------------custom import ------------------ */
            var customImportList = thatBlock.getState(STATE_customImportList);
            var countIsCustomImport = 0;
            customImportList.forEach(baseImportData => {
                if (baseImportData.isImport == true ) {
                    countIsCustomImport += 1;
                };
            });

            // customImport 갯수만큼 bottom block 옵션에 렌더링
            customImportContainer = RenderDefaultOrCustomImportContainer(IMPORT_BLOCK_TYPE.CUSTOM, countIsCustomImport);
            var customImportBody = $(`<div class='vp-apiblock-customimport-body'>
                                    </div>`);
            customImportList.forEach((customImportData, index ) => {
                var customImportDom = RenderCustomImportDom(customImportData, index);
    ;
                var deleteButton = MakeOptionDeleteButton(index + uuid);
                $(deleteButton).click(function() {
                    thatBlock.setState({
                        customImportList: DeleteOneArrayValueAndGet(thatBlock.getState(STATE_customImportList), index)
                    });
                    
                    blockContainerThis.renderBlockOptionTab();
                });
                customImportDom.append(deleteButton);
                customImportBody.append(customImportDom);
            });

            var isBaseImportPage = thatBlock.getState(STATE_isBaseImportPage);
            if (isBaseImportPage == true) {
                defaultImportContainer.append(defaultImportBody);
                importBlockOption.append(defaultImportContainer);
            } else {
                customImportContainer.append(customImportBody);
                importBlockOption.append(customImportContainer);
            }
        
            $(optionPageSelector).append(importBlockOption);
        }

        renderThisComponent();
    }

    return InitImportBlockOption;
});
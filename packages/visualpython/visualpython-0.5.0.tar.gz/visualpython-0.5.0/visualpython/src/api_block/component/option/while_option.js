define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    
], function ( $, vpCommon, vpConst, sb, api, config, constData, blockRenderer ) {
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

    const { RenderOptionPageContainer
            , RenderOptionPageContainerInner
            , RenderOptionPageName

            , RenderInputRequiredColor
            , RenderBottomOptionTitle
        
 

            , GenerateClassInParamList
            , GenerateDefInParamList
            , GenerateReturnOutParamList
            , GenerateIfConditionList
            , GenerateForParam } = blockRenderer;

    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , STR_COLON_SELECTED
            , STR_FOR

            , STR_CHANGE_KEYUP_PASTE
            , STATE_whileCodeLine } = constData;

    var InitWhileBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();
        var blockContainerThis = thatBlock.getBlockContainerThis();


        /** 
         * @event_function
         * While code 변경 
         */
        $(document).off(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-while-input-${uuid}`);
        $(document).on(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-while-input-${uuid}`, function(event) {
            RenderInputRequiredColor(this);
            thatBlock.setState({
                whileCodeLine: $(this).val()
            });
            $(`.vp-block-header-${thatBlock.getUUID()}`).html(thatBlock.getState(STATE_whileCodeLine));
            event.stopPropagation();
        });

        /** 
         * @rendering
         * While Option 렌더링
         */
        var renderThisComponent = function() {
            var flexRow = RenderOptionPageContainer();
            var whileBlockOption = RenderOptionPageContainerInner();
    
            /* ------------- while -------------- */
            var whileDom = RenderOptionPageName(thatBlock, thatBlock.getState(STATE_whileCodeLine), BLOCK_CODELINE_TYPE.WHILE);
            whileBlockOption.append(whileDom);
            flexRow.append(whileBlockOption);
    
            /** bottom block option 탭에 렌더링된 dom객체 생성 */
            $(optionPageSelector).append(flexRow);
        }
        
        renderThisComponent();
    }

    return InitWhileBlockOption;
});
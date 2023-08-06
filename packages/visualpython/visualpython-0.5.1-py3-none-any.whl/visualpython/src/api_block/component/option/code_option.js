define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpAccordionBox'
    , 'nbextensions/visualpython/src/common/component/vpLineNumberTextArea'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb, vpAccordionBox, vpLineNumberTextArea

              , api
              , config
              , constData
              , blockRenderer

              , baseComponent ) {

    const { SetTextareaLineNumber_apiBlock } = api;
    const { PROCESS_MODE } = config;
    const { RenderInputRequiredColor
            , RenderCodeBlockInputRequired
            , ShowCodeBlockCode } = blockRenderer;

    const { BLOCK_CODELINE_TYPE
            , STR_CHANGE_KEYUP_PASTE

            , STR_NULL
            , STR_ONE_SPACE 
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_INPUT_YOUR_CODE
            , STR_COLOR

            , STATE_customCodeLine
            , COLOR_BLACK
            , COLOR_GRAY_input_your_code

            , VP_ID_PREFIX
            , VP_ID_APIBLOCK_OPTION_CODE_ARG

            , VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED } = constData;
    const { MakeOptionContainer
            , MakeLineNumberTextArea_apiblock } = baseComponent;
    /**
     * @param {Block} thatBlock Block
     * @param {string} optionPageSelector  Jquery 선택자
     */
    var InitCodeBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();

        
        /**
         *  @event_function
         *  code 변경 이벤트 함수 
         */
        $(document).off(STR_CHANGE_KEYUP_PASTE,  vpCommon.wrapSelector(vpCommon.formatString("#{0}",VP_ID_APIBLOCK_OPTION_CODE_ARG + uuid)));
        $(document).on(STR_CHANGE_KEYUP_PASTE, vpCommon.wrapSelector(vpCommon.formatString("#{0}",VP_ID_APIBLOCK_OPTION_CODE_ARG + uuid)), function(event) {
            RenderInputRequiredColor(this);
            var inputValue = $(this).val();
            thatBlock.setState({
                [STATE_customCodeLine]: inputValue
            });
            inputValue = ShowCodeBlockCode(thatBlock);
            /** 어떤 데이터도 입력되지 않을 때 */
            if (inputValue == STR_NULL) {
                $(`.vp-block-header-${uuid}`).html(STR_INPUT_YOUR_CODE);
                $(`.vp-block-header-${uuid}`).css(STR_COLOR, COLOR_GRAY_input_your_code);
  
            /** 데이터가 입력되었을 때 */
            } else {
                $(`.vp-block-header-${uuid}`).html(inputValue);
                $(`.vp-block-header-${uuid}`).css(STR_COLOR, COLOR_BLACK);
            }

            event.stopPropagation();
        });


        /** Code option 렌더링 */
        var renderThisComponent = function() {
            /** ------------ get state -------------*/
            var codeState = thatBlock.getState(STATE_customCodeLine);
            
            /* ------------- string builder render -------------- */
            var optionContainer = MakeOptionContainer();
            var lineNumberTextAreaStr = MakeLineNumberTextArea_apiblock(VP_ID_APIBLOCK_OPTION_CODE_ARG + uuid, 
                                                                        codeState); 
            // var lineNumberTextArea = new vpLineNumberTextArea.vpLineNumberTextArea(VP_ID_APIBLOCK_OPTION_CODE_ARG + uuid, 
            //                                                                         codeState);                                                                 
            // var lineNumberTextAreaStr = lineNumberTextArea.toTagString();
     
            optionContainer.append(lineNumberTextAreaStr);
   
            /** bottom block option 탭에 렌더링된 dom객체 생성 */
            $(optionPageSelector).append(optionContainer);

            /** 처음 Code Option 생성시,
             *  사용자가 입력한 값을 토대로
             *  라인 넘버를 생성하기 위해서 커스터 마이징한 api 사용 */
            SetTextareaLineNumber_apiBlock(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_CODE_ARG + uuid, codeState);

            /** Code Option State에 문자열이 1개도 없을 때 */                                                                                   
            if (codeState == STR_NULL) {
                RenderInputRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_CODE_ARG + uuid);
            }       
        }

        renderThisComponent();
    }

    return InitCodeBlockOption;
});
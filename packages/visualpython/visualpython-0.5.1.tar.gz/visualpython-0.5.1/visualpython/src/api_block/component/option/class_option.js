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
       
            , RenderClassParentDom


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
            , STATE_className
            , STATE_parentClassName } = constData;

    const { MakeOptionContainer
            , MakeOptionDeleteButton
            , MakeOptionPlusButton
            , MakeVpSuggestInputText_apiblock
            , MakeOptionInput } = baseComponent;
            
    var InitClassBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();
        var blockContainerThis = thatBlock.getBlockContainerThis();

        /**
         * @event_function
         * Class 이름 변경 이벤트 함수
         */
        $(document).off(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-input-class-name-${uuid}`);
        $(document).on(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-input-class-name-${uuid}`, function(event) {
            RenderInputRequiredColor(this);
            thatBlock.setState({
                className: $(this).val()
            });
            $(`.vp-block-header-class-name-${thatBlock.getUUID()}`).html($(this).val());
            event.stopPropagation();
        });

        /**
         * @event_function
         * parent class 상속 값 입력 이벤트 함수
         */ 
        $(document).off(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-input-param-0-${uuid}`);
        $(document).on(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-input-param-0-${uuid}`, function(event) {

            thatBlock.setState({
                parentClassName: $(this).val()
            });
            var classInParamStr = GenerateClassInParamList(thatBlock);
            $(`.vp-block-header-param-${thatBlock.getUUID()}`).html(classInParamStr);
            event.stopPropagation();
        });

        /** 
         * @event_function
         * Class option 렌더링 
         */
        var renderThisComponent = function() {
            var classBlockOption = MakeOptionContainer();
            /** class name */
   
            var classNameState = thatBlock.getState(STATE_className);                                
            var classNameDom = RenderOptionPageName(thatBlock, classNameState, BLOCK_CODELINE_TYPE.CLASS);
            var classParentDom = RenderClassParentDom(thatBlock);
            classBlockOption.append(classNameDom);
            classBlockOption.append(classParentDom);

            /** */
            /** option 탭에 렌더링된 dom객체 생성 */
            $(optionPageSelector).append(classBlockOption);
            /** class 파라미터 생성 이벤트 함수 바인딩 */
            // blockContainerThis.bindCreateParamEvent(thatBlock, BLOCK_CODELINE_TYPE.CLASS);
            /** class 파라미터 삭제 이벤트 함수 바인딩 */
            // blockContainerThis.bindDeleteParamEvent(thatBlock, BLOCK_CODELINE_TYPE.CLASS);
        }
        
        renderThisComponent();
    }

    return InitClassBlockOption;
});
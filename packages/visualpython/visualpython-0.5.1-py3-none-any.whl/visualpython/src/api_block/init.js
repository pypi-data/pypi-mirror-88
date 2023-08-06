define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'

    , './api.js'    
    , './config.js'
    , './constData.js'
    , './blockContainer.js'
    , './createBlockBtn.js'
    , './blockRenderer.js'
    
    , './component/boardMenuBar.js'
], function ( $, vpCommon, vpConst, 
              api, config, constData, blockContainer, createBlockBtn, blockRenderer,
              apiBlockMenuInit ) {
 
    const { ControlToggleInput
            , LoadVariableList } = api;
    const { PROCESS_MODE } = config;
    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , FOCUSED_PAGE_TYPE

            , VP_ID_PREFIX
            , VP_CLASS_PREFIX
            , VP_CLASS_APIBLOCK_MAIN
            , VP_CLASS_APIBLOCK_BODY
            , VP_CLASS_APIBLOCK_BUTTONS
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_OPTION_TAB
            , VP_CLASS_APIBLOCK_MENU_BTN
            , VP_CLASS_MAIN_CONTAINER
            , VP_CLASS_APIBLOCK_TITLE
            , VP_CLASS_APIBLOCK_CODELINE_ELLIPSIS

            , API_BLOCK_PROCESS_PRODUCTION
            , API_BLOCK_PROCESS_DEVELOPMENT
            , NUM_DELETE_KEY_EVENT_NUMBER

            
            , STR_IS_SELECTED
            , STR_TOP
            , STR_RIGHT
            , STR_SCROLL
            , STR_FOCUS
            , STR_BLUR
            , STR_INPUT
            , STR_CLICK
            , STR_MIN_WIDTH
            , STR_WIDTH 
            , STR_MAX_WIDTH
            , STR_OPACITY

            , STR_PARENT
            , STR_SOLID
            , STR_BORDER
            , STR_NOTEBOOK
            , STR_HEADER
            , STR_CELL
            , STR_CODEMIRROR_LINES
            , STR_3PX
            , STR_MSG_BLOCK_DELETED
        
            , COLOR_FOCUSED_PAGE } = constData;

    const { BindArrowBtnEvent } = blockRenderer;
    const BlockContainer = blockContainer;
    const CreateBlockBtn = createBlockBtn;
    
    var init = function(){

        /** block container 생성
         * 싱글톤 무조건 1개
         */
        var blockContainer = new BlockContainer();
        var createBlockBtnArray = Object.values(BLOCK_CODELINE_BTN_TYPE);

        createBlockBtnArray.forEach(enumData => {
            /** API 블럭 생성 금지 */
            if ( enumData == BLOCK_CODELINE_BTN_TYPE.API ) {
                return;
            }
            new CreateBlockBtn(blockContainer, enumData);
        });

        /**  블럭 up down 버튼 bind Event함수 */
        BindArrowBtnEvent();

        apiBlockMenuInit(blockContainer);
        
        /** block을 클릭하고 delete 키 눌렀을 때 */ 
        $(document).keyup(function(e) {
            var keycode =  e.keyCode 
                                ? e.keyCode 
                                : e.which;

            if (keycode == NUM_DELETE_KEY_EVENT_NUMBER
                && blockContainer.getFocusedPageType() == FOCUSED_PAGE_TYPE.EDITOR){
                var selectedBlock = blockContainer.getSelectedBlock();
                selectedBlock.deleteBlockFromDeleteBtn();
            } 
        });

        /** API Block board 스크롤 바 움직여도 오른쪽 위의 메뉴 버튼 고정 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).on(STR_SCROLL, function() {
            var scrollValue = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).scrollTop(); 
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + 'vp-apiblock-menu-button')).css(STR_TOP,  scrollValue);
        });

        /** API Block board 스크롤 바 움직여도 Option Page resize 버튼 고정 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).on(STR_SCROLL, function() {
            var scrollValue = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).scrollTop(); 
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_TOP,  scrollValue);
        });
        
        /** API Block board 스크롤 바 움직여도 Option Page resize 버튼 고정 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).on(STR_SCROLL, function() {
            var scrollValue = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).scrollTop(); 
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB + '.ui-resizable-handle')).css(STR_TOP,  scrollValue);
        });

        /** API Block 옵션 팝업 스크롤 바 움직여도 Option Page resize 버튼 고정 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).on(STR_SCROLL, function() {
            var scrollValue = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).scrollTop(); 
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB + '.ui-resizable-handle')).css(STR_TOP,  scrollValue);
        });

        {
            var optionPageRectWidth = blockContainer.getOptionPageWidth();
            if (blockContainer.getIsOptionPageOpen() == true) {
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('display', 'block');
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('width', optionPageRectWidth);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css('right', optionPageRectWidth + 5);
            } else {
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('display', 'none');
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('width', 0);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css('right', 5);
            }
        }

        /** API Block 화면 좌우로 resize 이벤트 함수 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).resizable({
            containment: STR_PARENT,
            handles: 'w',
            resizeHeight: false
            ,resize:(function() {
                var optionPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB))[0].getBoundingClientRect();
                var optionPageRectWidth = optionPageRect.width;
                blockContainer.setOptionPageWidth(optionPageRectWidth);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('width', optionPageRectWidth);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css('right', optionPageRectWidth + 5);
            })
        });


        /** api block 화면 이외에 화면을 클릭했을 때, page 포커스 해제 */
        $(vpCommon.wrapSelector(`${VP_ID_PREFIX}${STR_NOTEBOOK}, 
           ${VP_ID_PREFIX}${STR_HEADER}, 
           ${VP_CLASS_PREFIX}${STR_CELL}, 
           ${VP_CLASS_PREFIX}${STR_CODEMIRROR_LINES}`)).click(function(e) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.NULL);

        });
        
        /** Create block buttons page를 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS)).click(function(e) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.BUTTONS);
        });

        /** Block Board page를 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).click(function(e) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);
        });




        /** Option page를 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).click(function(event) {
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_BORDER, `${STR_3PX} ${COLOR_FOCUSED_PAGE} ${STR_SOLID}`);
        });
        
        /** Option Page를 닫았을 때 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + 'vp-apiblock-option-delete')).click(function() {
            blockContainer.setIsOptionPageOpen(false);
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('display', 'none');
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('width', '0px');
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css('right', '5px');
        });

        // 외부영역 클릭 시 팝업 닫기
        $(document).mouseup(function (e){
    
            var container = $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB);

            if (!container.is(e.target) && container.has(e.target).length === 0){
                // console.log('e.target',e.target);

                var children = e.target;

                if ( children && $(children).attr('class')) {
                    if ($(children).attr('class').indexOf('ui-menu-item-wrapper') != -1
                        || $(children).attr('class').indexOf('vp-apiblock-style-flex-row') != -1
                        || $(children).attr('class').indexOf('ui-autocomplete ui-front') != -1){
           
                        var optionPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB))[0].getBoundingClientRect();
                        var optionPageRectWidth = optionPageRect.width;
                        blockContainer.setOptionPageWidth(optionPageRectWidth);
                        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('width', optionPageRectWidth);
                        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css('right', optionPageRectWidth + 5);
                        
                    } else {
                       
                        blockContainer.setIsOptionPageOpen(false);
                        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('display', 'none');
                        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('width', '0px');
                        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css('right', '5px');
                    }
                }

            }	 else {
           
                var optionPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB))[0].getBoundingClientRect();
                var optionPageRectWidth = optionPageRect.width;
                blockContainer.setOptionPageWidth(optionPageRectWidth);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('width', optionPageRectWidth);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css('right', optionPageRectWidth + 5);
            }

            e.stopPropagation();


        });

        /** FIXME: 임시 */
        $(document).on(STR_CLICK, vpCommon.formatString(".{0}", 'vp-tab-header li:nth-child(2)'), function(event) {
            // console.log('클릭');
            LoadVariableList(blockContainer);
            blockContainer.renderBlockOptionTab();
            // event.stopPropagation();
        });

        ControlToggleInput();
        return blockContainer;
    }

    return init;
});
